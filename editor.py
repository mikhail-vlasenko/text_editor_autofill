import tkinter
import os
import re
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
    __thisStatusBar = Label(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    __thisTextSize = Entry(__root)

    # To add scrollbar
    # __thisScrollBar = Scrollbar(__thisTextArea)
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
        self.__thisTextArea.grid(row=0, column=0, columnspan=4, sticky=N + E + S + W)

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

        self.__thisTextArea.configure(undo=True, autoseparators=True, maxundo=-1)
        self.__thisTextArea.config(font=("Open Sans", 14))

        self.p_button = Button(self.__root, text="Predict", command=self.predict)
        self.undo_button = Button(self.__root, text="Undo", command=self.undo)
        self.p_button.grid(row=2, column=2)
        self.undo_button.grid(row=2, column=3)
        self.__thisTextSize.grid(row=2, column=1)

        self.__root.bind("<Return>", self.enter_pressed)
        self.__thisTextSize.bind("<Return>", self.change_font)
        self.__thisTextSize.configure(width=5)
        self.__thisTextSize.insert(END, '14')

        self.__thisStatusBar.configure(bd=0, relief=SUNKEN, anchor=W, text="Status bar")
        self.__thisStatusBar.grid(row=2, column=0, sticky=W)

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

        # self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically according to the content
        # self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        # self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

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
        if self.__file is None:
            # Save as new file
            print('not here')
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.txt")])
            print('here')

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
        s = re.sub(r'\bi\b', 'I', s)
        return s

    def predict(self, only2words=False):
        text = self.beautify(self.__thisTextArea.get(1.0, END))
        print('text: {}'.format(text))
        sentence = ''
        new_line = False
        for i in range(len(text) - 2, -1, -1):
            if text[i] == '.' or text[i] == '?' or text[i] == '!':
                sentence = text[i + 2:-1]
                break
            if text[i] == '\n':
                sentence = text[i + 1:-1]
                new_line = True
                break
            if i == 0:
                sentence = text[:-1]
                break

        not_start = False
        if only2words:
            sent_len = 2
        else:
            sent_len = 3
        print('sent len = {}'.format(sent_len))
        if len(sentence.split()) >= sent_len:
            whole_sentence = sentence
            sentence = sentence.split()[-sent_len:]
            sentence = ' '.join(sentence)
            not_start = True

        print('sentence: {}'.format(sentence))
        new_sent = get_cont(sentence, 3, num_tries=2, max_coef=1, max_tries=4, strict=False)
        if new_sent == -1:
            if not only2words:
                self.predict(only2words=True)
            else:
                self.__thisStatusBar.configure(text='--Can\'t continue--')
                print()
            return

        if not_start and not (new_sent[0] == 'I' and new_sent[1] == ' '):
            new_sent = new_sent[0].lower() + new_sent[1:]

        if not not_start:
            new_sent = new_sent[0].upper() + new_sent[1:]

        print(new_sent)
        cur = self.__thisTextArea.index(INSERT)
        print("cursor = " + str(cur))
        line_c, col_c = map(int, str(cur).split('.'))
        self.__thisTextArea.delete('{}.{}'.format(line_c, col_c - len(sentence)), END)
        if new_line and not not_start:
            new_sent = '\n' + new_sent
        self.__thisTextArea.insert(END, new_sent)
        self.__thisStatusBar.configure(text=new_sent)
        print('------------')

    def enter_pressed(self, event):
        text = self.__thisTextArea.get(1.0, END)
        if text[-3] == '.':
            return
        cur = self.__thisTextArea.index(INSERT)
        line_c, col_c = map(int, str(cur).split('.'))
        self.__thisTextArea.delete('{}.{}'.format(line_c, col_c), END)
        self.predict()

    def change_font(self, event):
        try:
            size = int(self.__thisTextSize.get())
        except ValueError:
            self.__thisStatusBar.configure(text='--Enter a natural number--')
            return
        self.__thisTextArea.config(font=("Open Sans", size))

    # ---------------

    def run(self):
        self.__root.mainloop()


notepad = Notepad(width=600, height=400)
notepad.run()
