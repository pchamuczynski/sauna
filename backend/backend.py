import threading
import inspect
import time
import python_weather
import asyncio

class SaunaBackend:
    MAX_SAUNA_TEMP = 120
    MIN_SAUNA_TEMP = 40
    MAX_HOUSE_TEMP = 30
    MIN_HOUSE_TEMP = 10

    def __init__(self):
        self.lock = threading.Lock()

        self.house_oven_on = False
        self.sauna_oven_on = False

        self.sauna_temp_setting = 80
        self.house_temp_setting = 22
        self.current_house_temp = 10
        self.current_sauna_temp = 10
        self.current_external_temp = 20
        self.sauna_heating_enabled = False
        self.house_heating_enabled = False

        self.run = True
        self.temp_update_thread = threading.Thread(target=self.__updateTemp)
        self.temp_update_thread.start()

        self.oven_control_thread = threading.Thread(target=self.__ovenControl)
        self.oven_control_thread.start()

        self.event_loop = asyncio.new_event_loop()
        self.background_thread = threading.Thread(target=self.startBackgroundLoop, args=(self.event_loop,), daemon=True)
        self.background_thread.start()
        
        self.task = asyncio.run_coroutine_threadsafe(self.__getWeather(), self.event_loop)

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.__getWeather())

    def stop(self):
        self.run = False
        self.temp_update_thread.join()

    def increaseHouseTemp(self):
        with self.lock:
            self.house_temp_setting = self.__increment(
                self.house_temp_setting, self.MAX_HOUSE_TEMP)

    def decreaseHouseTemp(self):
        with self.lock:
            self.house_temp_setting = self.__decrement(
                self.house_temp_setting, self.MIN_HOUSE_TEMP)

    def increaseSaunaTemp(self):
        with self.lock:
            self.sauna_temp_setting = self.__increment(
                self.sauna_temp_setting, self.MAX_HOUSE_TEMP)

    def decreaseSaunaTemp(self):
        with self.lock:
            self.sauna_temp_setting = self.__decrement(
                self.sauna_temp_setting, self.MIN_HOUSE_TEMP)

    def currentHouseTemp(self):
        with self.lock:
            return self.current_house_temp

    def currentSaunaTemp(self):
        with self.lock:
            return self.current_sauna_temp

    def currentExternalTemp(self):
        with self.lock:
            return self.current_external_temp

    def enableSaunaHeating(self):
        with self.lock:
            self.sauna_heating_enabled = True

    def disableSaunaHeating(self):
        with self.lock:
            self.sauna_heating_enabled = False
            self.__switchSaunaOven(False)

    def enableHouseHeating(self):
        with self.lock:
            self.house_heating_enabled = True

    def disableHouseHeating(self):
        with self.lock:
            self.house_heating_enabled = False
            self.__switchHouseOven(False)

    async def __getWeather(self):
        while self.run:            
            client = python_weather.Client(format=python_weather.METRIC)
            weather = await client.find("Biały Kościół, dolnośląskie, Pl")
            print("Current weather in Biały Kościół: " + str(weather.current.temperature))
            await client.close()
            print(weather)
            print(weather.current)
            self.current_external_temp = int(weather.current.temperature)
            time.sleep(1)

    def __ovenControl(self):
        while self.run:
            if self.house_heating_enabled:
                if self.current_house_temp < self.house_temp_setting - 1:
                    self.__switchHouseOven(True)
                elif self.current_house_temp > self.house_temp_setting:
                    self.__switchHouseOven(False)
            if self.sauna_heating_enabled:
                if self.current_sauna_temp < self.sauna_temp_setting - 1:
                    self.__switchSaunaOven(True)
                else:
                    self.__switchSaunaOven(False)
            time.sleep(1)


    def __switchSaunaOven(self, new_state):
        if self.sauna_oven_on != new_state:
            print('switching sauna oven to ' + str(new_state))
            self.sauna_oven_on = new_state

    def __switchHouseOven(self, new_state):
        if self.house_oven_on != new_state:
            print('switching house oven to ' + str(new_state))
            self.house_oven_on = new_state

    def __updateTemp(self):
        while self.run:
            with self.lock:
                if self.house_oven_on:
                    if self.current_house_temp < self.MAX_HOUSE_TEMP:
                        self.current_house_temp += 1
                elif self.current_house_temp > self.current_external_temp:
                    self.current_house_temp -= 1
                elif self.current_house_temp < self.current_external_temp:
                    self.current_house_temp += 1

                if self.sauna_oven_on:
                    if self.current_sauna_temp < self.MAX_SAUNA_TEMP:
                        self.current_sauna_temp += 1
                elif self.current_sauna_temp > self.current_house_temp:
                    self.current_sauna_temp -= 1
                elif self.current_sauna_temp < self.current_house_temp:
                    self.current_sauna_temp += 1                   
                
            time.sleep(1)

    def __increment(self, var, max):
        return var if var == max else var + 1

    def __decrement(self, var, min):
        return var if var == min else var - 1
    
    def startBackgroundLoop(self, loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
