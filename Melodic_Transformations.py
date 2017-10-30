"""
" Author: Daniel Pitherin
" Version: 1.0
" Last Updated: 10/29/2017
" Functionality: This program takes a sequence of note names from the user, converts the sequence to pitches, generates
"                new pitch sequences based off three types of melodic transformations (inversion, retrograde, and
"                inverse retrograde) based on the user's selection, then translates each pitch sequence to a sequence of
"                note names and outputs that final sequence
" Planned Updates:
" - Implementing audio playback
" - Tweaking note-name conversion function to handle less-standard pitch sequences correctly
"""

from tkinter import *

root = Tk()
root.title("Melodic Transformations Generator") # Let's make a GUI!



def about(): # Generates a pop-up window with general information about the program
    about_window = Toplevel()
    about_window.wm_title("About")
    message = Message(about_window, text="v. 1.0\n\nProgram for transforming melodic sequences in various ways",
                      justify="center")
    message.grid(column=0, row=0)
    button = Button(about_window, text="Ok", command=about_window.destroy)
    button.grid(column=0, row=1)

def how_to_use(): # Generates a pop-up window with information about how to use the program
    use_window = Toplevel()
    use_window.wm_title("About")
    message = Message(use_window, text="This program takes in any combination of single-accidental note names and will "
                                       "display the inversion, retrograde, and inverse retrograde selected as note-name"
                                       " sequences. For more information regarding available transformations, please "
                                       "explore the help menu.\n\nSample input: C# D Eb", justify="center")
    message.grid(column=0, row=0)
    button = Button(use_window, text="Ok", command=use_window.destroy)
    button.grid(column=0, row=1)

def define(definition): # Generates a pop-up window with definitions for each melodic transformation based on selection
    def_window = Toplevel()
    def_window.wm_title("Definition: %s" % definition)
    if definition == "I":
        message = Message(def_window, text="An inversion takes the original melody and moves all intervals in the "
                                           "opposite direction, based on a selected inversion point.\n\nExample: C D E "
                                           "becomes C Bb Ab when inverted around C", justify="center")

    elif definition == "R":
        message = Message(def_window, text="A retrograde takes the original melody and plays it back in reverse order. "
                                           "\n\nExample: C D E becomes E D C", justify="center")

    else:
        message = Message(def_window, text="An inverse retrograde takes the original melody, reverses the direction of "
                                           "all intervals based on a selected inversion point, and then plays it back "
                                           "in reverse order.\n\nExample: C D E becomes Ab Bb C when inverted around C",
                          justify="center")

    message.grid(column=0, row=0)
    button = Button(def_window, text="Ok", command=def_window.destroy)
    button.grid(column=0, row=1)

# Checks if either Inversion or Inverse Retrograde have been selected without choosing an inversion point, disabling
# Transformation button if that is the case
def inversion_point_check():
    if (inversion_on.get() == 1 or inverse_retro_on.get() == 1) and inversion_point.get() == "Inversion Point":
        button_transform.configure(state="disabled")
    else:
        button_transform.configure(state="normal")

def transform_click(): # Initiate transformation. Autobots, roll out!
    user_input = str(original.get())
    if user_input == "":
        original.set("Try writing some notes!")
        return
    original_name_sequence = remove_junk_characters(user_input)
    try:
        sequence = [str(s) for s in original_name_sequence.split(' ')]
    except ValueError:
        how_to_use()
        return
    pitch_sequence = translate_name_to_pitch(sequence)
    standardize(pitch_sequence)
    original.set(translate_pitch_to_name(pitch_sequence))
    if inversion_on.get() == 1:
        inversion.set(translate_pitch_to_name(inverse(pitch_sequence, inversion_to_pitch[inversion_point.get()])))
    if retro_on.get() == 1:
        retro.set(translate_pitch_to_name(retrograde(pitch_sequence)))
    if inverse_retro_on.get() == 1:
        inverse_retro.set(translate_pitch_to_name(inverse_retrorade(pitch_sequence, inversion_to_pitch[inversion_point.get()])))

inversion_to_pitch = {'C/B#': 0, 'C#/Db': 1, 'D': 2, 'Eb/D#': 3, 'E/Fb': 4, 'F/E#': 5, 'F#/Gb': 6, 'G': 7, 'Ab/G#': 8,
                      'A': 9, 'Bb/A#': 10, 'B/Cb': 11}

