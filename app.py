from flask import Flask,render_template,request,jsonify,redirect,url_for
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
model=load_model("placerecognition.h5")
app=Flask(__name__)
UPLOAD_FOLDER="uploads"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/upload",methods=["POST"])
def upload_file():
    if "images" not in request.files:
        return jsonify({"error":"NO File part"}),400
    file=request.files["images"]
    if file.filename=="":
        return jsonify({"error":"NO File PART"}),400
    file_path=os.path.join(app.config["UPLOAD_FOLDER"],file.filename)
    file.save(file_path)
    img_path=file_path
    img_height,img_width=128,128
    class_names=['cloudy', 'desert', 'green_area', 'water']
    img=image.load_img(img_path,target_size=(img_height,img_width))
    img_array=image.img_to_array(img)
    img_array=img_array/255.0
    img_array=np.expand_dims(img_array,axis=0)
    predictions=model.predict(img_array)
    predictied_cl=np.argmax(predictions,axis=1)[0]
    confidence=np.max(predictions)
    return f"""
    <img src="{file_path}" alt="your img">
    <p>{class_names[predictied_cl]}</p><br>
    <p>{confidence*100 :.2f}</p>
    """
    
if __name__=="__main__":
    app.run(debug=True)