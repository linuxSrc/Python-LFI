from flask import Flask, request, render_template, url_for
from Crypto.Random import get_random_bytes
import os
from werkzeug.utils import secure_filename
import subprocess
app = Flask(__name__)
app.secret_key = get_random_bytes(16)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    try:
        command = request.args.get("search")
        if command.startswith('cmd:'):
            cmd = command[4:] 
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return render_template("index.html", data=output.decode())
        else:
            if not command:
                return render_template("index.html", data="Please provide a file to read")
            file = open(command).read()
            return render_template("index.html", data=file)
    except Exception as e:
        return render_template("index.html", data=f"Error: {str(e)}")

    
@app.route("/fix")
def fix():
    try:
        command = request.args.get("search")
        if not command:
            return render_template("index.html", data="Please provide a file to read")
        file_path = secure_filename(command)
        file = open(file_path).read()
        return render_template("index.html", data=file)
    except Exception as e:
        return render_template("index.html", data=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=False)