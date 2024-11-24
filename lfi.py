
from flask import Flask,request,render_template,url_for
from Crypto.Random import get_random_bytes
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = get_random_bytes(16)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    try:
        command = request.args.get("search")
        file = open(command).read()  #LFI Vulnerbility unsanitized data
    except Exception as e:
        file = f'{str(e)}' # Possible infomation disclosure if upload fails
    return render_template("index.html",data=file)     
    
@app.route("/fix")
def fix():
    try:
        command = request.args.get("search")
        file_path = secure_filename(command) # Strips ../
        #print(file_path)
        file = open(file_path).read()
    except Exception as e:
        file = f'{str(e)}' # Possible infomation disclosure if upload fails
    return render_template("index.html",data=file)
     
app.run('0.0.0.0',8000)


