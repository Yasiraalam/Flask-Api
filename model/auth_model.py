import mysql.connector
import json
from flask import make_response,request
from jwt.exceptions import ExpiredSignatureError
from functools import wraps
import jwt
import re
from config.config import dbconfig

class auth_model():

    def __init__(self):
        try:
            self.con = mysql.connector.connect(host= dbconfig['hostname'],user =dbconfig['username'],password = dbconfig['password'],database =dbconfig['database'])
            self.con.autocommit=True
            self.cur = self.con.cursor(dictionary = True)
            print("connection Successful")
        except:
            print("Something went wrong")
    
    def token_auth(self,endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                authorization = request.headers.get("authorization")
                # if re.match("^Bearer *([^]+) *$",authorization,flags=0):
                if re.match("^Bearer *(.+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        decoded_token = jwt.decode(token, "yasir", algorithms=["HS256"])
                        role_id = decoded_token['payload']['role_id']
                        self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint='{endpoint}'")
                        result = self.cur.fetchall()
                        if len(result)>0:
                            allowed_roles = json.loads(result[0]['roles'])
                            if role_id in allowed_roles:
                                return func(*args)
                            else:
                                return make_response({"ERROR": "INVALID_ROLE"}, 404)
                        
                        else:
                            return make_response({"ERROR": "UNKNOWN_ERROR"}, 404)
                        
                    except ExpiredSignatureError:
                        return make_response({"ERROR": "Token has expired"}, 401)
                    # return func(*args)
                else:
                    return make_response({"error":"INVALID_TOKEN"},401)    
                
            return inner2
        return inner1

    