from app import app
from model.user_model import user_model
from flask import request
from datetime import datetime

obj = user_model()

# getall user
@app.route("/user/getall")
def user_getall_controller():
    return obj.user_getall_model()
# add user
@app.route("/user/adduser",methods=["POST"])
def user_adduser_controller():
    return obj.user_adduser_model(request.form)
# update user
@app.route("/user/updateuser",methods=["PUT"])
def user_updateuser_controller():
    return obj.user_updateuser_model(request.form)
# delete user
@app.route("/user/delete/<id>",methods=["DELETE"])
def user_deleteuser_controller(id):
    return obj.user_deleteuser_model(id)
# update user using patch
@app.route("/user/patch/<id>",methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form,id)

# pagination
@app.route("/user/getall/limit/<limit>/page/<page>",methods=["GET"])
def user_pagination_controller(limit, page):
    return obj.user_pagination_model(limit, page)

# uploading file
@app.route("/user/<uid>/upload/avatar",methods=["PUT"])
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    uniqueFilename = str(datetime.now().timestamp()).replace(".","")
    fileNameSplit = file.filename.split(".")
    ext = fileNameSplit[len(fileNameSplit) -1]
    finalFilePath = f"uploads/{uniqueFilename}.{ext}"
    file.save(finalFilePath)
    return obj.user_upload_avatar_model(uid,finalFilePath)

@app.route("/user/<id>")
def user_getuser_controller(id):
    return obj.user_getuser_model(id)