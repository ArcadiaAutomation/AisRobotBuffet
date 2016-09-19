from LocalConfiger import LocalConfiger


config_file = "D:\ArcadiaAtlas\Robot\Config\ParallelLocalConfig.xml"
filters = {'virtual_3PO_1': 'include', 'virtual_AisCloudRegistered': 'exclude'}
key_name = "virtual_3PO_1"
result = LocalConfiger.take_virtual_local_config(config_file, key_name, filters)

device_name = result[key_name + "_" + '#device_name']
timestamp = result[key_name + "_" + '#timestamp']
# LocalConfiger.release_virtual_local_config(config_file, device_name, timestamp)
