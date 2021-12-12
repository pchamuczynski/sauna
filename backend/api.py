import backend

class SaunaApi:
    def __init__(self, backend):
        self.backend = backend

    def stop(self):
        self.backend.stop()

    def getSaunaTempSetting(self):
        return self.backend.sauna_temp_setting

    def getHouseTempSetting(self):
        return self.backend.house_temp_setting

    def increaseHouseTemp(self):
        self.backend.increaseHouseTemp()

    def decreaseHouseTemp(self):
        self.backend.decreaseHouseTemp()

    def increaseSaunaTemp(self):
        self.backend.increaseSaunaTemp()

    def decreaseSaunaTemp(self):
        self.backend.decreaseSaunaTemp()

    def currentHouseTemp(self):
        return self.backend.current_house_temp

    def currentSaunaTemp(self):
        return self.backend.current_sauna_temp

    def currentExternalTemp(self):
        return self.backend.current_external_temp
    
    def isSaunaHeatingOn(self):
        return self.backend.sauna_heating_enabled

    def isHouseHeatingOn(self):
        return self.backend.house_heating_enabled
    
    def switchHouseHeating(self):
        if self.backend.house_heating_enabled:
            self.backend.disableHouseHeating()
        else:
            self.backend.enableHouseHeating()

    def switchSaunaHeating(self):
        if self.backend.sauna_heating_enabled:
            self.backend.disableSaunaHeating()
        else:
            self.backend.enableSaunaHeating()

    def isHouseOvenOn(self):
        return self.backend.house_oven_on

    def isSaunaOvenOn(self):
        return self.backend.sauna_oven_on
