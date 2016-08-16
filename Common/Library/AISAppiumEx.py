import ast
from AppiumLibrary import AppiumLibrary
from appium import webdriver
from AtlasInfo import AtlasInfo


# create new class that inherits from AppiumLibrary
class AISAppiumEx(AppiumLibrary):
    # create a new keyword called "get application instance"
    # Public, element lookups
    def aisappium_get_driver_instance(self):
        """return current session Appium.
        """
        return self._current_application()

    def aisappium_set_driver_instance(self, oAppiumInfo):
        """set current session Appium.
        |oAppiumInfo=${AppInfo}|
        """
        self._cache.current = oAppiumInfo.driver

    def aisappium_open_application(self, remote_url, alias=None, **kwargs):
        """Connect to mobile and open application
        |remote_url=http://10.239.223.84/wd/hub|alias=None|cap|
        """
        index = AppiumLibrary.open_application(self, remote_url, alias, **kwargs)
        driver = self._current_application()
        oAppiumInfo = AtlasInfo(index, alias, driver, remote_url)
        return oAppiumInfo

    def aisappium_click_element(self, locator, oAppiumInfo=None):
        """Click element on mobile.
        |locator=xpath=//*[@id="id123"]|oAppiumInfo=${AppInfo}
        """
        self._info("Clicking mobile element '%s'." % locator)
        if oAppiumInfo is not None:
            self._element_find_atlas(locator, True, True, oAppiumInfo.driver).click()
        else:
            self._element_find(locator, True, True).click()

    def aisappium_clear_text(self, locator, oAppiumInfo=None):
        """Clears the text field identified by `locator`.

        |locator=xpath=//*[@id="id123"]|oAppiumInfo=${AppInfo}
        """
        self._info("Clear text field '%s'" % locator)
        if oAppiumInfo is not None:
            self._element_clear_text_by_locator_atlas(locator, oAppiumInfo.driver)
        else:
            self._element_clear_text_by_locator(locator)

    def aisappium_input_text(self, locator, text, oAppiumInfo=None):
        """Types the given `text` into text field identified by `locator`.

        |locator=xpath=//*[@id="id123"]|oAppiumInfo=${AppInfo}
        See `introduction` for details about locating elements.
        """
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        if oAppiumInfo is not None:
            self._element_input_text_by_locator_atlas(locator, text, oAppiumInfo.driver)
        else:
            self._element_input_text_by_locator(locator, text)

    def aisappium_input_password(self, locator, text, oAppiumInfo=None):
        """Types the given password into text field identified by `locator`.

        |locator=xpath=//*[@id="id123"]|oAppiumInfo=${AppInfo}

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self._info("Typing password into text field '%s'" % locator)
        if oAppiumInfo is not None:
            self._element_input_text_by_locator_atlas(locator, text, oAppiumInfo.driver)
        else:
            self._element_input_text_by_locator(locator, text)

    def aisappium_hide_keyboard(self, oAppiumInfo=None, key_name=None):
        """Hides the software keyboard on the device. (optional) In iOS, use `key_name` to press
        a particular key, ex. `Done`. In Android, no parameters are used.
        """
        if oAppiumInfo is not None:
            driver = oAppiumInfo.driver
        else:
            driver = self._current_application()
        driver.hide_keyboard(key_name)

    def aisappium_element_should_be_disabled(self, locator, loglevel='INFO', oAppiumInfo=None):
        """Verifies that element identified with locator is disabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if oAppiumInfo is not None:
            element = self._element_find_atlas(locator, True, True, oAppiumInfo.driver)
        else:
            element = self._element_find(locator, True, True)
        if element.is_enabled():
            self.log_source(loglevel)
            raise AssertionError("Element '%s' should be disabled "
                                 "but did not" % locator)
        self._info("Element '%s' is disabled ." % locator)

    def aisappium_element_should_be_enabled(self, locator, loglevel='INFO', oAppiumInfo=None):
        """Verifies that element identified with locator is enabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if oAppiumInfo is not None:
            element = self._element_find_atlas(locator, True, True, oAppiumInfo.driver)
        else:
            element = self._element_find(locator, True, True)
        if not element.is_enabled():
            self.log_source(loglevel)
            raise AssertionError("Element '%s' should be enabled "
                                 "but did not" % locator)
        self._info("Element '%s' is enabled ." % locator)

    def aisappium_element_name_should_be(self, locator, expected, oAppiumInfo=None):
        """Verifies that element's name identified with locator is equal 'expected'.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if oAppiumInfo is not None:
            element = self._element_find_atlas(locator, True, True, oAppiumInfo.driver)
        else:
            element = self._element_find(locator, True, True)
        if expected != element.get_attribute('name'):
            raise AssertionError("Element '%s' name should be '%s' "
                                 "but it is '%s'." % (locator, expected, element.get_attribute('name')))
        self._info("Element '%s' name is '%s' " % (locator, expected))

    def aisappium_element_value_should_be(self, locator, expected, oAppiumInfo=None):
        """Verifies that element's value identified with locator is equal 'expected'.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if oAppiumInfo is not None:
            element = self._element_find_atlas(locator, True, True, oAppiumInfo.driver)
        else:
            element = self._element_find(locator, True, True)
        if expected != element.get_attribute('value'):
            raise AssertionError("Element '%s' value should be '%s' "
                                 "but it is '%s'." % (locator, expected, element.get_attribute('value')))
        self._info("Element '%s' value is '%s' " % (locator, expected))

    def aisappium_element_attribute_should_match(self, locator, attr_name, match_pattern, regexp=False,
                                              oAppiumInfo=None):
        """Verify that an attribute of an element matches the expected criteria.

        The element is identified by _locator_. See `introduction` for details
        about locating elements. If more than one element matches, the first element is selected.

        The _attr_name_ is the name of the attribute within the selected element.

        The _match_pattern_ is used for the matching, if the match_pattern is
        - boolean or 'True'/'true'/'False'/'false' String then a boolean match is applied
        - any other string is cause a string match

        The _regexp_ defines whether the string match is done using regular expressions (i.e. BuiltIn Library's
        [http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Should%20Match%20Regexp|Should
        Match Regexp] or string pattern match (i.e. BuiltIn Library's
        [http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Should%20Match|Should
        Match])


        Examples:

        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | text | *foobar |
        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | text | f.*ar | regexp = True |
        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | enabled | True |

        | 1. is a string pattern match i.e. the 'text' attribute should end with the string 'foobar'
        | 2. is a regular expression match i.e. the regexp 'f.*ar' should be within the 'text' attribute
        | 3. is a boolead match i.e. the 'enabled' attribute should be True


        _*NOTE: *_
        On Android the supported attribute names are hard-coded in the
        [https://github.com/appium/appium/blob/master/lib/devices/android/bootstrap/src/io/appium/android/bootstrap/AndroidElement.java|AndroidElement]
        Class's getBoolAttribute() and getStringAttribute() methods.
        Currently supported (appium v1.4.11):
        _contentDescription, text, className, resourceId, enabled, checkable, checked, clickable, focusable, focused, longClickable, scrollable, selected, displayed_


        _*NOTE: *_
        Some attributes can be evaluated in two different ways e.g. these evaluate the same thing:

        | Element Attribute Should Match | xpath = //*[contains(@text,'example text')] | name | txt_field_name |
        | Element Name Should Be         | xpath = //*[contains(@text,'example text')] | txt_field_name |      |

        """
        if oAppiumInfo is not None:
            elements = self._element_find_atlas(locator, False, True, oAppiumInfo.driver)
        else:
            elements = self._element_find(locator, False, True)
        if len(elements) > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        attr_value = elements[0].get_attribute(attr_name)

        # ignore regexp argument if matching boolean
        if isinstance(match_pattern, bool) or match_pattern.lower() == 'true' or match_pattern.lower() == 'false':
            if isinstance(match_pattern, bool):
                match_b = match_pattern
            else:
                match_b = ast.literal_eval(match_pattern.title())

            if isinstance(attr_value, bool):
                attr_b = attr_value
            else:
                attr_b = ast.literal_eval(attr_value.title())

            self._bi.should_be_equal(match_b, attr_b)

        elif regexp:
            self._bi.should_match_regexp(attr_value, match_pattern,
                                         msg="Element '%s' attribute '%s' should have been '%s' "
                                             "but it was '%s'." % (locator, attr_name, match_pattern, attr_value),
                                         values=False)
        else:
            self._bi.should_match(attr_value, match_pattern,
                                  msg="Element '%s' attribute '%s' should have been '%s' "
                                      "but it was '%s'." % (locator, attr_name, match_pattern, attr_value),
                                  values=False)
        # if expected != elements[0].get_attribute(attr_name):
        #    raise AssertionError("Element '%s' attribute '%s' should have been '%s' "
        #                         "but it was '%s'." % (locator, attr_name, expected, element.get_attribute(attr_name)))
        self._info("Element '%s' attribute '%s' is '%s' " % (locator, attr_name, match_pattern))

    def aisappium_set_network_connection_status(self, connectionStatus, oAppiumInfo=None):
        """Sets the network connection Status.

        Android only.

        Possible values:
            | =Value= | =Alias=          | =Data= | =Wifi= | =Airplane Mode=  |
            |  0      | (None)           | 0      |   0    | 0                |
            |  1      | (Airplane Mode)  | 0      |   0    | 1                |
            |  2      | (Wifi only)      | 0      |   1    | 0                |
            |  4      | (Data only)      | 1      |   0    | 0                |
            |  6      | (All network on) | 1      |   1    | 0                |
        """
        if oAppiumInfo is not None:
            driver = oAppiumInfo.driver
        else:
            driver = self._current_application()
        return driver.set_network_connection(int(connectionStatus))

    def aisappium_get_elements(self, locator, first_element_only=False, fail_on_error=True, oAppiumInfo=None):
        """Return elements that match the search criteria

        The element is identified by _locator_. See `introduction` for details
        about locating elements.

        If the _first_element_ is set to 'True' then only the first matching element is returned.

        If the _fail_on_error_ is set to 'True' this keyword fails if the search return nothing.

        Returns a list of [http://selenium-python.readthedocs.org/en/latest/api.html#module-selenium.webdriver.remote.webelement|WebElement] Objects.
        """
        if oAppiumInfo is not None:
            element = self._element_find_atlas(locator, first_element_only, fail_on_error, oAppiumInfo.driver)
        else:
            element = self._element_find(locator, first_element_only, fail_on_error)
        return element

    def aisappium_get_element_attribute(self, locator, attribute, oAppiumInfo=None):
        """Get element attribute using given attribute: name, value,...

        Examples:

        | Get Element Attribute | locator | name |
        | Get Element Attribute | locator | value |
        """
        if oAppiumInfo is not None:
            elements = self._element_find_atlas(locator, False, True, oAppiumInfo.driver)
        else:
            elements = self._element_find(locator, False, True)
        ele_len = len(elements)
        if ele_len == 0:
            raise AssertionError("Element '%s' could not be found" % locator)
        elif ele_len > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        try:
            attr_val = elements[0].get_attribute(attribute)
            self._info("Element '%s' attribute '%s' value '%s' " % (locator, attribute, attr_val))
            return attr_val
        except:
            raise AssertionError("Attribute '%s' is not valid for element '%s'" % (attribute, locator))

    def aisappium_get_elements_attribute(self, locator, attribute, oAppiumInfo=None):
        """Get element attribute using given attribute: name, value,...

        Examples:

        | Get Element Attribute | locator | name |
        | Get Element Attribute | locator | value |
        """
        if oAppiumInfo is not None:
            elements = self._element_find_atlas(locator, False, True, oAppiumInfo.driver)
        else:
            elements = self._element_find(locator, False, True)
        ele_len = len(elements)
        if ele_len == 0:
            raise AssertionError("Element '%s' could not be found" % locator)
        elif ele_len > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        try:
            attr_val = []
            for num in range(ele_len-1, 0, -1):
                attr_val.append(elements[num].get_attribute(attribute))
            self._info("Element '%s' attribute '%s' " % (locator, attribute))
            return attr_val
        except:
            raise AssertionError("Attribute '%s' is not valid for element '%s'" % (attribute, locator))

    def aisappium_get_element_attribute_index(self, locator, attribute, index, oAppiumInfo=None):
        """Get element attribute using given attribute: name, value,...

        Examples:

        | Get Element Attribute | locator | name |
        | Get Element Attribute | locator | value |
        """
        if oAppiumInfo is not None:
            elements = self._element_find_atlas(locator, False, True, oAppiumInfo.driver)
        else:
            elements = self._element_find(locator, False, True)
        ele_len = len(elements)
        if ele_len == 0:
            raise AssertionError("Element '%s' could not be found" % locator)
        elif ele_len > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        try:
            attr_val = elements[ele_len - int(index)].get_attribute(attribute)
            self._info("Element '%s' attribute '%s' value '%s' " % (locator, attribute, attr_val))
            return attr_val
        except:
            raise AssertionError("Attribute '%s' is not valid for element '%s'" % (attribute, locator))

    def aisappium_get_element_location(self, locator, oAppiumInfo=None):
        """Get element location

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if oAppiumInfo is not None:
            element = self._element_find_atlas(locator, True, True, oAppiumInfo.driver)
        else:
            element = self._element_find(locator, True, True)
        element_location = element.location
        self._info("Element '%s' location: %s " % (locator, element_location))
        return element_location

    def aisappium_get_element_size(self, locator, oAppiumInfo=None):
        """Get element size

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if oAppiumInfo is not None:
            element = self._element_find_atlas(locator, True, True, oAppiumInfo.driver)
        else:
            element = self._element_find(locator, True, True)
        element_size = element.size
        self._info("Element '%s' size: %s " % (locator, element_size))
        return element_size

    # Private
    def _element_clear_text_by_locator_atlas(self, locator, Mdriver):
        try:
            element = self._element_find_atlas(locator, True, True, Mdriver)
            element.clear()
        except Exception, e:
            raise e

    def _element_input_text_by_locator_atlas(self, locator, text, Mdriver):
        try:
            element = self._element_find_atlas(locator, True, True, Mdriver)
            element.send_keys(text)
        except Exception, e:
            raise e

    def _element_input_value_by_locator_atlas(self, locator, text, Mdriver):
        try:
            element = self._element_find_atlas(locator, True, True, Mdriver)
            element.set_value(text)
        except Exception, e:
            raise e

    def _element_find_atlas(self, locator, first_only, required, Mdriver, tag=None):
        elements = self._element_finder.find(Mdriver, locator, tag)
        if required and len(elements) == 0:
            raise ValueError("Element locator '" + locator + "' did not match any elements.")
        if first_only:
            if len(elements) == 0: return None
            return elements[0]
        return elements

    def _is_element_present_atlas(self, locator, Mdriver):
        elements = self._element_finder.find(Mdriver, locator, None)
        return len(elements) > 0
