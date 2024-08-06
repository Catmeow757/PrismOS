import PySimpleGUI as gui
import webbrowser
import subprocess
import os
import sys

# Define colors
background_color = '#0000FF'  # Blue color
shut_down_button_color = ('white', '#FF0000')  # Red background with white text
other_button_color = ('white', '#00008B')  # Dark blue background with white text

# Define the main layout
layout = [
    [gui.Text('PrismOS', font=('Arial', 14), background_color=background_color, text_color='white')],
    [gui.Button('Register', button_color=other_button_color, key='Register')],
    [gui.Button('Start Menu', button_color=other_button_color, key='Start Menu')],
    [gui.Button('Programs', button_color=other_button_color, key='Programs')],
    [gui.Button('Documents', button_color=other_button_color, key='Documents')],
    [gui.Button('Control Panel', button_color=other_button_color, key='Control Panel')],
    [gui.Button('Shut Down', button_color=shut_down_button_color, key='Shut Down')]
]

# Define the Start Menu layout
start_menu_layout = [
    [gui.Text('Start Menu', font=('Arial', 14), background_color=background_color, text_color='white')],
    [gui.Button('Shut Down', button_color=shut_down_button_color, key='StartMenu_ShutDown')],
    [gui.Button('Run Program', button_color=other_button_color, key='StartMenu_RunProgram')],
    [gui.Button('Open Documents', button_color=other_button_color, key='StartMenu_OpenDocuments')],
    [gui.Button('Open Programs', button_color=other_button_color, key='StartMenu_OpenPrograms')],
    [gui.Button('Close Start Menu', button_color=other_button_color, key='StartMenu_Close')]
]

# Create the main window
window = gui.Window('PrismOS Display', [
    [gui.Frame('', layout, background_color=background_color, size=(800, 600), element_justification='center', pad=(0, 0))]
], size=(800, 600), resizable=True, finalize=True)

def run_program(program_path):
    try:
        if sys.platform == 'win32':
            subprocess.Popen([program_path], shell=True)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', program_path])
        else:
            subprocess.Popen(['bash', program_path])  # Assuming Linux
    except Exception as e:
        gui.popup(f"Failed to start program: {e}", title='Error')

# Event loop
while True:
    event, values = window.read()
    
    if event == gui.WIN_CLOSED:
        break
    elif event == 'Start Menu':
        # Create a new window for the Start Menu
        start_menu_window = gui.Window('Start Menu', start_menu_layout, modal=True, size=(300, 200))
        
        while True:
            start_menu_event, start_menu_values = start_menu_window.read()
            if start_menu_event == gui.WIN_CLOSED or start_menu_event == 'StartMenu_Close':
                start_menu_window.close()
                break
            elif start_menu_event == 'StartMenu_ShutDown':
                gui.popup("Click OK Or X To Shut Down Your Computer.", title='Notification')
                if sys.platform == 'win32':
                    os.system('shutdown /s /t 1')
                else:
                    os.system('shutdown -h now')
                quit()
            elif start_menu_event == 'StartMenu_RunProgram':
                # Ask the user for the executable path
                program_path = gui.popup_get_file('Select an executable file to run', file_types=(('Executable Files', '*.exe;*.bat;*.cmd;*.msi;*.sh;*.app;*.dmg;*.pkg;*.bin;*.run;*.com;*.out'),))
                if program_path:
                    run_program(program_path)
            elif start_menu_event == 'StartMenu_OpenDocuments':
                # Open the documents folder
                if sys.platform == 'win32':
                    documents_folder = os.path.expanduser(r'~\Documents')
                elif sys.platform == 'darwin':
                    documents_folder = os.path.expanduser('~/Documents')
                else:
                    documents_folder = os.path.expanduser('~/Documents')
                try:
                    subprocess.Popen(['explorer', documents_folder] if sys.platform == 'win32' else ['open', documents_folder])
                except Exception as e:
                    gui.popup(f"Failed to open documents folder: {e}", title='Error')
            elif start_menu_event == 'StartMenu_OpenPrograms':
                # Open a predefined folder for programs or shortcuts
                if sys.platform == 'win32':
                    programs_folder = os.path.expanduser(r'~\AppData\Local\Programs')
                elif sys.platform == 'darwin':
                    programs_folder = '/Applications'
                else:
                    programs_folder = '/usr/bin'
                try:
                    subprocess.Popen(['explorer', programs_folder] if sys.platform == 'win32' else ['open', programs_folder])
                except Exception as e:
                    gui.popup(f"Failed to open programs folder: {e}", title='Error')
    
    elif event == 'Shut Down':
        gui.popup("Click OK Or X To Shut Down Your Computer.", title='Notification')
        if sys.platform == 'win32':
            os.system('shutdown /s /t 1')
        else:
            os.system('shutdown -h now')
        quit()
    elif event == 'Register':
        webbrowser.open("https://pysimplegui.com/pricing")

# Close the main window after the event loop
window.close()
