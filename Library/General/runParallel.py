from multiprocessing import Pool
from multiprocessing import Process
from threading import Thread
import subprocess as subp
import os
import sys
import time
from robot.conf.settings import RobotSettings
from robot.result import ExecutionResult
from robot.running.model import TestSuite
from robot.api import TestSuiteBuilder
import threading

from functools import partial


def call_script(run_dir, robot_test_suite, robot_output, tag, lang, browser, run_name):
    print "in call script"
    # command = "robot -t " + run_name + " -d " + dir_path + " -o output" + run_name + " -r report" + run_name \
    #           + " -l log" + run_name + " -v ar_LANG:" + LANG + " -v ar_BROWSER:" + BROWSER + " -i " + tag + " " \
    #           + robot_test_suite
    command = "pybot -t " + run_name + " -d " + robot_output + " -o output" + run_name + lang + " -r report" + run_name\
              + lang + " -l log" + run_name + lang + " -v ar_LANG:" + lang + " -v ar_BROWSER:" + browser + " -i " + tag\
              + " " + robot_test_suite
    print "command is a " + command
    os.system(command)
    # subp.call(args, shell=True)
    # thread = Thread(group=None, target=lambda: os.system(command))
    # thread.start()
    # thread.join()


def parallel_execution(robot_path, robot_test_suite, robot_output, tag="*", lang="EN", browser="gc"):
    print "begin"
    run_name = []
    path = robot_path + '\\' + robot_test_suite
    suite = TestSuiteBuilder().build(path)
    suite.filter(included_tags=tag)
    tests = suite.tests
    print tests
    for test in tests:
        run_name.append(str(test))
    threads = []
    print "path : " + path
    dir_path = path.replace(".txt", "")
    print "dir_path : " + dir_path
    print "len : " + str(len(run_name))
    # run_name = ['[F01-001]eServiceWeb-PO-Login-NumberNotComplete', '[F01-002]eServiceWeb-PO-Login-NumberDtac']
    # run_dir = "D:\ArcadiaAtlas\Robot\eServiceWebPostPaid_BuffeStyle"
    # run_name = tests
    run_dir = dir_path
    os.chdir(robot_path)
    pool = Pool(len(run_name))
    func = partial(call_script, run_dir, robot_test_suite, robot_output, tag, lang, browser)
    pool.map_async(func, run_name)
    pool.close()
    pool.join()
    # for i in range(len(run_name)):
    #     # os.chdir(robot_path)
    #
    #     # command = "robot -t " + run_name[i] + " -d " + dir_path + " -o output" + run_name[
    #     #     i] + " -r report" + run_name[i] + " -l log" + run_name[
    #     #               i] + " -v ar_LANG:" + LANG + " -v ar_BROWSER:" + BROWSER + " -i " + tag + " " + robot_test_suite
    #     print "run_name => " + run_name[i]
    #     pool.apply_async(test_copy, args=(run_name[i],))
    #
    # pool.close()
    # pool.join()
        # thread = Thread(target=call_script, args=(command,))
        # threads.append(thread)
    # [t.start() for t in threads]
    # [t.join() for t in threads]

    print "finished..."

if __name__ == "__main__":
    # (robot_path, robot_test_suite, tag = "*", LANG = "EN", BROWSER = "gc")
    # parallel_execution("D:\ArcadiaAtlas\Robot\eServiceWebPostPaid_BuffeStyle", "eServiceWebPostPaidLogin.txt", "ptest")
    # parallel_execution("D:\ArcadiaAtlas\Robot\eServiceWebPostPaid_BuffeStyle", "eServiceWebPostPaidBillAISPostpaid.txt", "T1")
    print "[0] => " + sys.argv[0]
    print "[1] => " + sys.argv[1]   # => robot path
    print "[2] => " + sys.argv[2]   # => robot test suite
    print "[3] => " + sys.argv[3]   # => robot output report
    print "[4] => " + sys.argv[4]   # => tag
    print "[5] => " + sys.argv[5]   # => lang
    print "[6] => " + sys.argv[6]   # => browser
    parallel_execution(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])


# def call_script(args):
#     subp.call(args, shell=True)
#
#
# def testHello(str1, str2):
#     print "Str1 = " + str1 + " Str2 = " + str2
#
#
# def parallel_execution(robot_path, robot_test_suite, tag="*", LANG="EN", BROWSER="gc"):
#     print "begin"
#     run_name = []
#     path = robot_path + '\\' + robot_test_suite
#     suite = TestSuiteBuilder().build(path)
#     suite.filter(included_tags=tag)
#     tests = suite.tests
#     print tests
#     for test in tests:
#         run_name.append(str(test))
#     threads = []
#     print "path : " + path
#     dir_path = path.replace(".txt", "")
#     print "dir_path : " + dir_path
#
#     for i in range(len(run_name)):
#         os.chdir(robot_path)
#         command = "robot -t " + run_name[i] + " -d " + dir_path + " -o output" + run_name[
#             i] + " -r report" + run_name[i] + " -l log" + run_name[
#                       i] + " -v ar_LANG:" + LANG + " -v ar_BROWSER:" + BROWSER + " -i " + tag + " " + robot_test_suite
#         thread = Thread(target=call_script, args=(command,))
#         threads.append(thread)
#     [t.start() for t in threads]
#     [t.join() for t in threads]