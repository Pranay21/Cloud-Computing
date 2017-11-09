# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#REFERENCES
#http://stackoverflow.com/questions/27628053/uploading-and-downloading-files-with-flask
#http://code.runnable.com/UiIdhKohv5JQAAB6/how-to-download-a-file-generated-on-the-fly-in-flask-for-python
#http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
#http://pythoncentral.io/hashing-files-with-python/
import os,time
from flask import Flask, jsonify, request, render_template, make_response, redirect,url_for
from cloudant.client import Cloudant
import hashlib
from mimetypes import MimeTypes

USERNAME = '8449445a-8fcb-4470-8f88-3803ba8f7c14-bluemix'
PASSWORD = 'e31f8d442090ad98ba283b1d047039bc9671709f7577336356ca06be7e450e0b'
URL = "https://8449445a-8fcb-4470-8f88-3803ba8f7c14-bluemix:e31f8d442090ad98ba283b1d047039bc9671709f7577336356ca06be7e450e0b@8449445a-8fcb-4470-8f88-3803ba8f7c14-bluemix.cloudant.com"
client = Cloudant(USERNAME, PASSWORD, url=URL)
client.connect()
dbs=  client.all_dbs()
print dbs
for db in dbs:
    print  str(db)
    if str(db) == 'my_database':
        temp = 1
        break
    else:
        temp =0


if temp==1:
    my_database = client['my_database']
else:
    my_database = client.create_database('my_database')


app = Flask(__name__)

@app.route('/')
def Welcome():
    return render_template('index.html')

@app.route('/upload/', methods=['POST','GET'])
def upload():

    version_number=1
    if request.method=='POST':
     file = request.files['myFile']
     de=request.form['desc']
     file_name = file.filename
    print file
    if file_name != "":
        hasher = hashlib.md5()
        buf = file.read()
        hasher.update(buf)
        hash_value=hasher.hexdigest()
        last_modified_time = time.asctime(time.localtime(time.time()))
    else:
        return render_template('result.html',result="Please select a file.")

    for document in my_database:
        if document['file_name']== file_name:
            if document['hash_value']== hash_value:
                return render_template('result.html',result="File already Exists")
            else:
                if document['version_number']== version_number:
                       version_number=document['version_number']+1


    file_Info = {
         'hash_value': hash_value,
         'file_name': file_name,
         'version_number': version_number,
         'lastModifiedDate': last_modified_time,
        'description' : de
    }

    my_document = my_database.create_document(file_Info)
    mime = MimeTypes()
    content_type = mime.guess_type(file_name)
    my_document.put_attachment(file_name, content_type[0], buf)
    return render_template('result.html',result="File uploaded successfully!!")



@app.route('/list/' ,methods=['POST','GET'])
def list():
    dirlist = os.listdir("E:\Quiz3-2.30\Quiz3-2.30")
    print dirlist
    return render_template('list.html',  file_list= dirlist)

@app.route('/view/' ,methods=['GET'])
def view():
	return render_template('view.html', documents = my_database)

@app.route('/download/<id>/', methods=['GET'])
def download(id):
	my_document = my_database[id]
	file_name = my_document['file_name']
	file_contents = my_document.get_attachment(file_name)
	response = make_response(file_contents)
	response.headers["Content-Disposition"] = "attachment; filename="+file_name
	return response
@app.route('/delete/<id>/' ,methods=['GET'])
def delete(id):
	my_document = my_database[id]
	my_document.delete()
	return redirect(url_for('view'))

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
