from cx_Oracle import *
from traceback import *

class Db_Model:
    def __init__(self):
        self.file_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = connect("c##mojo/mojo@127.0.0.1/xe")
            self.cur = self.conn.cursor()
        except DatabaseError:
            self.db_status = False
            print("DB Error",format_exc())
    def get_db_satus(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def add_file(self,file_name,file_path,file_owner,file_pwd):
        self.file_dict = {file_name:(file_path,file_owner,file_pwd)}
        return file_name

    def get_file_path(self,file_name):
        file_path,file_owner,file_pwd = self.file_dict[file_name]
        return file_path

    def add_file_to_db(self,file_name,file_path,file_owner,file_pwd):
        self.cur.execute("select max(file_id) from mysecurefiles")
        last_file_id = self.cur.fetchone()
        next_file_id = 1
        if last_file_id[0] is not None:
            next_file_id = last_file_id[0]+1
        self.cur.execute("insert into mysecurefiles values(:1,:2,:3,:4,:5)",(next_file_id,file_name,file_path,file_owner,file_pwd))
        self.conn.commit()
        return "file successfully added to the database!"

    def load_file_from_db(self):
        self.cur.execute("select file_name,file_path,file_owner,file_pwd from mysecurefiles")
        file_added = False
        for file_name,file_path,file_owner,file_pwd in self.cur:
            self.file_dict[file_name] = (file_path,file_owner,file_pwd)
            file_added = True
        if file_added == True:
            return "Files populated from the DB"
        else:
            return "No file present in your DB"

    def remove_file_from_db(self,file_name):
        self.cur.execute("delete from mysecurefiles where file_name=:1",(file_name,))
        if self.cur.rowcount == 0:
            return "File not present in your DB"
        self.file_dict.pop(file_name)
        self.conn.commit()
        return "Remove file from DB"

    def is_file_secure(self,file_name):
        if file_name in self.file_dict:
            return True
        else:
            return False

    def get_file_pwd(self,file_name):
        file_path, file_owner, file_pwd = self.file_dict[file_name]
        return file_pwd

    def get_file_count(self):
        return len(self.file_dict)



