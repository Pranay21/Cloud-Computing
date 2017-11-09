import json
import boto3

s3 = boto3.resource('s3')
content_object = s3.Object('sxa0453', 'users.json')
file_content = content_object.get()['Body'].read()
json_content = json.loads(file_content)
for users in json_content['users']:
    print users['username']
    # now song is a dictionary

app.route('/login/',methods=['POST','GET'])
def login():
    if request.method=='POST':
     u_name = request.form['u_name']
     print u_name

     u_pass = request.form['p_name']
     print u_pass
    content_object = s3.Object('sxa0453', 'users.json')
    file_content = content_object.get()['Body'].read()
    json_content = json.loads(file_content)
    for users in json_content['users']:
        print users['username']

    return render_template('login.html')



@app.route('/index/')
def index():
    return render_template('index.html')