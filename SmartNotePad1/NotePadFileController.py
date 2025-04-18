import NotePadFileModel
import speech_recognition as s

class File_Controller:
    def __init__(self):
        self.file_model = NotePadFileModel.File_Model()

    def save_file(self,msg):
        file_name = self.file_model.save_file(msg)
        return  file_name
    def save_as_file(self,msg):
        self.file_model.save_as(msg)

    def read_file(self,url):
        self.msg,self.basename = self.file_model.read_file(url)
        return self.msg,self.basename

    def new_file(self):
        self.file_model.new_file()

    def take_query(self):
        sr = s.Recognizer()
        with s.Microphone() as m:
            audio = sr.listen(m)
            text = sr.recognize_google(audio,language="en-IN")
            return text