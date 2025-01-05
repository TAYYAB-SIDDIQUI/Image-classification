from flask import Flask,render_template,request,jsonify,redirect,url_for
import os
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
    return jsonify({"message":"Fole uploaded successfully","file_path":file_path}),200
    
if __name__=="__main__":
    app.run(debug=True)