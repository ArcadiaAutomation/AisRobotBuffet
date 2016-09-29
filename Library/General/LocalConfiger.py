import logging
import xml.etree.ElementTree as ElementTree
import os.path
from DateTime import datetime
from FileLock import FileLock

# define constant
DEVICE_NAME = '#device_name'
TIMESTAMP = '#timestamp'
INCLUDE = 'include'
EXCLUDE = 'exclude'


class State(object):
    NORMAL = 'Normal'
    BUSY = 'Busy'


class LocalConfiger:
    def __init__(self):
        print('hey.')
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def release_virtual_local_config(config_file, device_name, timestamp, max_repeat=3):
        lock = FileLock(config_file)
        if max_repeat <= 0:
            msg_error_over_max_repeat = 'Over maximum repeat to release device name ' \
                                        + device_name + ' with timestamp ' + timestamp
            logging.error(msg_error_over_max_repeat)
            raise Exception(msg_error_over_max_repeat)
        try:
            with lock:
                tree = ElementTree.parse(config_file)
                root = tree.getroot()
                device = root.find('.//device[@name="' + device_name + '"]')
                if timestamp != device.get('timestamp'):
                    # Will can not change state because this locked by another.
                    logging.info('timestamp not valid to release device ' + device_name)
                    # print('timestamp not valid to release device ' + device_name)
                    return
                device.set('state', State.NORMAL)
                tree.write(config_file)
                logging.info("Release success = > " + device_name + " Time => " + timestamp)
                # print "Release success = > " + device_name + " Time => " + timestamp

        except:
            if os.path.isfile(config_file + ".lock"):
                lock.release()
                max_repeat -= 1
                release_virtual_local_config(config_file, device_name, timestamp, max_repeat)
            msg_error_when_release_virtual = 'Found error when try to release virtual data.'
            logging.error(msg_error_when_release_virtual)
            raise Exception(msg_error_when_release_virtual)

    @staticmethod
    def take_virtual_local_config(config_file, key_name, key_tag):
        # type: (basestring, basestring) -> dictionary
        result = None
        original_tree = None
        lock = FileLock(config_file)
        try:

            with lock:
                original_tree = ElementTree.parse(config_file)
                tree = ElementTree.parse(config_file)
                root = tree.getroot()
                for device in root.findall('.//device[@state="' + State.NORMAL + '"]'):
                    # Check device is tag is support key
                    if not LocalConfiger.__check_key_is_match_in_support_tag(device, key_tag):
                        msg_not_support_tag_and_try_next = 'Device ' + device.get('name') \
                                                           + ' is not support tags and will continue next device.'
                        logging.info(msg_not_support_tag_and_try_next)
                        # print(msg_not_support_tag_and_try_next)
                        continue

                    # Mark timestamp
                    device.set('timestamp', str(datetime.now()))

                    # Create virtual local config data
                    result = LocalConfiger.__create_virtual_local_config_dictionary(device, key_name)

                    # Mark sate to Busy
                    device.set('state', State.BUSY)

                    # Update xml local config file.
                    tree.write(config_file)

                    # Return and exit function
                    # return result
                    break

                if result is not None:
                    logging.warning("Take virtual devices success.")
                    return result

        except:
            if os.path.isfile(config_file + ".lock"):
                # try to reset to normal state
                original_tree.write(config_file)
                lock.release()

            msg_err_try_to_take_virtual = 'Found error when try to take virtual data.'
            logging.error(msg_err_try_to_take_virtual)
            raise Exception(msg_err_try_to_take_virtual)

        # All busy or not support throw fail
        msg_all_busy_or_not_support = 'All busy or not support...'
        logging.warning(msg_all_busy_or_not_support)
        raise Exception(msg_all_busy_or_not_support)

    @staticmethod
    def __check_key_is_match_in_support_tag(device, filters):
        pass
        msg_filters = "filters : " + str(len(filters))
        logging.info(msg_filters)
        if len(filters) == 0:
            msg_not_found_tag = 'Not found tag filter.'
            logging.error(msg_not_found_tag)
            raise Exception(msg_not_found_tag)
        tags_in_xml = {}
        tags = device.find('tags')
        for eachTag in tags.findall('tag'):
            key = eachTag.text
            value = None
            tags_in_xml.update({key: value})

        for each_filter in filters:
            # if each filter is include
            if filters.get(each_filter) == INCLUDE:
                # check is must in tags_in_xml if not reject
                if each_filter not in tags_in_xml:
                    return False

            # else if each filter is exclude
            elif filters.get(each_filter) == EXCLUDE:
                # check is must be not in tags_in_xml if not reject
                if each_filter in tags_in_xml:
                    return False

            # else
            else:
                # filter not support throw error
                msg_not_support_filter = 'Not support filter ' + filters.get(each_filter)
                logging.error(msg_not_support_filter)
                raise Exception(msg_not_support_filter)

        # All condition is passed.
        return True

    @staticmethod
    def __create_virtual_local_config_dictionary(device, key):
        pass
        # result = None
        result = {}
        key += "_"
        # Must have a DEVICE NAME
        device_name = device.get('name')
        result[key + DEVICE_NAME] = device_name
        # Must have a TIMESTAMP
        timestamp = device.get('timestamp')
        result[key + TIMESTAMP] = timestamp
        # Get default element
        default = device.find('default')
        items = default.findall('item')
        for item in items:
            # Define key name
            keyname = key + item.get('name')
            # Check type of value
            if item.get('type') == 'Scalar':
                result[keyname] = item.find('value').text
            elif item.get('type') == 'List':
                values = item.findall('value')
                list_value = []
                for value in values:
                    list_value.append(value.text)
                result[keyname] = list_value
            elif item.get('type') == 'Dictionary':
                values = item.findall('value')
                dic_value = {}
                for value in values:
                    name = value.get('name')
                    dic_value[name] = value.text
                result[keyname] = dic_value

        return result
