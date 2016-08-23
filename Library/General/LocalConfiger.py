import time
import xml.etree.ElementTree as ElementTree
from FileLock import FileLock

# define constant
DEVICE_NAME = '#device_name'
SPACE_SPLITER = '    '


class State(object):
    NORMAL = 'Normal'
    BUSY = 'Busy'


class LocalConfiger:
    def __init__(self):
        print('hey.')

    @staticmethod
    def release_virtual_local_config(config_file, device_name):
        print(config_file)
        print(device_name)
        tree = ElementTree.parse(config_file)
        root = tree.getroot()
        device = root.find('.//device[@name="' + device_name + '"]')
        device.set('state', State.NORMAL)
        tree.write(config_file)

    @staticmethod
    def take_virtual_local_config(config_file, key):
        # type: (basestring, basestring) -> dictionary
        print(config_file)
        print(key)
        result = None
        with FileLock(config_file):
            tree = ElementTree.parse(config_file)
            root = tree.getroot()
            time.sleep(10)
            for device in root.findall('.//device[@state="Normal"]'):
                # state = device.find('state')
                # print(state.text)
                #  Check device state is normal
                # if state.text != State.NORMAL:
                #     print('State is ' + state.text + ' continue')
                #     continue

                # Check device is tag is support key
                if not LocalConfiger.__check_key_is_match_in_support_tag(device, key):
                    print('Device is not tag support ' + key + ' continue')
                    continue

                # Create virtual local config data
                result = LocalConfiger.__create_virtual_local_config_dictionary(device, key)

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
        # print (device)
        # print (key)
        tags = device.find('tags')
        for eachTag in tags.findall('tag'):
            if eachTag.text == key:
                print (key + ' tag is support')
                return True

        return False

    @staticmethod
    def __create_virtual_local_config_dictionary(device, key):
        pass
        print (device)
        print (key)
        # result = None
        result = {}
        key += "_"
        # Must be have a DEVICE NAME
        device_name = device.get('name')
        result[key + DEVICE_NAME] = device_name
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

        print(result)
        return result
