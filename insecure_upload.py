from flask import Flask, request,render_template, send_from_directory
from Crypto.Random import get_random_bytes
import os
from werkzeug.utils import secure_filename

# App Configuration
app = Flask(__name__)
app.secret_key = get_random_bytes(16)
# Vulnerbility no file limit set
# Vulnerbility no allow list set

@app.route("/")
def home():
    return render_template("insecure_upload.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files["file"]
        filename = file.filename

        # filename = secure_filename(filename)
        # file.save(os.path.join('uploads', filename)) # Vulnerbility fixed by sanitizing the filename
        
        file.save('uploads/' + filename) # Vulnerbility file name not
        response = 'Upload Successful'
        
    except Exception as e:
        
        response = f"{str(e)}" # Possible infomation disclosure if upload fails
    
    return render_template("insecure_upload.html",data=response)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

app.run('0.0.0.0',8000)
