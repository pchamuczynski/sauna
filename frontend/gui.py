#!/usr/bin/python3

from tkinter import Scale
from tkinter.constants import N
import PySimpleGUI as sg
from datetime import datetime
import time
import threading

from PySimpleGUI.PySimpleGUI import VStretch

# BACKGROUND_COLOR='black'
DEGREE_SIGN = u'\N{DEGREE SIGN}'

class TempControl(sg.Column):
    def __init__(self, title, is_heating_enabled):
        self.title = title
        self.isHeatingEnabled = is_heating_enabled
        self.button_color = sg.theme_background_color()
        self.on_off_button = sg.Button(key = title + ".On",
            image_filename=self.onOffButtonImage(),
            border_width=0,
            button_color=(self.button_color, self.button_color))
        self.timer_button = sg.Button(key = title + ".Timer",
            image_filename='resources/clock_40x40.png',
            border_width=0,
            button_color=(self.button_color, self.button_color)
        )

        self.layout=[
            [self.on_off_button, self.timer_button]
        ]
        sg.Column.__init__(self,self.layout)
    
    def update(self):
        self.on_off_button.update(image_filename=self.onOffButtonImage())
            
    def onOffButtonImage(self):
        if self.isHeatingEnabled():
            return 'resources/on_off_red_40x40.png'
        else:
            return 'resources/on_off_black_40x40.png'


class SetupTempColumn(sg.Column):    
    def __init__(self, title, image, get_temp_setting, get_heating_enabled):
        self.button_color=sg.theme_background_color()
        self.title = title
        self.image = image
        self.getTempSetting = get_temp_setting
        self.up_button = sg.Button(key = self.title + ".Up", image_filename='resources/triangle_up_60x60.png',
                                   border_width=0, button_color=(self.button_color, self.button_color))
        self.temp_display = sg.Text(str(self.getCurrentTemp()) + DEGREE_SIGN, font='Comic 30')
        self.down_button = sg.Button(key=self.title + ".Down", image_filename='resources/triangle_down_60x60.png',
                                     border_width=0, button_color=(self.button_color, self.button_color))
        self.temp_control = TempControl(title, get_heating_enabled)
        

        self.layout = [
            [sg.Image(self.image)],
            [sg.VStretch()],
            [self.up_button],
            [self.temp_display],
            [self.down_button],
            [self.temp_control],
            [sg.VStretch()],
        ]
        sg.Column.__init__(self, self.layout, element_justification='c',expand_y=True)

    def getCurrentTemp(self):
        return self.getTempSetting()
    
    def update(self):
        self.temp_display.update(str(self.getCurrentTemp()) + DEGREE_SIGN)
        self.temp_control.update()

class SetupColumn(sg.Column):
    def __init__(self, width, api):
        self.width_fill = sg.Text(' '*width, font='Any 2', pad=(0, 0))
        self.home_temp_column = SetupTempColumn("House", 'resources/home_60x60.png', 
                                                api.getHouseTempSetting, api.isHouseHeatingOn)
        self.sauna_temp_column = SetupTempColumn("Sauna", 'resources/sauna_60x60.png', 
                                                 api.getSaunaTempSetting, api.isSaunaHeatingOn)
        self.layout = [
            [self.width_fill],
            [sg.Text('Ustawienia temperatury', font='Comic 16', justification='c')],
            [sg.Stretch(),self.home_temp_column,sg.Stretch(),self.sauna_temp_column,sg.Stretch()],
        ]
        sg.Column.__init__(self, 
                           self.layout, 
                           expand_x=True, expand_y=True,
                           element_justification='c')
        
    def update(self):
        self.home_temp_column.update()
        self.sauna_temp_column.update()
        
class Clock(sg.Column):
    def __init__(self):
        self.date_text = sg.Text('', font='Comic 16')
        self.time_text = sg.Text('', font='Comic 24')
        self.layout = [
            [self.date_text],
            [self.time_text]
        ]
        sg.Column.__init__(self,self.layout,element_justification='c')
    
    def update(self):
        now = datetime.now()
        self.date_text.update(value=now.strftime('%A %Y-%m-%d'))
        self.time_text.update(value=now.strftime('%H:%M:%S'))

