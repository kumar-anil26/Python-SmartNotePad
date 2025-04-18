import time
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser,font,messagebox,filedialog,simpledialog

from speech_recognition import RequestError, WaitTimeoutError, UnknownValueError

import NotePadDbController
import NotePadFileController
import traceback
import os

class NotePad:
    def __init__(self):
        #self.new_file = None
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        self.root.title("SmartNotePad")
        self.root.wm_iconbitmap("icons/icon.ico")

        self.set_icons()
        self.set_menu_bar()
        self.set_tool_bar()
        self.set_tool_bar_event_binding()
        self.set_status_bar()
        self.set_file_menu_event_binding()

        self.set_file_sub_menu()
        self.set_edit_sub_menu()
        self.set_view_sub_menu()
        self.set_color_theme()
        self.set_canvas()

        self.set_controllers()
        self.check_db_status()

        self.root.protocol("WM_DELETE_WINDOW",self.exit_func)

    def set_icons(self):
        self.new_icon = tk.PhotoImage(file="icons/new.png")
        self.open_icon = tk.PhotoImage(file="icons/open.png")
        self.save_icon = tk.PhotoImage(file="icons/save.png")
        self.save_as_icon = tk.PhotoImage(file="icons/save_as.png")
        self.exit_icon = tk.PhotoImage(file="icons/exit.png")
        self.copy_icon = tk.PhotoImage(file="icons/copy.png")
        self.paste_icon = tk.PhotoImage(file="icons/paste.png")
        self.cut_icon = tk.PhotoImage(file="icons/cut.png")
        self.clear_all_icon = tk.PhotoImage(file="icons/clear_all.png")
        self.find_icon = tk.PhotoImage(file="icons/find.png")
        self.tool_bar_icon = tk.PhotoImage(file="icons/tool_bar.png")
        self.status_bar_icon = tk.PhotoImage(file="icons/status_bar.png")
        self.light_default_icon = tk.PhotoImage(file="icons/light_default.png")
        self.light_plus_icon = tk.PhotoImage(file="icons/light_plus.png")
        self.dark_icon = tk.PhotoImage(file="icons/dark.png")
        self.red_icon = tk.PhotoImage(file="icons/red.png")
        self.monokai_icon = tk.PhotoImage(file="icons/monokai.png")
        self.night_blue_icon = tk.PhotoImage(file="icons/night_blue.png")

    def set_menu_bar(self):
        self.main_menu = tk.Menu()
        self.root.config(menu=self.main_menu)
        self.p_file = tk.Menu(self.main_menu,tearoff = False)
        self.file_menu = tk.Menu(self.main_menu,tearoff = False)
        self.edit_menu = tk.Menu(self.main_menu,tearoff = False)
        self.view_menu = tk.Menu(self.main_menu,tearoff = False)
        self.color_theme = tk.Menu(self.main_menu,tearoff = False)
        self.theme_choice = tk.StringVar()
        self.color_icons = (self.light_default_icon,self.light_plus_icon,self.dark_icon,self.red_icon,self.monokai_icon,self.night_blue_icon)
        self.color_dict = {
            'Light Default': ('#000000', '#ffffff'),
            'Light Plus': ('#474747', '#e0e0e0'),
            'Dark': ('#c4c4c4', '#2d2d2d'),
            'Red': ('#2d2d2d', '#ffe8e8'),
            'Monokai': ('#d3b774', '#474747'),
            'Night Blue': ('#ededed', '#6b9dc2')
        }
        self.main_menu.add_cascade(label = "File",menu=self.file_menu)
        self.main_menu.add_cascade(label="Edit",menu=self.edit_menu)
        self.main_menu.add_cascade(label = "View",menu = self.view_menu)
        self.main_menu.add_cascade(label = "Color Theme",menu = self.color_theme)
        self.main_menu.add_cascade(label="Secure File",menu=self.p_file,compound=tk.LEFT)

    def set_tool_bar(self):
        self.tool_bar = ttk.Label(self.root)
        self.tool_bar.pack(side=tk.TOP,fill = tk.X)
        self.show_tool_bar = tk.BooleanVar()
        self.show_tool_bar.set(True)
    # font Families

        self.font_tuple = tk.font.families()
        self.font_family = tk.StringVar()
        self.font_box = ttk.Combobox(self.tool_bar, width=30, textvariable=self.font_family,state='readonly')
        self.font_box['value'] = self.font_tuple
        self.font_box.current(self.font_tuple.index("Arial"))
        self.font_box.grid(row = 0 , column = 0, padx = 5)
    #Size box
        self.size_var = tk.IntVar()
        self.font_size = ttk.Combobox(self.tool_bar, width =14, textvariable=self.size_var, state = 'readonly' )
        self.font_size['value'] = tuple(range(8,81))
        self.font_size.current(4)
        self.font_size.grid(row = 0, column = 1, padx = 5)
    #Bold button

        self.bold_icon = tk.PhotoImage(file="icons/bold.png")
        self.bold_btn = ttk.Button(self.tool_bar,image=self.bold_icon)
        self.bold_btn.grid(row = 0 , column = 2, padx = 5)
    # ittalic button

        self.italic_icon = tk.PhotoImage(file="icons/italic.png")
        self.italic_btn = ttk.Button(self.tool_bar,image=self.italic_icon)
        self.italic_btn.grid(row = 0, column = 3, padx = 5)
    #underline button

        self.underline_icon = tk.PhotoImage(file="icons/underline.png")
        self.underline_btn = ttk.Button(self.tool_bar, image = self.underline_icon)
        self.underline_btn.grid(row = 0, column = 4, padx = 5)
    #font color button

        self.font_color_icon = tk.PhotoImage(file="icons/font_color.png")
        self.font_color_btn = ttk.Button(self.tool_bar, image=self.font_color_icon)
        self.font_color_btn.grid(row = 0, column=5,  padx = 5)
    #Align left button

        self.align_left_icon = tk.PhotoImage(file="icons/align_left.png")
        self.align_left_btn = ttk.Button(self.tool_bar, image = self.align_left_icon)
        self.align_left_btn.grid(row = 0, column = 6, padx = 5)
    #Align center button

        self.align_center_icon = tk.PhotoImage(file="icons/align_center.png")
        self.align_center_btn = ttk.Button(self.tool_bar, image = self.align_center_icon)
        self.align_center_btn.grid(row = 0, column = 7, padx = 5)
    #Align right button

        self.align_right_icon = tk.PhotoImage(file="icons/align_right.png")
        self.align_right_btn = ttk.Button(self.tool_bar, image = self.align_right_icon)
        self.align_right_btn.grid(row = 0, column = 8, padx = 5)
    #Mic button

        self.microphone_icon = tk.PhotoImage(file="icons/microphone.png")
        self.microphone_btn = ttk.Button(self.tool_bar, image=self.microphone_icon)
        self.microphone_btn.grid(row = 0, column = 9, padx = 5)

    #Time label

        self.timeLabel = ttk.Label(self.tool_bar, foreground='black', font=('calibri',25,'bold'))
        self.timeLabel.grid(row=0, column=10, padx=300)

    def set_tool_bar_event_binding(self):
        # Font families and font size functionality
        self.current_font_family = "Arial"
        self.curren_font_size = 12
        self.font_box.bind("<<ComboboxSelected>>",self.change_font)
        self.font_size.bind("<<ComboboxSelected>>",self.change_fontsize)
        self.bold_btn.configure(command = self.change_bold)
        self.italic_btn.configure(command = self.change_italic)
        self.underline_btn.configure(command = self.change_underline)
        self.font_color_btn.configure(command = self.change_font_color)
        self.align_left_btn.configure(command = self.change_align_left)
        self.align_center_btn.configure(command = self.change_align_center)
        self.align_right_btn.configure(command = self.change_align_right)
        self.microphone_btn.configure(command = self.say_something)

    def set_status_bar(self):
        self.status_bar = ttk.Label(self.root,text = "Status bar")
        self.status_bar.pack(side = tk.BOTTOM)
        self.count = 0
        self.show_status_bar = tk.BooleanVar()
        self.show_status_bar.set(True)

    def set_file_menu_event_binding(self):
        self.root.bind("<Control-n>",self.new_file)
        self.root.bind("<Control-N>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-O>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-S>", self.save_file)
        self.root.bind("<Alt-s>", self.save_as_file)
        self.root.bind("<Alt-S>", self.save_as_file)
        self.root.bind("<Control-q>", self.exit_func)
        self.root.bind("<Control-Q>", self.exit_func)
        self.root.bind("<Control-f>", self.find_func)
        self.root.bind("<Control-F>", self.find_func)

        self.root.bind("<Control-a>", lambda e:self.say_something())
        self.root.bind("<Control-A>", lambda e: self.say_something())

    def set_file_sub_menu(self):
        self.file_menu.add_command(label='New', image=self.new_icon, compound=tk.LEFT, accelerator = 'Ctrl + N', command = self.new_file)
        self.file_menu.add_command(label = "Open", image = self.new_icon, compound=tk.LEFT, accelerator = "Ctrl + O", command = self.open_file)
        self.file_menu.add_command(label = "Sava", image = self.save_icon, compound= tk.LEFT, accelerator = 'Ctrl + S', command = self.save_file)
        self.file_menu.add_command(label="Save as", image=self.save_as_icon, compound = tk.LEFT, accelerator = 'Alt + S', command = self.save_as_file)
        self.file_menu.add_command(label = "Exit", image = self.exit_icon , compound=tk.LEFT, accelerator = "Ctrl + Q", command = self.exit_func)

        self.p_file.add_command(label = "Secure Files", compound = tk.LEFT, accelerator = "Ctrl + P", command = self.secure_files)


    def set_edit_sub_menu(self):
        self.edit_menu.add_command(label="Copy", image=self.copy_icon, compound=tk.LEFT, accelerator='Ctrl + C',command=lambda e: self.text_editor.event_generate("<Control c>"))
        self.edit_menu.add_command(label = "Paste", image=self.paste_icon, compound=tk.LEFT, accelerator='Ctrl+V', command=lambda e: self.text_editor.event_generate("<Control v>"))
        self.edit_menu.add_command(label="Cut",image=self.cut_icon,compound=tk.LEFT,accelerator='Ctrl+X',command=lambda e: self.text_editor.event_generate("<Control x>"))
        self.edit_menu.add_command(label="Clear All",image = self.clear_all_icon,compound=tk.LEFT, accelerator='Alt+X',command=lambda e:self.text_editor.delete(1.0,tk.END))
        self.edit_menu.add_command(label="Find",image=self.find_icon,compound=tk.LEFT,accelerator='Ctrl+F',command =self.find_func)

    def set_view_sub_menu(self):
        self.view_menu.add_checkbutton(label="Tool bar",image=self.tool_bar_icon,onvalue= True,offvalue=0,variable = self.show_tool_bar,compound=tk.LEFT,command= self.hide_tool_bar)
        self.view_menu.add_checkbutton(label="Status bar",image=self.status_bar_icon,onvalue=1,offvalue=False,variable=self.show_status_bar,compound=tk.LEFT,command=self.hide_status_bar)


    def set_color_theme(self):
        for i in self.color_dict:
            self.color_theme.add_radiobutton(label=i,image=self.color_icons[self.count],variable = self.theme_choice,compound=tk.LEFT,command=self.change_theme)
            self.count+=1

    def set_canvas(self):
        #Text Editor
        self.text_editor = tk.Text(self.root)
        self.text_editor.config(wrap='word',relief = tk.FLAT)
        self.text_editor.focus_set()

        self.scoll_bar = ttk.Scrollbar(self.root)
        self.scoll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.pack(fill=tk.BOTH,expand=True)
        self.scoll_bar.config(command = self.text_editor.yview)
        self.text_editor.config(yscrollcommand=self.scoll_bar.set)

        self.text_changed = False
        self.text_editor.bind("<<Modified>>",self.changed)

    def set_controllers(self):
        self.file_controller = NotePadFileController.File_Controller()
        self.db_controller = NotePadDbController.Db_Controller()

    def check_db_status(self):
        self.db_status = self.db_controller.get_db_status()
        if self.db_status:
            self.files = self.db_controller.load_file_from_db()
        else:
            messagebox.showerror("DataBase Error","Conn't connec to the DB")
            print(traceback.format_exc())

    def exit_func(self):
       try:
           if self.text_changed:
            if messagebox.askyesno("File not Saved!","Do you want to save the file ?"):
                msg = self.text_editor.get(1.0,tk.END)
                self.file_controller.save_file(msg)
       except:
           messagebox.showerror("App Error","Error in Closing")
           print(traceback.format_exc())
       finally:
           endTime = time.time()
           messagebox.showinfo("Using Time","Total use time :  " + str(round((endTime - startTime) / 60)) + " mintues")
           messagebox.showinfo("Thank you","Have a good day")
           self.db_controller.close_notepad()
           self.root.destroy()

    def change_font(self,event=None):
        self.current_font_family = self.font_family.get()
        self.text_editor.config(font=(self.current_font_family,self.curren_font_size))

    def change_fontsize(self,event = None):
        self.curren_font_size = int(self.size_var.get())
        self.text_editor.config(font=(self.current_font_family,self.curren_font_size))

    def change_bold(self):
        self.current_font_details = tk.font.Font(font=self.text_editor['font'])
        if self.current_font_details.actual('weight') == 'normal':
            self.text_editor.configure(font=(self.current_font_family,self.curren_font_size,"bold"))
        if self.current_font_details.actual('weight') == 'bold':
            self.text_editor.configure(font=(self.current_font_family, self.curren_font_size, "normal"))

    def change_italic(self):
        self.current_font_details = tk.font.Font(font=self.text_editor['font'])
        if self.current_font_details.actual('slant') == 'roman':
            self.text_editor.configure(font=(self.current_font_family, self.curren_font_size, "italic"))
        if self.current_font_details.actual('slant') == 'italic':
            self.text_editor.configure(font=(self.current_font_family, self.curren_font_size, "roman"))

    def change_underline(self):
        self.current_font_details = tk.font.Font(font=self.text_editor['font'])
        if self.current_font_details.actual()['underline'] == 0:
            self.text_editor.config(font = (self.current_font_family,self.curren_font_size,'underline'))
        if self.current_font_details.actual()['underline'] == 1:
            self.text_editor.config(font = (self.current_font_family,self.curren_font_size,'normal'))

    def change_font_color(self):
        color_var = tk.colorchooser.askcolor()
        self.text_editor.config(fg=color_var[1])

    def change_align_left(self):
        text_content = self.text_editor.get(1.0,'end').strip()
        self.text_editor.tag_config('left',justify=tk.LEFT)
        self.text_editor.delete(1.0,tk.END)
        self.text_editor.insert(tk.INSERT,text_content,'left')

    def change_align_center(self):
        text_content = self.text_editor.get(1.0, tk.END).strip()
        self.text_editor.tag_config('center', justify=tk.CENTER)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, 'center')

    def change_align_right(self):
        text_content = self.text_editor.get(1.0, tk.END).strip()
        self.text_editor.tag_config('right', justify=tk.RIGHT)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, 'right')

    def say_something(self):
        try:
            self.take_audio = self.file_controller.take_query()
            if self.take_audio =='':
                messagebox.showinfo("Say again","Your voice is not Recognizable...")

            elif self.take_audio.lower() == 'he mojo open file':
                self.open_file()

            elif self.take_audio.lower() == 'he mojo save file':
                self.save_file()

            elif self.take_audio.lower() == 'he mojo new file':
                self.new_file()

            elif self.take_audio.lower() == 'he mojo file save':
                self.save_as_file()

            elif self.take_audio.lower() == 'he mojo close app':
                self.exit_func()

            elif self.take_audio.lower() == 'he mojo search':
                self.find_func()

            elif self.take_audio.lower() == 'he mojo hide status bar':
                self.hide_status_bar()

            elif self.take_audio.lower() == 'he mojo hide toolbar':
                self.hide_tool_bar()

            elif self.take_audio.lower() == 'he mojo text bold':
                self.change_bold()

            elif self.take_audio.lower() == 'he mojo text italic':
                self.change_italic()

            elif self.take_audio.lower() == 'he mojo text underline':
                self.change_underline()

            elif self.take_audio.lower() == 'he mojo remove underline':
                self.change_underline()

            else:
                messagebox.showinfo("Invalid Input","Sorry!, Please try again...")
                print(traceback.format_exc())
        except RequestError as request:
            messagebox.showerror("No Interner","Please check your internet connection!")
            print(traceback.format_exc())
        except WaitTimeoutError as wait:
            messagebox.showerror("Time Over","Time limit exceeded!")
            print(traceback.format_exc())
        except UnknownValueError as unkwn:
            messagebox.showerror("Non Translable","Speech unrecognizable!")
            print(traceback.format_exc())
        except Exception as e:
            print(e)

    def new_file(self,event=None):
        self.file_controller.new_file()
        self.root.title("SmartNotePad")
        self.text_editor.delete(1.0,tk.END)

    def open_file(self,event=None):
        try:
            self.msg,self.base = self.file_controller.read_file('')
            if self.db_controller.is_file_secure(self.base):
                pwd = self.get_file_pwd()
                if pwd == self.db_controller.get_file_pwd(self.base):
                    self.text_editor.delete(1.0,tk.END)
                    self.text_editor.insert(1.0,self.msg)
                    self.root.title(self.base)
                else:
                    messagebox.showerror("Password Error", "Wrong Password")
                    print(traceback.format_exc())
            else:
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, self.msg)
                self.root.title(self.base)
        except FileNotFoundError as e:
            messagebox.showerror("Wrong file Name" , "File doesnot exist!")
        except:
            print(traceback.format_exc())


    def save_file(self,event=None):
        try:
            contents = self.text_editor.get(1.0,tk.END)
            file_name = self.file_controller.save_file(contents)
            self.root.title(file_name)
        except:
            messagebox.showerror("File Error" , "Conn't save the file")
            print(traceback.format_exc())

    def save_as_file(self,event = None):
        try:
            contents = self.text_editor.get(1.0,tk.END)
            self.file_controller.save_as_file(contents)
        except:
            messagebox.showerror("File Error" , "Conn't save as the file")
            print(traceback.format_exc())

    def get_file_pwd(self):
        access_pwd = simpledialog.askstring("Passeord Input", "Enter file Password ")
        return access_pwd

    def find_func(self,event=None):
        self.find_dialogue = tk.Toplevel()
        self.find_dialogue.geometry("450x250+700+350")
        self.find_dialogue.title("Find")
        self.find_dialogue.resizable(0,0)

        # Frame
        self.find_frame = ttk.LabelFrame(self.find_dialogue,text='Find/Replace')
        self.find_frame.pack(pady=20)

        # Label
        self.text_find_label = ttk.Label(self.find_frame, text='Find :')
        self.text_replace_label = ttk.Label(self.find_frame, text ='Replace :')

        # Entry:
        self.find_input = ttk.Entry(self.find_frame, width = 30)
        self.replace_input = ttk.Entry(self.find_frame, width=30)

        # Button

        self.find_button = ttk.Button(self.find_frame,text='Find', command = self.find)
        self.replace_button = ttk.Button(self.find_frame, text='Replace', command = self.replace)

        #Label grid

        self.text_find_label.grid(row=0, column=0, padx = 4, pady = 4)
        self.text_replace_label.grid(row=1, column=0, padx = 4, pady = 4)

        # Entry grid

        self.find_input.grid(row = 0, column = 1, padx = 4, pady = 4)
        self.replace_input.grid(row = 1, column = 1, padx = 4, pady = 4)

        # Button grid

        self.find_button.grid(row = 2, column = 0, padx = 8, pady = 4)
        self.replace_button.grid(row = 2, column = 1, padx = 8, pady = 4)

        self.find_dialogue.mainloop()

    def find(self):
        word = self.find_input.get()
        if word:
            self.text_editor.tag_remove('match','1.0',tk.END)
            matches = 0
            start_pos = '1.0'
            while True:
                start_pos = self.text_editor.search(word,start_pos,stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                self.text_editor.tag_add('match',start_pos,end_pos)
                self.text_editor.tag_config('match',background = 'yellow', foreground ='red')
                matches +=1
                start_pos = end_pos


    def replace(self):
        word = self.find_input.get()
        replace_text = self.replace_input.get()
        if len(word.strip()) == 0 or len(replace_text.strip())==0:
            return
        content = self.text_editor.get(1.0,tk.END)
        new_content = content.replace(word,replace_text)
        self.text_editor.delete(1.0,tk.END)
        self.text_editor.insert(1.0,new_content)

    def is_secure_file(self,file_name):
         return self.db_controller.is_file_secure(file_name)

    def secure_files(self):
        if self.db_status:
            self.file_dialogue = tk.Toplevel()
            self.file_dialogue.geometry("450x400+500+200")
            self.file_dialogue.title("Secure Files")
            self.file_dialogue.resizable(0,0)

            #Frame

            self.file_frame = ttk.LabelFrame(self.file_dialogue,text="Add Secure File")
            self.file_frame.pack(pady=20)

            #label

            self.text_file_owner_label = ttk.Label(self.file_frame,text = "File Owner :")
            self.text_file_pwd_label = ttk.Label(self.file_frame,text="File Password :")
            self.total_files = self.db_controller.get_file_count()
            self.total_files_label = ttk.Label(self.file_frame,text=f"Total Files : {self.total_files}")

            # Entry
            self.text_file_owner_input = tk.Entry(self.file_frame, width=30)
            self.text_file_pwd_input = tk.Entry(self.file_frame, width=30)

             #Buttons

            self.add_file_button = ttk.Button(self.file_frame, text = "Add File", command = self.add_secure_file)
            self.open_file_button = ttk.Button(self.file_frame, text = "Open File", command = self.open_secure_file)
            self.remove_file_button = ttk.Button(self.file_frame, text = "Remove File", command = self.remove_secure_file)

        #Label grid

            self.text_file_owner_label.grid(row =0, column=0, padx=4, pady=4)
            self.text_file_pwd_label.grid(row=1, column=0, padx=4, pady=4)
            self.total_files_label.grid(row=2, column=0, padx=4, pady=4)

        #Entry grid

            self.text_file_owner_input.grid(row=0, column=1, padx=4, pady=4)
            self.text_file_pwd_input.grid(row=1, column=1, padx=4, pady=4)

        #Buttons grid

            self.add_file_button.grid(row=3, column=0, padx=8, pady=4)
            self.open_file_button.grid(row=3, column=1, padx=8, pady=4)
            self.remove_file_button.grid(row=3, column=2, padx=8, pady=4)

        # Scroll bar
            scrollbar = ttk.Scrollbar(self.file_dialogue, orient = 'vertical')
            scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        # List Box
            self.fileList = tk.Listbox(self.file_dialogue)
            self.fileList.pack(fill=tk.BOTH, expand=True)

            self.fileList.configure(background='white', foreground='black')
            self.fileList.configure(disabledforeground='#a3a3a3')
            self.fileList.configure(font='Lato')
            self.fileList.configure(highlightbackground='#d9d9d9')
            self.fileList.configure(highlightcolor='#d9d9d9')
            self.fileList.configure(selectbackground='#c4c4c4')
            self.fileList.configure(selectforeground='black')
            self.fileList.configure(width=40)
            self.fileList.configure(yscrollcommand=scrollbar.set)
            scrollbar.configure(command=self.fileList.yview)
            self.fileList.bind("<Double-1>",self.list_double_click)
         # Load file from DB

            for value in self.files.keys():
                self.f_name = value
                self.files_owner = self.files.get(self.f_name)[1]
                self.full_name = "  "+self.f_name + "              "+ "[Owner : "+self.files_owner+" ]"
                self.fileList.insert(tk.END,self.full_name)
            self.file_dialogue.mainloop()
        else:
            messagebox.showerror("DataBase Error","Please connect to the DataBase")


    def add_secure_file(self):
        try:
            if self.text_file_owner_input.get() !='' and self.text_file_pwd_input.get() != '':
                self.file_owner = self.text_file_owner_input.get()
                self.file_pwd = self.text_file_pwd_input.get()
                self.file_path = filedialog.askopenfilename(title="Select File name", filetype=[('Text Documents','*.*')])
                self.file_name = os.path.basename(self.file_path)
                result = self.db_controller.add_file(self.file_name,self.file_path,self.file_owner,self.file_pwd)
                if result.find('already')!=-1:
                    messagebox.showerror("Error",result)
                elif result == "":
                    messagebox.showerror("Error","Something went wrong")
                else:
                    messagebox.showinfo("Success",result)
            else:
                messagebox.showerror("Error ?","Please Input file owner and password before adding file")
        except:
            messagebox.showerror("DB Error","Error while adding")
            print(traceback.format_exc())


    def open_secure_file(self):
        try:
            self.sel_file_index_tuple = self.fileList.curselection()
            if len(self.sel_file_index_tuple) == 0:
                messagebox.showerror("Error!","Plese select file first")
            else:
                self.full_file_name = self.fileList.get(self.sel_file_index_tuple[0])
                self.file_pos = self.full_file_name.find("[")
                self.file_name = self.full_file_name[:self.file_pos].strip()
                self.file_path = self.db_controller.get_file_path(self.file_name)
                content,basename = self.file_controller.read_file(self.file_path)
                pwd = self.get_file_pwd()
                if pwd == self.db_controller.get_file_pwd(basename):
                    self.text_editor.delete(1.0,tk.END)
                    self.text_editor.insert(1.0,content)
                    self.root.title(basename)
                else:
                    messagebox.showerror("Wrong password!","Password is wrong, Try again...")
        except:
            messagebox.showerror("Secure file Error!","Secure file opening Error, Please try again...")
            print(traceback.format_exc())

    def remove_secure_file(self):
        try:
            self.select_file_index_tuple = self.fileList.curselection()
            if len(self.select_file_index_tuple) != 0 :
                self.full_file_name = self.fileList.get(self.select_file_index_tuple[0])
                self.file_pos = self.full_file_name.find("[")
                self.file_name = self.full_file_name[:self.file_pos].strip()
                self.db_controller.remove_file(self.file_name)
                self.fileList.delete(self.select_file_index_tuple[0])
                messagebox.showinfo("Success","File remove Successfylly.")
            else:
                messagebox.showerror("Error!","Please Select file")
        except:
            messagebox.showerror("Secure File Error!","Removing secure file error")
            print(traceback.format_exc())


    def list_double_click(self,e):
        self.open_secure_file()

    def hide_tool_bar(self):
        if self.show_tool_bar:
            self.tool_bar.pack_forget()
            self.show_tool_bar = False
        else:
            self.text_editor.pack_forget()
            self.status_bar.pack_forget()
            self.tool_bar.pack(side = tk.TOP,fill=tk.X)
            self.text_editor.pack(fill = tk.BOTH,expand=True)
            self.status_bar.pack(side=tk.BOTTOM)
            self.show_tool_bar = True

    def hide_status_bar(self):
        if self.show_status_bar:
            self.status_bar.pack_forget()
            self.show_status_bar = False
        else:
            self.status_bar.pack(side = tk.BOTTOM)
            self.show_status_bar = True

    def change_theme(self):
        theme_name = self.theme_choice.get()
        foreground_color,background_color = self.color_dict[theme_name]
        self.text_editor.config(fg=foreground_color,bg = background_color)

    def changed(self,event=None):
        if self.text_editor.edit_modified():
            self.text_changed = True
            words = len(self.text_editor.get(1.0,'end-1c').split())
            characters = len(self.text_editor.get(1.0,'end-1c'))
            self.status_bar.config(text=f"Total words :{words} and Total characters :{characters}")
        self.text_editor.edit_modified(False)

    def run(self):
        self.root.mainloop()


    def dateTime(self):
        currentTime = time.strftime("%H:%M:%S")
        self.timeLabel.config(text=currentTime)
        self.timeLabel.after(1000,self.dateTime)

startTime=time.time()
obj = NotePad()
obj.dateTime()
obj.run()


