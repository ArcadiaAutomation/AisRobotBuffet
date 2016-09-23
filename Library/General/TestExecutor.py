import runParallel

from LocalConfiger import LocalConfiger

robot_path = "D:\ArcadiaAtlas\Robot\eServiceWebPostPaid_BuffeStyle"
suit = "eServiceWebPostPaidLogin.txt"
output = "D:\OutputTest"
flag = "debug"
config_file = "D:\ArcadiaAtlas\Robot\Config\ParallelLocalConfig.xml"
filters = {'3PO_1': 'include', 'virtual_AisCloudRegistered': 'exclude'}
key_name = "virtual_3PO_1"


runParallel.parallel_execution(robot_path, suit, output, flag, "EN", "gc")


#
# result = LocalConfiger.take_virtual_local_config(config_file, key_name, filters)
#
# device_name = result[key_name + "_" + '#device_name']
# timestamp = result[key_name + "_" + '#timestamp']
# LocalConfiger.release_virtual_local_config(config_file, device_name, timestamp)