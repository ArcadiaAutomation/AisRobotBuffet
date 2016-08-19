from LocalConfiger import LocalConfiger


def release_virtual_local_config(config_file, device_name):
    LocalConfiger.release_virtual_local_config(config_file, device_name)


def take_virtual_local_config(config_file, key):
    return LocalConfiger.take_virtual_local_config(config_file, key)
