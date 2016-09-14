from copy_reg import add_extension

from pip._vendor.requests.packages.urllib3.util import url
from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver


def SetChromeOption():
    options = webdriver.ChromeOptions()
    options.add_extension('C:/Users/AtlasRobot/Downloads/ModHeader_2_1_1.crx')
    # options.add_argument("user-data-dir=C:/Program Files (x86)/Google/Chrome/Application/52.0.2743.116");
    # driver = webdriver.Remote('http://10.239.223.84:4444/wd/hub', options.to_capabilities())
    return options.to_capabilities()


def openBrowserWithExtension():
    options = webdriver.ChromeOptions()
    options.add_argument('--load-and-launch-app=C:/Users/AtlasRobot/Downloads/ModHeader_2_1_1.crx')
    capabilities = webdriver.DesiredCapabilities()
    instance = BuiltIn().get_library_instance('Selenium2Library').create_webdriver('Remote', command_executor=url,
                                                                                   desired_capabilities=options.to_capabilities())
    return instance


def OpenAndSetUpBrowser():
    options = webdriver.ChromeOptions()
    options.add_extension('C:/Users/AtlasRobot/Downloads/ModHeader_2_1_1.crx')
    driver = webdriver.Remote('http://10.239.223.84:4444/wd/hub', options.to_capabilities())
    driver.get('chrome-extension://idgpnmonknjnojddfkpgkljpfnnfcklj/icon.png')
    driver.execute_script(
        'localStorage.setItem("profiles", JSON.stringify([{title: "Selenium", hideComment: true, appendMode: "",headers: [{enabled: true, name: "X-Forwarded-For", value: "10.239.223.84", comment: ""}],respHeaders: [],filters: []}]));')
    driver.get('https://www.google.com')
