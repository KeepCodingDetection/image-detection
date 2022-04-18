
from flask import Flask, request, jsonify
from prediction2 import foodDetection
import torch

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def parse_request():
    request_data = request.get_json() 
    ImageBase64 = request_data['image']
    fd = foodDetection()
    response_64 = fd.predict(ImageBase64,model)
    return jsonify(output=response_64)
    #return jsonify({"uuid":"prueba"})
    

if __name__ == "__main__":
    model=torch.hub.load('ultralytics/yolov5','yolov5s')
    #model=model
    app.run(debug=True, host='0.0.0.0', port= 8001)
