
class AtlasInfo:
    def __init__(self, index, alise, driver, remote_url):
        self.index = index
        self.alise = alise
        self.driver = driver
        self.remote_url = remote_url

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def setAlias(self, alise):
        self.alise = alise

    def getAlias(self):
        return self.alise

    def setDriver(self, driver):
        self.driver = driver

    def getDriver(self):
        return self.driver
