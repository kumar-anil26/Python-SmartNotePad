import os
import string
from tkinter import filedialog

class File_Model:
    def __init__(self):
        #self.key = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.url = ""
        self.key =string.ascii_letters+''.join([str(x) for x in range (0,10)])
        self.offset = 5

    def encrypt(self,planeText):
        result = ""
        for ch in planeText:
            try:
                index = self.key.index(ch)
                newIndex = (index + self.offset)%62
                result = result + self.key[newIndex]
            except ValueError:
                result +=ch
        return result
    def decrypt(self,ciphertext):
        result=""
        for ch in ciphertext:
            try:
                index = self.key.index(ch)
                newIndex = (index-self.offset)%62
                result +=self.key[newIndex]
            except ValueError:
                result +=ch
        return result

    def open_file(self):
        self.url = filedialog.askopenfilename(title="Select file",filetypes=[("Text Document","*.*")])

    def new_file(self):
        self.url = ""

    def save_as(self,msg):
        encrypted_text = self.encrypt(msg)
        self.url = filedialog.asksaveasfile(mode="w", defaultextension=".ntxt", filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        if self.url is not None:
            self.url.write(encrypted_text)
            filepath = self.url.name
            self.url.close()
            self.url = filepath
        else:
            return

    def save_file(self,msg):
        if self.url == "":
            self.url = filedialog.asksaveasfilename(title="Ask file name", defaultextension=".ntxt", filetypes=[("Files Documents","*.*")])
        file_name,file_extension = os.path.splitext(self.url)
        file_name = os.path.basename(self.url)
        content = msg
        if file_extension in '.ntxt':
            self.encrypt(content)
        with open(self.url,'w',encoding="utf-8") as fw:
            fw.write(content)

        return file_name

    def read_file(self,url=''):
        if url != '':
            self.url = url
        else:
            self.open_file()
        basename = os.path.basename(self.url)
        file_name,file_extension = os.path.splitext(self.url)
        fr = open(self.url,"r")
        contents = fr.read()
        if file_extension == ".ntxt":
            contents = self.decrypt(contents)
        fr.close()
        return contents,basename

