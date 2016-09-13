import datetime
import xml.etree.ElementTree as ElementTree
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

    @staticmethod
    def release_virtual_local_config(config_file, device_name, timestamp):
        with FileLock(config_file):
            tree = ElementTree.parse(config_file)
            root = tree.getroot()
            device = root.find('.//device[@name="' + device_name + '"]')
            if timestamp != device.get('timestamp'):
                # Will can not change state because this locked by another.
                print('timestamp not valid to release device ' + device_name)
                return
            device.set('state', State.NORMAL)
            tree.write(config_file)

    @staticmethod
    def take_virtual_local_config(config_file, key_name, key_tag):
        # type: (basestring, basestring) -> dictionary
        result = None
        with FileLock(config_file):
            tree = ElementTree.parse(config_file)
            root = tree.getroot()
            for device in root.findall('.//device[@state="' + State.NORMAL + '"]'):
                # Check device is tag is support key
                if not LocalConfiger.__check_key_is_match_in_support_tag(device, key_tag):
                    print('Device ' + device.get('name') + ' is not support tags and will continue next device.')
                    continue

                # Mark timestamp
                device.set('timestamp', str(datetime.datetime.utcnow()))

                # Create virtual local config data
                result = LocalConfiger.__create_virtual_local_config_dictionary(device, key_name)

                # Mark sate to Busy
                device.set('state', State.BUSY)

                # Update xml local config file.
                tree.write(config_file)

                # Return and exit function
                return result

        # All busy or not support throw fail
        raise Exception('All busy or not support.')

    @staticmethod
    def __check_key_is_match_in_support_tag(device, filters):
        pass
        print "filters : " + str(len(filters))
        if len(filters) == 0:
            raise Exception('Not found tag filter.')
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
                raise Exception('Not support filter ' + filters.get(each_filter))

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
