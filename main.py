import os
import shutil
import tkinter
from tkinter import messagebox, filedialog, font
from tkinter.ttk import Progressbar, Button
from tooltip import CreateToolTip
from functools import partial

runningpath = os.path.dirname(__file__)
appdata = os.environ['LOCALAPPDATA']

if os.path.isdir(f'{appdata}\\Roblox'):
    print('Roblox directory in AppData installed: continuing.')
else:
    tkinter.messagebox.showerror("Roblox directory in AppData directory does not seem to exist. Program halted.")
    exit()

if os.path.isdir(f'{appdata}\\Roblox\\Versions'):
    print('Roblox versions directory seem to exist: checking if they actually have crap in them.')
    rblxversions = [f.path for f in os.scandir(f'{appdata}\\Roblox\\Versions') if f.is_dir()]
    if not rblxversions:
        tkinter.messagebox.showerror("There seem to be no currently installed Roblox versions, "
                                     "therefore making it very unlikely any Roblox versions are currently installed. "
                                     "Program halted.")
        exit()
else:
    tkinter.messagebox.showerror("Roblox versions directory doesn't seem to exist, "
                                 "therefore making it very unlikely any Roblox versions are currently installed. "
                                 "Program halted.")

for x in rblxversions:
    if os.path.isfile(f'{x}\\RobloxPlayerBeta.exe'):
        print(f"I found the Roblox engine player directory! {x}")
        rblxclient = x
    elif os.path.isfile(f'{x}\\RobloxStudioBeta.exe'):
        print(f"I found the Roblox engine studio directory! {x}")
        rblxstudio = x

try:
    rblxclient
except NameError:
    tkinter.messagebox.showerror("I couldn't find any Roblox versions that contain the Roblox engine player. Program halted.")

rblxsounds = f'{rblxclient}\\content\\sounds'
if not os.path.isdir(rblxsounds):
    tkinter.messagebox.showerror("Umm... That's odd, I couldn't find the directory where the sounds are stored.. Program halted, I guess?")

# Whoo! We made it to the sound files!
expected_sounds = {
    "uuhhh": f'{rblxsounds}\\uuhhh.mp3',
    "snap": f'{rblxsounds}\\snap.mp3',
    "impact_water": f'{rblxsounds}\\impact_water.mp3',
    "impact_explosion_03": f'{rblxsounds}\\impact_explosion_03.mp3',
    "action_swim": f'{rblxsounds}\\action_swim.mp3',
    "action_jump_land": f'{rblxsounds}\\action_jump_land.mp3',
    "action_jump": f'{rblxsounds}\\action_jump.mp3',
    "action_get_up": f'{rblxsounds}\\action_get_up.mp3',
    "action_footsteps_plastic": f'{rblxsounds}\\action_footsteps_plastic.mp3',
    "action_falling": f'{rblxsounds}\\action_falling.mp3'
}
expected_backups = {
    "uuhhh": f'{rblxsounds}\\uuhhh.mp3.bak',
    "snap": f'{rblxsounds}\\snap.mp3.bak',
    "impact_water": f'{rblxsounds}\\impact_water.mp3.bak',
    "impact_explosion_03": f'{rblxsounds}\\impact_explosion_03.mp3.bak',
    "action_swim": f'{rblxsounds}\\action_swim.mp3.bak',
    "action_jump_land": f'{rblxsounds}\\action_jump_land.mp3.bak',
    "action_jump": f'{rblxsounds}\\action_jump.mp3.bak',
    "action_get_up": f'{rblxsounds}\\action_get_up.mp3.bak',
    "action_footsteps_plastic": f'{rblxsounds}\\action_footsteps_plastic.mp3.bak',
    "action_falling": f'{rblxsounds}\\action_falling.mp3.bak'
}
sounds = {}
replacable_sounds = {}

for key, value in expected_sounds.items():
    if os.path.isfile(value):
        sounds[key] = value

GuiWindow = tkinter.Tk()
GuiWindow.title('Roblox Sound Replacer')
GuiWindow.resizable(False, False)

fontlist = tkinter.font.families()
if "Segoe UI" in fontlist:
    fontuse = 'Segoe UI'
    print("Using Segoe UI font, as it is installed.")
else:
    fontuse = 'Arial'
    print("Using Arial font, as Segoe UI is not installed.")
labelRow = 0