class Thermometer(sg.Column):
    def __init__(self, image, temp_source, oven_on_source, title):
        self.title = title
        self.image = image
        self.temp_source = temp_source
        self.temp_text = sg.Text('', font='Comic 24', size=3)
        self.image_element = sg.Image(image)
        self.isOvenOn = oven_on_source
        self.heating_image = sg.Image(size=(40,40))

        self.layout=[[self.image_element, self.temp_text, self.heating_image]]

        sg.Column.__init__(self,self.layout)
    
    def update(self):
        self.temp_text.update(value=str(self.__readTemperature()) + DEGREE_SIGN)
        self.heating_image.update(filename=self.__heatingImageFilename())

    def __readTemperature(self):
        print(self.title + " temp = " + str(self.temp_source()))
        return str(self.temp_source())
    
    def __heatingImageFilename(self):
        if self.isOvenOn():
            return 'resources/heating_40x40.png'
        else:
            return None

class StatusColumn(sg.Column):
    def __init__(self, width, api):
        now = datetime.now()
        self.width_fill = sg.Text(' '*width, font='Any 2', pad=(0, 0))
        self.clock=Clock()
        self.home_thermo = Thermometer('resources/home_60x60.png', api.currentHouseTemp, api.isHouseOvenOn, "Home")
        self.outside_thermo = Thermometer('resources/sun_60x60.png', api.currentExternalTemp, lambda: False, "External")
        self.sauna_thermo = Thermometer('resources/sauna_60x60.png', api.currentSaunaTemp, api.isSaunaOvenOn, "Sauna")

        self.layout = [
            [self.width_fill],
            [self.clock],
            [VStretch()],
            [sg.Text('Temp. teraz', font='Comic, 18')],
            [self.outside_thermo],
            [self.home_thermo],
            [self.sauna_thermo],
            [sg.Button('Cancel')]
        ]

        sg.Column.__init__(self, self.layout,
                          expand_x=True, expand_y=True,
                          element_justification='c')
    def update(self):
        self.clock.update()
        self.home_thermo.update()
        self.outside_thermo.update()
        self.sauna_thermo.update()


class GUI:   
    def __init__(self, api):     
        self.setup_width = 500
        self.status_width = 300
        self.hight = 500

        self.setup_column = SetupColumn(self.setup_width, api)
        self.status_column = StatusColumn(self.status_width, api)
        self.layout = [[self.setup_column, sg.VSep(), self.status_column]]

        self.window = sg.Window('Temp Control', self.layout, finalize=True,
                                grab_anywhere=True,
                                use_default_focus=False, no_titlebar=True,
                                # alpha_channel=.8, 
                                element_justification='c',
                                size=(self.setup_width+self.status_width,self.hight))
        self.status_column.expand(expand_x=True,expand_y=True)
        self.run = True
        self.api = api
        
        self.update_display_thread = threading.Thread(target=self.updateDisplayThread)
        self.update_display_thread.start()

    def dispose(self):
        self.update_display_thread.join()
        self.api.stop()
        
    def updateDisplayThread(self):
        while self.run:
            self.status_column.update()
            time.sleep(1)
            
    def eventListenerLoop(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                self.run = False
                break
            if event == "House.On":
                self.api.switchHouseHeating()
                self.setup_column.update()
            if event == "House.Up":
                self.api.increaseHouseTemp()
                self.setup_column.update()
            if event == "House.Down":
                self.api.decreaseHouseTemp()
                self.setup_column.update()
            if event == "Sauna.On":
                self.api.switchSaunaHeating()
                self.setup_column.update()
            if event == "Sauna.Up":
                self.api.increaseSaunaTemp()
                self.setup_column.update()
            if event == "Sauna.Down":
                self.api.decreaseSaunaTemp()
                self.setup_column.update()
            # break

   
