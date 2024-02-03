import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig


class user_model():

    def __init__(self):
        try:
            self.con = mysql.connector.connect(host= dbconfig['hostname'],user =dbconfig['username'],password = dbconfig['password'],database =dbconfig['database'])
            self.con.autocommit=True
            self.cur = self.con.cursor(dictionary = True)
            print("connection Successful")
        except:
            print("Something went wrong")

    def user_getall_model(self):
        # get Query  execution code
        self.cur.execute("SELECT * FROM students")
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"Students":result},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            return make_response({"message":"No Data found!"},204)
    
    def user_adduser_model(self,data):
        # post Query  execution code
        self.cur.execute(f"INSERT INTO students(student_name,email,phone,semister,password) VALUES('{data['student_name']}','{data['email']}','{data['phone']}','{data['semister']}','{data['password']}')")
        return make_response({"message":"User Created Successfully"},201)
    
    def user_updateuser_model(self,data):
        # put Query  execution code
        self.cur.execute(f"UPDATE students SET student_name ='{data['student_name']}',email='{data['email']}',phone='{data['phone']}',semister='{data['semister']}',password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount > 0:
                return make_response({"message":"User UPDATED Successfully"},201)
        else:
            return make_response({"message":"Nothing to Update"},202)
        
    def user_deleteuser_model(self,id):
        # put Query  execution code
        self.cur.execute(f"DELETE FROM students WHERE id={id}")
        if self.cur.rowcount > 0:
                return make_response({"message":"User DELETE Successfully"},200)
        else:
            return make_response({"message":"Nothing to delete"},202)
        
    def user_patch_model(self,data,id):
        qry = "UPDATE students SET "
        for key in data:
            qry += f"{key}='{data[key]}',"
        qry = qry[:-1]+ f" WHERE id={id}"

        self.cur.execute(qry)
        if self.cur.rowcount > 0:
                return make_response({"message":"User Updated Successfully"},201)
        else:
            return make_response({"message":"Nothing to Update"},202)
        
        
    def user_pagination_model(self,limit,page):
        limit =int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f"SELECT * FROM students LIMIT {start},{limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"Students":result})
        else:
            return make_response({"message":"No Data found!"})
        
    def user_upload_avatar_model(self,uid,filepath):
        self.cur.execute(f"UPDATE students SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount > 0:
                return make_response({"message":"File Uploaded Successfully"},201)
        else:
            return make_response({"message":"Nothing to Update"},202)
        
    def user_login_model(self,data):
        # put Query  execution code
        self.cur.execute(f"SELECT id,student_name,email,phone,semister,avatar,role_id FROM students WHERE email ='{data['email']}' and password ='{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
             "payload" : userdata,
             "exp" : exp_epoch_time
        }
        token = jwt.encode(payload,"yasir",algorithm="HS256")
        return make_response({"token":token},200)
    