name_to_pitch = {'C': 0, 'B#': 0,
                 'C#': 1, 'Db': 1,
                 'D': 2,
                 'Eb': 3, 'D#': 3,
                 'E': 4, 'Fb': 4,
                 'F': 5, 'E#': 5,
                 'F#': 6, 'Gb': 6,
                 'G': 7,
                 'Ab': 8, 'G#': 8,
                 'A': 9,
                 'Bb': 10, 'A#': 10,
                 'B': 11, 'Cb': 11}


def remove_junk_characters(mess_string): # Removes any characters not defined as musical characters
    cleansed_string = ''
    i = 0
    while i < len(mess_string):
        if is_musical_character(mess_string[i]):
            cleansed_string = cleansed_string + mess_string[i]
        i = i + 1
    return cleansed_string

def is_musical_character(questionable_character): # Checks if a single character is in the list of musical characters
    i = 0
    while i < len(musical_characters):
        if questionable_character == musical_characters[i]:
            return True
        i = i + 1
    return False

musical_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', '#', 'b', ' ']

def translate_name_to_pitch(sequence): # Translates note name sequence to pitch sequence
    i = 0
    pitch_sequence = []
    try:
        while i < len(sequence):
            name = sequence[i]
            pitch_sequence.append(name_to_pitch[name])
            i = i + 1
    except KeyError:
        how_to_use()
        return
    return pitch_sequence


default_name = ('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B')


def is_present(array, n): # Checks if an item n is present in parameter array
    for i in array:
        if i == n:
            return True
    return False


def translate_pitch_to_name(pitch_sequence): # Translates pitch sequence to note name sequence
    name_sequence = []
    for n in pitch_sequence:
        name_sequence.append(default_name[n])
    length = len(name_sequence)

    i = 0
    while i < length:
        pitch = pitch_sequence[i]
        if pitch == 1 and (is_present(pitch_sequence, 0) or is_present(pitch_sequence, 5)) and not is_present(pitch_sequence, 2):
            name_sequence[i] = 'Db'
        if pitch == 6 and is_present(pitch_sequence, 5) and not is_present(pitch_sequence, 9) and not is_present(pitch_sequence, 7):
            name_sequence[i] = 'Gb'
        i = i + 1

    i = 0
    while i < length:
        pitch = pitch_sequence[i]
        if pitch == 0 and is_present(name_sequence, 'C#') and not is_present(pitch_sequence, 11):
            name_sequence[i] = 'B#'
        if pitch == 3 and (is_present(name_sequence, 'C#') or is_present(pitch_sequence, 4)) and not is_present(pitch_sequence,
                                                                                                       2):
            name_sequence[i] = 'D#'
        if pitch == 5 and is_present(name_sequence, 'F#') and not is_present(pitch_sequence, 4):
            name_sequence[i] = 'E#'
        if pitch == 8 and (is_present(name_sequence, 'F#') or is_present(pitch_sequence, 9)) and not is_present(pitch_sequence,
                                                                                                       7):
            name_sequence[i] = 'G#'
        i = i + 1

    i = 0
    while i < length:
        pitch = pitch_sequence[i]
        if pitch == 4 and is_present(name_sequence, 'Eb') and not is_present(pitch_sequence, 5):
            name_sequence[i] = 'Fb'
        if pitch == 10 and (is_present(name_sequence, 'G#') or is_present(pitch_sequence, 11)) and \
                not (is_present(pitch_sequence, 9) or is_present(name_sequence, 'Ab')):
            name_sequence[i] = 'A#'
        i = i + 1

    i = 0
    while i < length:
        pitch = pitch_sequence[i]
        if pitch == 11 and is_present(name_sequence, 'Bb') and not is_present(pitch_sequence, 0):
            name_sequence[i] = 'Cb'
        i = i + 1
    return name_sequence

def standardize(mess): # Translates all pitches in sequence to be within range of 0-11
    i = 0
    while i < len(mess):
        if mess[i] > 11:
            mess[i] = mess[i] % 12
        elif mess[i] < 0:
            mess[i] = mess[i] % 12
        i = i + 1
    return mess

def inverse(sequence, point): # Returns the parameter pitch sequence inverted around parameter pitch point
    i = 0
    length = len(sequence)
    inversion = []
    while i < length:
        inversion.append(2 * point - sequence[i])
        i = i + 1
    standardize(inversion)
    return inversion

def retrograde(sequence): # Returns the parameter pitch sequence in reverse
    i = 0
    length = len(sequence)
    retrograde = []
    while i < length:
        retrograde.append(sequence[length - 1 - i])
        i = i + 1
    return retrograde

