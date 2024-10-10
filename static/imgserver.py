import io
import json                    
import base64                  
import logging             
import numpy as np
import os
import zipfile
from flask import Flask, request, jsonify, abort, render_template
from flask import send_file

from PIL import Image

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)
  
  
#http://192.168.32.162:8080/
@app.route('/')
def init():
    return render_template("info.html")

@app.route('/filenum', methods=['POST'])
def setup():
    rdate = request.args['dateType']
    #date = int(rdate)

    rid = request.args["deviceType"]
    #deviceid = int(rid)

    #file = open("setup.txt", "w")
    #file.write(pdate +',' + pdeviceid)

    print("rdate=",rdate)
    print("rid=",rid)

    file_path = './upload/' + rdate + '/'
    zip_filename = rid + '_' + rdate + '.zip'

    print("file_path=", file_path)
    print("zip_filename=", zip_filename)

    fileNum = 0
    for file in os.listdir(file_path):

        if file.endswith('.jpg'):
            #print("same folder filename=",file)
        
            if rid in file:
                print("specific ID=",file)
                fileNum += 1
    
    return "<h2>업로드 할수 있는 파일의 갯수는 %d </h2>" % (fileNum)

@app.route('/imageupload', methods=['POST'])
def image_upload():         
    # print(request.json)      
    if not request.json or 'image' not in request.json: 
        abort(400)
             
    # get the base64 encoded string
    im_b64 = request.json['image']

    fname = request.json['fname']
    print('fname=',fname)
    
    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    img.save(fname,"JPEG")
    
    # PIL image object to numpy array
    img_arr = np.asarray(img)      
    print('img shape', img_arr.shape)

    # process your img_arr here    
    
    # access other keys of json
    # print(request.json['other_key'])

    result_dict = {'output': 'output_key'}
    return result_dict
    
#http://192.168.32.162:8080/downinfo?date=20241010&deviceid=1001

@app.route("/downinfo")
def downinfo():

    rdate = request.args['date']
    rid = request.args['deviceid']

    print("rdate=",rdate)
    print("rid=",rid)

    file_path = './upload/' + rdate + '/'
    zip_filename = rid + '_' + rdate + '.zip'

    print("file_path=", file_path)
    print("zip_filename=", zip_filename)

    fileNum = 0
    for file in os.listdir(file_path):

        if file.endswith('.jpg'):
            #print("same folder filename=",file)
        
            if rid in file:
                print("specific ID=",file)
                fileNum += 1
    

    data = {'fileNum' : fileNum}

    return jsonify(data)

#http://192.168.32.162:8080/download?date=20241010&deviceid=1001

@app.route("/download")
def download():

    rdate = request.args['date']
    rid = request.args['deviceid']

    print("rdate=",rdate)
    print("rid=",rid)

    file_path = './upload/' + rdate + '/'
    zip_filename = rid + '_' + rdate + '.zip'

    print("file_path=", file_path)
    print("zip_filename=", zip_filename)

    zip_file = zipfile.ZipFile(file_path + zip_filename,'w')

    for file in os.listdir(file_path):
        if file.endswith('.jpg'):
            #print("same folder filename=",file)
            
            if rid in file:
                print("specific ID=",file)
                zip_file.write(os.path.join(file_path,file), compress_type=zipfile.ZIP_DEFLATED)
          
    zip_file.close()
    
    return send_file(file_path + zip_filename, mimetype="text/plain", as_attachment=True)



def run_server_api():
    app.run(host='0.0.0.0', port=8080)
  
  
if __name__ == "__main__":     
    run_server_api()