sounds_info = {
    "uuhhh": "The Roblox death sound file.",
    "snap": "i dont think this sound is used ingame",
    "impact_water": "The sound used for landing in water.",
    "impact_explosion_03": "This is an explosion sound. It *might* be used in a few games.",
    "action_swim": "The sound used for swimming.",
    "action_jump_land": "The sound used for landing.",
    "action_jump": "The sound used for jumping.",
    "action_get_up": "The (rarely used) sound used when the character gets up.",
    "action_footsteps_plastic": "The sound used for walking on Plastic material.",
    "action_falling": "The sound used for falling.",
    "bass": "i dont know and its also not an mp3 file so im not gonna touch that"
}
sounds_textboxes = {}
sounds_browsers = {}


def browsefiles(keyparam):
    filename = filedialog.askopenfilename(initialdir=runningpath,
                                          title="Select a File",
                                          filetypes=(("*.mp3 files",
                                                      "*.mp3*"),
                                                     ("all files",
                                                      "*.*")))
    sounds_textboxes[keyparam].insert(0, filename)


for key, value in sounds.items():
    labelRow = labelRow + 1
    currentLabel = tkinter.Label(GuiWindow, text=key, font=(fontuse, 12))
    currentLabel.grid(column=1, row=labelRow)
    CreateToolTip(currentLabel, sounds_info[key])
    labelRow = labelRow + 1
    currentTextbox = tkinter.ttk.Entry(GuiWindow)
    sounds_textboxes[key] = currentTextbox
    currentTextbox.grid(column=1, row=labelRow, sticky='ew')
    labelRow = labelRow + 1
    button_explore = Button(GuiWindow,
                            text="Browse files",
                            command=partial(browsefiles, key))
    button_explore.grid(column=1, row=labelRow, sticky='ew')
    labelRow = labelRow + 1
    tkinter.ttk.Separator(GuiWindow).grid(column=1, row=labelRow, sticky='ew', pady=5)

for key, value in expected_sounds.items():
    if os.path.isfile(f'{runningpath}\\{key}.mp3'):
        replacable_sounds[key] = f'{runningpath}\\{key}.mp3'
        try:
            sounds_textboxes[key].insert(0, f'{runningpath}\\{key}.mp3')
        except KeyError:
            pass


def soundreplace():
    for xkey, y in sounds_textboxes.items():
        currentvaluetext = y.get()
        if not currentvaluetext == '':
            replacable_sounds[xkey] = currentvaluetext
    GuiButton['state'] = 'disabled'
    progressleap = 100 / len(replacable_sounds.values())
    for xkey, y in replacable_sounds.items():
        if xkey in sounds:
            shutil.move(sounds[xkey], f'{sounds[xkey]}.bak')
            try:
                shutil.copyfile(y, sounds[xkey])
            except FileNotFoundError:
                tkinter.messagebox.showerror('File not found',
                                             f'File {y} is missing and therefore could not be copied. '
                                             f'Action cancelled.')
                GuiButton['state'] = 'normal'
                progress['value'] = 0
                return
            progress['value'] = progress['value'] + progressleap
    if progress['value'] == 100:
        GuiButton['state'] = 'normal'
        tkinter.messagebox.showinfo('Success', 'All sound files have been replaced!')
        progress['value'] = 0


def soundrevert():
    GuiRevertButton['state'] = 'disabled'
    progressleap = 100 / len(expected_backups.values())
    for xkey, y in expected_backups.items():
        progress['value'] = progress['value'] + progressleap
        if os.path.isfile(y):
            try:
                os.remove(expected_sounds[xkey])
            except FileNotFoundError:
                pass  # File does not exist.
            os.rename(y, expected_sounds[xkey])
        if progress['value'] == 100:
            GuiRevertButton['state'] = 'normal'
            tkinter.messagebox.showinfo('Success', 'All sound files have been reverted!')
            progress['value'] = 0


GuiButton = tkinter.ttk.Button(GuiWindow, text='Replace', command=soundreplace)
GuiButton.grid(column=1, row=labelRow + 2)
CreateToolTip(GuiButton, 'Replaces sound files accordingly.')
GuiRevertButton = tkinter.ttk.Button(GuiWindow, text='Revert', command=soundrevert)
GuiRevertButton.grid(column=1, row=labelRow + 3)
CreateToolTip(GuiRevertButton, 'Reverts any changes to sound files accordingly.')
progress = Progressbar(GuiWindow, orient='horizontal',
                       length=400, mode='determinate')
progress.grid(column=1, row=labelRow + 4, pady=5)

print('Launching Tk window')
GuiWindow.mainloop()
