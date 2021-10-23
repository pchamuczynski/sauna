#!/usr/bin/python3

import threading
from tkinter import Scale
from tkinter.constants import N
import PySimpleGUI as sg
from datetime import datetime
import time

from PySimpleGUI.PySimpleGUI import VStretch

class SetupColumn(sg.Column):
    def __init__(self, width):
        self.width_fill = sg.Text(' '*width, font='Any 2', pad=(0, 0))
        self.layout = [
            [self.width_fill],
            [sg.VStretch()],
            [sg.Text("Dupa", expand_y=True)],
            [sg.VStretch()]
        ]
        sg.Column.__init__(self, 
                          self.layout, 
                          expand_x=True, expand_y=True,
                          element_justification='c')
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
    degree_sign = u'\N{DEGREE SIGN}'

    def __init__(self, image, temp_source):
        self.image = image
        self.temp_source = temp_source
        self.temp_text = sg.Text('', font='Comic 24')
        self.image_element = sg.Image(image)

        self.layout=[[self.image_element, self.temp_text]]

        sg.Column.__init__(self,self.layout)
    
    def update(self):
        self.temp_text.update(value=self.readTemperature())

    def readTemperature(self):
        return str(self.temp_source) + self.degree_sign


class StatusColumn(sg.Column):
    def __init__(self, width):
        now = datetime.now()
        self.width_fill = sg.Text(' '*width, font='Any 2', pad=(0, 0))
        self.clock=Clock()
        self.home_thermo = Thermometer('resources/home_60x60.png', 19)
        self.outside_thermo = Thermometer('resources/sun_60x60.png', -3)
        self.sauna_thermo = Thermometer('resources/sauna_60x60.png', 84)

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

    def __init__(self):     
        self.setup_column = SetupColumn(700)
        self.status_column = StatusColumn(300)
        self.layout = [[self.setup_column, sg.VSep(), self.status_column]]

        self.window = sg.Window('Window Title', self.layout, finalize=True,
                                background_color='black', grab_anywhere=True,
                                use_default_focus=False, no_titlebar=True,
                                alpha_channel=.8, element_justification='c',
                                size=(1000,700))
        self.status_column.expand(expand_x=True,expand_y=True)
        self.run = True

    def updateDisplayThread(self):
        while self.run:
            self.status_column.update()
            print('StatusColumn.update')
            time.sleep(1)
   

def main():
    print('cycki')
    gui = GUI()
    thread = threading.Thread(target=gui.updateDisplayThread)
    thread.start()
    print('Main thread')
    while True:
        event, values = gui.window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            gui.run = False
            thread.join()
            break
        break

if __name__ == '__main__':
    main()

###
# # Create the Window

# setup_layout = [
#                     [sg.Text(' '*700, font='Any 2',pad=(0,0))],
#                     [sg.Stretch(),sg.Text("Setup"), sg.Text('dupa'), sg.Stretch()]
#                ]
# status_layout = [
#                     [sg.Text(' '*300, font='Any 2', pad=(0, 0))],
#                     [sg.Stretch(), sg.Text("Status"), sg.Text('dupa'), sg.Stretch()]
# ]

# layout = [[sg.Column(layout=setup_layout, element_justification='c'), sg.Column(layout=status_layout, element_justification='c')]]

# window = sg.Window('Window Title', layout, finalize=True,
#                    background_color='black', grab_anywhere=True,
#                    use_default_focus=False, no_titlebar=True,
#                    alpha_channel=.8, element_justification='c')
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
#         break
#     break

# window.close()

###


# sg.theme('DarkAmber')   # Add a touch of color
# sg.set_options(border_width=1, text_color='white',
#                background_color='blue', 
#                text_element_background_color='brown')

# now = datetime.now()

# home_setup_column_layout = []

# sauna_setup_column_layout = []

# setup_frame_layout = [
#     [sg.Stretch(), sg.Text(text='Zadana temperatura', expand_x=True, expand_y=True, justification='c'), sg.Stretch()],
    
# ]   

# setup_frame = sg.Frame(title='', layout=setup_frame_layout, 
#                          border_width=0,
#                          element_justification='center', 
#                          size=(0,600),
#                          expand_x=True, expand_y=True, 
#                          pad=(0, 0),
#                          background_color='black')

# setup_column = sg.Column(layout=[[setup_frame]],
#                          size=(0, 600),
#                          expand_x=True, expand_y=True,
#                          pad=(0, 0),
#                          background_color='green'
#                          )

# status_column_layout = [
#     [sg.Text(text=now.strftime('%A %Y-%m-%d'), justification='c', expand_x=True, expand_y=False, font='Arial 24 bold')],
#     [sg.Text(text=now.strftime('%H:%M:%S'), justification='c', expand_x=True, expand_y=False, font='Arial 30 bold')],
#     [sg.Button('Cancel')]
# ]
# status_column = sg.Column(layout=status_column_layout, 
#                           size=(324, 600), 
#                         #   element_justification='right', 
#                         #   expand_x=True, expand_y=True,
#                           background_color='black',
#                           visible=True)

# # All the stuff inside your window.
# layout = [
#     [sg.Stretch(), setup_column, sg.Stretch(), status_column]
# ]
# # layout = [[setup_column, sg.VerticalSeparator(), status_column]]

# # Create the Window
# window = sg.Window('Window Title', layout, finalize=True,
#                    background_color='black', grab_anywhere=True,
#                    use_default_focus=False, no_titlebar=True,
#                    alpha_channel=.8, element_justification='c')
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
#         break
#     break

# window.close()


# # # # All the stuff inside your window.
# # # layout = [[sg.Text('Zadana temperatura'), sg.Text(date.today())],
# # #           [sg.Text('Enter something on Row 2'), sg.InputText()],
# # #           [sg.Button('Ok'), sg.Button('Cancel')]]

# # # # Create the Window
# # # window = sg.Window('Window Title', layout)
# # # # Event Loop to process "events" and get the "values" of the inputs
# # # while True:
# # #     event, values = window.read()
# # #     if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
# # #         break
# # #     print('You entered ', values[0])

# # # window.close()


