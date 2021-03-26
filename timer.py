from sys import version_info

if version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
from time import time

# ----------------  Create Form  ----------------
sg.ChangeLookAndFeel('Black')
sg.SetOptions(element_padding=(0, 0))

layout = [[sg.Text('')],
         [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='time')],
         [sg.Button('Run', key='Run/Pause', button_color=('white', '#001480')),
          sg.Button('Reset', key='Reset/Record', button_color=('white', '#007339')),
          sg.Exit(button_color=('white', 'firebrick4'), key='Exit')],
         [sg.Text('', size=(20, 0), font=('Helvetica', 10), justification='left', key='text')]]

window = sg.Window('Running Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True, alpha_channel=.8)

# ----------------  main loop  ----------------
current_time = 0
paused = True
start_time = int(round(time() * 100))
paused_time = int(round(time() * 100))
record = ''
record_n = 0
while (True):
    # --------- Read and update window --------
    if paused:
        event, values = window.read()
    else:
        event, values = window.read(timeout=10)
        current_time = int(round(time() * 100)) - start_time
    if event == 'Run/Pause' or event == 'Reset/Record':
        event = window[event].GetText()
    # --------- Do Button Operations --------
    if event == sg.WIN_CLOSED or event == 'Exit':        # ALWAYS give a way out of program
        break
    if event == 'Record':
        record_n += 1
        record += '{:02d}    {:02d}:{:02d}.{:02d}\n'.format(record_n, (current_time // 100) // 60,(current_time // 100) % 60, current_time % 100)
        # print(record)
        if record_n % 2 == 0:
            window['text'].color
        window['text'].update(record)
        window['text'].set_size((None,record_n))
    elif event is 'Reset':
        start_time = int(round(time() * 100))
        current_time = 0
        paused_time = start_time
        window['text'].update('')
        window['text'].set_size((None,0))
        record = ''
        record_n = 0
    elif event == 'Pause':
        paused = True
        paused_time = int(round(time() * 100))
        window['Run/Pause'].update(text='Run')
        window['Reset/Record'].update(text='Reset')
    elif event == 'Run':
        paused = False
        start_time = start_time + int(round(time() * 100)) - paused_time
        window['Run/Pause'].update(text='Pause')
        window['Reset/Record'].update(text='Record')

    # --------- Display timer in window --------
    window['time'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60, (current_time // 100) % 60, current_time % 100))