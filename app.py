import os
from flask import Flask, request, send_from_directory, render_template
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    images = os.listdir(UPLOAD_FOLDER)
    images = [file for file in images if file != '.DS_Store']
    return render_template("index.html", images=images)


class ImageUpload(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part"}, 400
        file = request.files['file']
        if file.filename == '':
            return {"message": "No selected file"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {"message": f"Image {filename} uploaded successfully"}, 201

class ImageRetrieve(Resource):
    def get(self, filename):
        if allowed_file(filename):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        else:
            return {"message": "Invalid file format"}, 400

api.add_resource(ImageUpload, '/api/upload')
api.add_resource(ImageRetrieve, '/api/<string:filename>')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=5000)
