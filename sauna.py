#!/usr/bin/python3

import PySimpleGUI as sg
from datetime import datetime

sg.theme('DarkAmber')   # Add a touch of color
sg.set_options(border_width=1, text_color='white',
               background_color='blue', 
               text_element_background_color='brown')

now = datetime.now()

home_setup_column_layout = []

sauna_setup_column_layout = []

setup_frame_layout = [
    [sg.Stretch(), sg.Text(text='Zadana temperatura', expand_x=True, expand_y=True, justification='c'), sg.Stretch()],
    
]   

setup_frame = sg.Frame(title='', layout=setup_frame_layout, 
                         border_width=0,
                        #  element_justification='center', 
                         size=(700,600),
                         expand_x=True, expand_y=True, 
                         pad=(0, 0),
                         background_color='black')

setup_column = sg.Column(layout=[[setup_frame]],
                         size=(700, 600),
                         expand_x=True, expand_y=True,
                         pad=(0, 0),
                         background_color='green'
                         )

status_column_layout = [
    [sg.Text(text=now.strftime('%A %Y-%m-%d'), justification='c', expand_x=True, expand_y=False, font='Arial 24 bold')],
    [sg.Text(text=now.strftime('%H:%M:%S'), justification='c', expand_x=True, expand_y=False, font='Arial 30 bold')],
    [sg.Button('Cancel')]
]
status_column = sg.Column(layout=status_column_layout, 
                          size=(324, 600), 
                        #   element_justification='right', 
                        #   expand_x=True, expand_y=True,
                          background_color='black',
                          visible=True)

# All the stuff inside your window.
layout = [
    [sg.Stretch(), setup_column, sg.Stretch(), status_column]
]
# layout = [[setup_column, sg.VerticalSeparator(), status_column]]

# Create the Window
window = sg.Window('Window Title', layout, finalize=True,
                   background_color='black', grab_anywhere=True,
                   use_default_focus=False, no_titlebar=True,
                   alpha_channel=.8, element_justification='c')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    break

window.close()


# # All the stuff inside your window.
# layout = [[sg.Text('Zadana temperatura'), sg.Text(date.today())],
#           [sg.Text('Enter something on Row 2'), sg.InputText()],
#           [sg.Button('Ok'), sg.Button('Cancel')]]

# # Create the Window
# window = sg.Window('Window Title', layout)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
#         break
#     print('You entered ', values[0])

# window.close()


