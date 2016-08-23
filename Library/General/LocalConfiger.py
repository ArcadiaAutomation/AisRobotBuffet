import datetime
import xml.etree.ElementTree as ElementTree
from FileLock import FileLock


# define constant
DEVICE_NAME = '#device_name'
TIMESTAMP = '#timestamp'


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
    def take_virtual_local_config(config_file, key_tag):
        # type: (basestring, basestring) -> dictionary
        result = None
        with FileLock(config_file):
            tree = ElementTree.parse(config_file)
            root = tree.getroot()
            for device in root.findall('.//device[@state="' + State.NORMAL + '"]'):

                # Check device is tag is support key
                if not LocalConfiger.__check_key_is_match_in_support_tag(device, key_tag):
                    print('Device ' + device.get('name') + ' is not tag support ' + key_tag + ' continue')
                    continue

                # Mark timestamp
                device.set('timestamp', str(datetime.datetime.utcnow()))

                # Create virtual local config data
                result = LocalConfiger.__create_virtual_local_config_dictionary(device, key_tag)

                # Mark sate to Busy
                device.set('state', State.BUSY)

                # Update xml local config file.
                tree.write(config_file)

                # Return and exit function
                return result

        # All busy or not support throw fail
        raise Exception('All busy or not support.')

    @staticmethod
    def __check_key_is_match_in_support_tag(device, key):
        pass
        tags = device.find('tags')
        for eachTag in tags.findall('tag'):
            if eachTag.text == key:
                print (key + ' tag is support')
                return True

        return False

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
