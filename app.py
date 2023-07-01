import io
from PIL import Image
from flask import Flask, request, render_template
from ultralytics import YOLO
import torch
import os

app = Flask(__name__,template_folder="templates",static_folder='static')

# PEOPLE_FOLDER = os.path.join('static')
# app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
#  app.config['STATIC_FOLDER'] = PEOPLE_FOLDE

model = YOLO("final.pt")
def Convert(lst):
   res_dict = {}
   for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
        return res_dic

def file_to_dict(file_path):
    data_dict = {}
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                value, key = line.strip().split(' ')
                data_dict[key] = value
                
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    
    return data_dict

def cleardir(path = 'runs\classify'):
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))    
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/objectdetection", methods=["POST"])
def predict():
    if not request.method == "POST":
        return
    
    if request.files.get("image"):
        image_file = request.files["image"]
        # print(image_file)
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        results = model(img, save_txt = True)
        # print(type)
        img.save(r"static\images\temp.png")
        file_path = 'runs\classify\predict\labels.txt'  
        result = file_to_dict(file_path)
        # print(result)
        max_value = 0
        for key, value in result.items():
            # print(key, value)
            if float(value) > 0.5 and float(value) > max_value:
                max_value = float(value)
                max_pair = [ key.capitalize() , value]

        cleardir()
        # return result
        # max_pair.append("temp.png")
        return render_template('object_detection.html', result=max_pair)
    else:
        return {"error": "No image file provided"}

if __name__ == '__main__':
   # app.run()
   app.run(debug=True)
