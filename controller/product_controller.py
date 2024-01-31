from app import app
@app.route("/product/add")
def productAdd():
    return "This is product add operation"