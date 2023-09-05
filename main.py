import PySimpleGUI as sg

sg.theme('Topanga')  # Use the 'Topanga' theme for a colorful appearance

# Create frames for input and output
input_frame = [
    [sg.Text('QNX path:')],
    [sg.InputText(key='command', size=(52, ))],
    [sg.Text('Android path:')],
    [sg.InputText(key='command', size=(52, )), sg.Button('Execute')],
]

command_frame = [
    [sg.Multiline(key='log', size=(60, 10), background_color='white')],
]

output_frame = [
    [sg.Multiline(key='output', size=(60, 10), background_color='white')],
]

# Combine frames and separator in the layout
layout = [
    [sg.Frame('Input', input_frame, font=("Arial", 12))],
    [sg.HorizontalSeparator()],
    [sg.Frame('Log', command_frame, font=("Arial", 12))],
    [sg.Frame('Output', output_frame, font=("Arial", 12))],
]

window = sg.Window('Lazy Logger', layout, finalize=True)
window['command'].bind('<Return>', '_Enter')  # Bind the Return key to the Execute button

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Execute':
        command_text = values['command']
        # You can process the command here and get the output
        output_text = f'Command: {command_text}\nOutput: [Output will go here]\n'
        window['commands_output'].print(command_text)
        window['output'].print(output_text)

window.close()
