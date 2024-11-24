from flask import Flask, request,render_template
from werkzeug.utils import secure_filename
from Crypto.Random import get_random_bytes
import os
import uuid

# App Configuration
app = Flask(__name__)
app.secret_key = get_random_bytes(16)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 # Set file size limit
app.config["UPLOAD_EXTENSIONS"] = [".jpg",".png",".jpeg",".pdf"] # Set allowed extensions

@app.route("/")
def home():
    return render_template("secure_upload.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files["file"]
        filename = secure_filename(file.filename) # Strip ../ from filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                response = 'File Type not Allowed!'
                return render_template("secure_upload.html",data=response)
                
            unique_filename = str(uuid.uuid4()) # Generate a unique filename to avoid overwriting existing files
            file.save('uploads/' + unique_filename)
            response = 'Upload Successful'
            return render_template("secure_upload.html",data=response)
    except Exception as e:
        response = f"{str(e)}" # Possible infomation disclosure if upload fails
        return render_template("secure_upload.html",data=response)

app.run('0.0.0.0',8000)
