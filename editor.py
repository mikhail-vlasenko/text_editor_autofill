import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from text_editor_autofill.model import get_cont


class Notepad:
    __root = Tk()

    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self, **kwargs):

        # Set icon
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass

        # Set window size (the default is 300x300)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.__root.title("Untitled - not Notepad")

        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left-alling
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # For right-allign
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # To open new file
        self.__thisFileMenu.add_command(label="New",
                                        command=self.__newFile)

        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open",
                                        command=self.__openFile)

        # To save current file
        self.__thisFileMenu.add_command(label="Save",
                                        command=self.__saveFile)

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File",
                                       menu=self.__thisFileMenu)

        # ----------

        self.__thisEditMenu.add_command(label="Predict", command=self.predict)

        self.p_button = Button(self.__root, text="Predict", command=self.predict)

        self.__thisTextArea.configure(undo=True, autoseparators=True, maxundo=-1)

        self.undo_button = Button(self.__root, text="Undo", command=self.undo)

        # ----------

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut",
                                        command=self.__cut)

        # to give a feature of copy
        self.__thisEditMenu.add_command(label="Copy",
                                        command=self.__copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste",
                                        command=self.__paste)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit",
                                       menu=self.__thisEditMenu)

        # To create a feature of description of the notepad
        self.__thisHelpMenu.add_command(label="About Notepad",
                                        command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help",
                                       menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically according to the content
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    # exit()

    def __showAbout(self):
        showinfo("not Notepad", "")

    def __openFile(self):

        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])

        if self.__file == "":

            # no file to open
            self.__file = None
        else:

            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")

            self.__thisTextArea.insert(1.0, file.read())

            file.close()

    def __newFile(self):
        self.__root.title("Untitled - not Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.txt")])

            if self.__file == "":
                self.__file = None
            else:

                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - not Notepad")


        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")
        print(self.__thisTextArea.get(1.0, END))

    # ---------------

    def undo(self):
        self.__thisTextArea.edit_undo()

    def beautify(self, s):
        for i in range(len(s)):
            if s[i] == '.' and s[i+1] != ' ':
                s = s[:i+1] + ' ' + s[i+1:]
                if i+2 < len(s):
                    if i+3 < len(s):
                        s = s[:i+2] + s[i+2].upper() + s[i+3:]
                    else:
                        s = s[:i + 2] + s[i + 2].upper()
        return s

    def predict(self):
        text = self.beautify(self.__thisTextArea.get(1.0, END))
        print('text: {}'.format(text))
        sentence = ''
        for i in range(len(text) - 2, -1, -1):
            if text[i] == '.':
                sentence = text[i+2:-1]
                break
            if i == 0:
                sentence = text[:-1]
                break

        not_start = False
        if len(sentence.split()) > 3:
            whole_sentence = sentence
            sentence = sentence.split()[-3:]
            sentence = ' '.join(sentence)
            not_start = True

        sentence = sentence.capitalize()
        print('sentence: {}'.format(sentence))
        new_sent = get_cont(sentence, 3, 10, 0.5)
        if new_sent == -1:
            print()
            return

        if not_start:
            new_sent = new_sent[0].lower() + new_sent[1:]

        print(new_sent)
        cur = self.__thisTextArea.index(INSERT)
        print("cursor = " + str(cur))
        line_c, col_c = map(int, str(cur).split('.'))
        self.__thisTextArea.delete('{}.{}'.format(line_c, col_c - len(sentence)), END)
        self.__thisTextArea.insert(END, new_sent)

    # ---------------

    def run(self):
        self.p_button.grid()
        self.undo_button.grid()
        self.__root.mainloop()


notepad = Notepad(width=600, height=400)
notepad.run()
