from LocalConfiger import LocalConfiger


def release_virtual_local_config(config_file, device_name, timestamp):
    LocalConfiger.release_virtual_local_config(config_file, device_name, timestamp)


def take_virtual_local_config(config_file, key_name, key_tag):
    return LocalConfiger.take_virtual_local_config(config_file, key_name, key_tag)