# Returns the parameter pitch sequence inverted around paramter pitch point, then reversed
def inverse_retrorade(sequence, point):
    return retrograde(inverse(sequence, point))

def reset_click(): # Clears all fields and resets inversion point drop-down menu
    inversion_point.set("Inversion Point")
    original.set("")
    inversion.set("")
    retro.set("")
    inverse_retro.set("")
    inversion_on.set(0)
    retro_on.set(0)
    inverse_retro_on.set(0)
    entry_original.focus_set()


# Menu
menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="About", command=about)
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="How to Use", command=how_to_use)
menubar.add_cascade(label="Help", menu=helpmenu)

definitionsmenu = Menu(helpmenu, tearoff=1)
definitionsmenu.add_command(label="Inversion", command=lambda: define("I"))
definitionsmenu.add_command(label="Retrograde", command=lambda: define("R"))
definitionsmenu.add_command(label="Inverse Retrograde", command=lambda: define("IR"))
helpmenu.add_cascade(label="Definitions", menu=definitionsmenu)

root.config(menu=menubar)

# Row 0
frame1 = Frame(height=10).grid(column=0, row=0)

frame2 = Frame(height=1, width=10).grid(column=0, row=1)

label_original = Label(root, text="Original: ").grid(column=2, row=1, sticky='E')

original = StringVar()
entry_original = Entry(root, textvariable=original)
entry_original.grid(column=3, row=1, sticky='W')
entry_original.focus_set()


frame3 = Frame(height=1, width=10).grid(column=4, row=1)

# button_original = Button(root, text=u"Playback", command=OnButtonClick).grid(column=5, row=1)

# frame4 = Frame(height=1, width=10).grid(column=6, row=1)

OPTIONS = (
   "C/B#",
    "C#/Db",
    "D",
    "Eb/D#",
    "E/Fb",
    "F/E#",
    "F#/Gb",
    "G",
    "Ab/G#",
    "A",
    "Bb/A#",
    "B/Cb"
)

inversion_point = StringVar()
inversion_point.set("Inversion Point")
menu_inversion_point = OptionMenu(root, inversion_point, *tuple(OPTIONS), command=lambda _: inversion_point_check())
menu_inversion_point.grid(column=7, row=1)

frame5 = Frame(height=1, width=10).grid(column=8, row=1)

# Row 1
frame6 = Frame(height=10).grid(column=0, row=2)

inversion_on = IntVar()
checkbox_inversion = Checkbutton(root, text="               Inversion: ", variable=inversion_on, onvalue=1, offvalue=0,
                                 command=inversion_point_check)
checkbox_inversion.grid(column=1, row=3, columnspan=2, sticky='E')
checkbox_inversion.configure(disabledforeground="Blue", font="Italics", activeforeground="Red")

inversion = StringVar()
label_inversion = Label(root, textvariable=inversion).grid(column=3, row=3, sticky='W')

# button_inversion = Button(root, text=u"Playback", command=OnButtonClick).grid(column=5, row=3)

button_transform = Button(root, text=u"Transform", command=transform_click)
button_transform.grid(column=7, row=3)

# Row 2
frame7 = Frame(height=10).grid(column=0, row=4)

retro_on = IntVar()
checkbox_retro = Checkbutton(root, text="            Retrograde: ", variable=retro_on, onvalue=1, offvalue=0)
checkbox_retro.grid(column=1, row=5, columnspan=2, sticky='E')

retro = StringVar()
label_retro = Label(root, textvariable=retro).grid(column=3, row=5, sticky='W')

# button_retro = Button(root, text=u"Playback", command=OnButtonClick).grid(column=5, row=5)

button_reset = Button(root, text=u"Reset", command=reset_click).grid(column=7, row=5)

# Row 3
frame8 = Frame(height=10).grid(column=0, row=6)

inverse_retro_on = IntVar()
checkbox_inverse_retro = Checkbutton(root, variable=inverse_retro_on, text="Inverse Retrograde: ", onvalue=1,
                                     offvalue=0, command=inversion_point_check)
checkbox_inverse_retro.grid(column=1, row=7, columnspan = 2, sticky = 'E')

inverse_retro = StringVar()
label_inverse_retro = Label(root, textvariable = inverse_retro).grid(column=3, row=7, sticky='W')

# button_inverse_retro = Button(root, text=u"Playback", command=OnButtonClick).grid(column=5, row=7)

button_quit = Button(root, text=u"Quit", command=root.quit).grid(column=7, row=7)

frame9 = Frame(height=10).grid(column=0, row=8)

root.mainloop()