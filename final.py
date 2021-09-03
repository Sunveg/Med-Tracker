from flask import Flask

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify,request

from werkzeug.security import generate_password_hash,check_password_hash

import bcrypt

import json

import random



app = Flask(__name__)

#bcrypt = Bcrypt(app)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/Users"

mongo = PyMongo(app)





@app.route('/addvaccine',methods=['POST']) 
def addvaccine():
    form = request.form
    patientId=form["id"]
    vac_name = form["vac_name"]
    vac_date = form["vac_date"]
    details = {"vaccine_name":vac_name, "vaccine_data":vac_date}
    mongo.db.patients.update({"id":patientId},{"$push" : {"vaccines":details}})

    mongo.db.vaccine_list.insert({"vac_name":vac_name,"vac_date":vac_date,"patient_id":patientId})
    return 'added'



@app.route('/vaccine_list',methods=['POST'])
#@app.route('/doctor_appointment_history')
def vaccine_list():
    
    # Prepare a dictionary object to hold the result of any processing
    result = []  # create a list instead of dict

    
    form=request.form
    #email=form["email"]
    #print(email)
    a=mongo.db.vaccine_list.find({"patient_id":form["id"]},{"_id":0})
    
    #a=mongo.db.doctor_appointments.find({},{"_id":0})

    for d in a:
        result.append(d) 
      

    print("1")
    print(result)
    return jsonify({"result":result}) 
    #return 'hello'




@app.route('/book_lab_appointment',methods=['POST'])
def book_lab_appointment():
    #print("ok")
    form=request.form
    lab_id=form["lab_id"]
    lab_name=form["lab_name"]
    date=form["date"]
    time=form["time"]
    diagnosis=form["diagnosis"]
    doctor_id=form["doctor_id"]
    patient_id=form["id"]
    #email=form["email"]
    #print(email)
    #password=form["password"]
    #password_hash=generate_password_hash(password)
    count=mongo.db.lab_appointments.count({"patient_id":patient_id}, {})
    appointment_id=patient_id+str(count)#+"_"+"lab"
    mongo.db.lab_appointments.insert({"lab_id":lab_id,"lab_name":lab_name,"date":date,"time":time,"diagnosis":diagnosis,"appointment_id":appointment_id,"doctor_id":doctor_id,"patient_id":patient_id})
    
    print("inserted")
    return 'inserted'  



@app.route('/book_doctor_appointment',methods=['POST'])
def book_doctor_appointment():
    #print("ok")
    form=request.form
    doctor_id=form["doctor_id"]
    doctor_name=form["doctor_name"]
    date=form["date"]
    time=form["time"]
    problem=form["problem"]
    #email=form["email"]
    patient_id=form["id"]
    #print(email)
    #password=form["password"]
    #password_hash=generate_password_hash(password)
    patientInfo = {"patientid":patient_id, "illness":problem, "time":time, "date":date}
    mongo.db.doctor.update({"id":doctor_id}, {"$push":{"requests":patientInfo}})

    count=mongo.db.doctor_appointments.count({"patient_id":patient_id}, {})
    appointment_id=patient_id+str(count)
    mongo.db.doctor_appointments.insert({"doctor_id":doctor_id,"doctor_name":doctor_name,"date":date,"time":time,"problem":problem,"appointment_id":appointment_id,"status":"pending","patient_id":patient_id})
    
    print("inserted")
    return 'inserted'  
   


#@app.route('/all', methods = ['GET'])
@app.route('/all')
def getType():

    # Prepare a dictionary object to hold the result of any processing
    result = []  # create a list instead of dict

    # Get hold of DB connection
     #db_connection = getDbConnection()
     #db = db_connection['OER']
    # Extract all records passed for the paramater that matches "Type": ie MOOC
     #oerType = request.args.get("oerType");
    # test to see that there is something in the string if so try to get a record
    # Not doing this test yet lets get it working with a known record first 

    a=mongo.db.doctor_data.find({},{"_id":0})

    for d in a:
        result.append(d) 
        #result.append(make_public_page(d))  # append to the list of dicts

       # print(d)
        #result.append(d)

    print("1")
    #result=json.dumps(result,default=str)
    #print(result)
    #return result
    #print(a)
    #return(json.dumps(a,default=str))
    return jsonify({"result":result})



@app.route('/lab_reports',methods=['POST'])
#@app.route('/doctor_appointment_history')
def lab_reports():
    
    # Prepare a dictionary object to hold the result of any processing
    result = []  # create a list instead of dict

    # Get hold of DB connection
     #db_connection = getDbConnection()
     #db = db_connection['OER']
    # Extract all records passed for the paramater that matches "Type": ie MOOC
     #oerType = request.args.get("oerType");
    # test to see that there is something in the string if so try to get a record
    # Not doing this test yet lets get it working with a known record first 
    
    form=request.form
    #email=form["email"]
    #print(email)
    a=mongo.db.lab_appointments.find({"email":form["email"]},{"_id":0})
    
    #a=mongo.db.doctor_appointments.find({},{"_id":0})

    for d in a:
        result.append(d) 
      

    print("1")
    print(result)
    return jsonify({"result":result}) 
    #return 'hello'    




@app.route('/doctor_appointment_history',methods=['POST'])
#@app.route('/doctor_appointment_history')
def doctor_appointment_history():
    
    # Prepare a dictionary object to hold the result of any processing
    result = []  # create a list instead of dict

    # Get hold of DB connection
     #db_connection = getDbConnection()
     #db = db_connection['OER']
    # Extract all records passed for the paramater that matches "Type": ie MOOC
     #oerType = request.args.get("oerType");
    # test to see that there is something in the string if so try to get a record
    # Not doing this test yet lets get it working with a known record first 
    
    form=request.form
    #email=form["email"]
    #print(email)
    a=mongo.db.doctor_appointments.find({"patient_id":form["id"]},{"_id":0})
    
    #a=mongo.db.doctor_appointments.find({},{"_id":0})

    for d in a:
        result.append(d) 
      

    print("1")
    print(result)
    return jsonify({"result":result}) 
    #return 'hello'


@app.route('/doctor_login',methods=['POST'])
def doctor_login():
    form=request.form
    email=form["email"]
    password=form["password"]
    

    if mongo.db.doctor.count({"email":email}, {}) == 1:
        x=mongo.db.doctor.find_one({"email":email})["password_hash"]
        if check_password_hash(x,password) :
          print("1")
          y=mongo.db.doctor.find_one({"email":email})["name"]
          myid = mongo.db.doctor.find_one({"email":email})["id"]
          #z=mongo.db.lab_data.find_one({"email":email})["username"]
          return jsonify({"response":{"status":"approved","email":email,"id":myid}})
          

        else:
            print("2")
            return jsonify({"response":{"status":"wrong_password"}})
            


    else:
        print("3")
        return jsonify({"response":{"status":"not_signed_up"}})
         
    
    
@app.route('/lab_login',methods=['POST'])
def lab_login():
    form=request.form
    email=form["email"]
    password=form["password"]



    if mongo.db.lab.count({"email":email}, {}) == 1:
        x=mongo.db.lab.find_one({"email":email})["password_hash"]
        if check_password_hash(x,password) :
          print("1")
          y=mongo.db.lab.find_one({"email":email})["name"]
          labid = mongo.db.lab.find_one({"email":email})["id"]
          #z=mongo.db.lab_data.find_one({"email":email})["username"]
          return jsonify({"response":{"status":"approved","email":email,"id":labid}})
          

        else:
            print("2")
            return jsonify({"response":{"status":"wrong_password"}})
            


    else:
        print("3")
        return jsonify({"response":{"status":"not_signed_up"}})



@app.route('/patient_login',methods=['POST'])
#@app.route('/patient_login')
def patient_login():
    
    form=request.form
    email=form["email"]
    password=form["password"]
    #print(email)
    #print(password)
    
    if mongo.db.patients.count({"email":email}, {}) == 1:
        x=mongo.db.patients.find_one({"email":email})["password_hash"]
        if check_password_hash(x,password) :
          print("1")
          y=mongo.db.patients.find_one({"email":email})["name"]
          patid = mongo.db.patients.find_one({"email":email})["id"]
          #z=mongo.db.lab_data.find_one({"email":email})["username"]
          return jsonify({"response":{"status":"approved","email":email,"id":patid}})
          

        else:
            print("2")
            return jsonify({"response":{"status":"wrong_password"}})
            


    else:
        print("3")
        return jsonify({"response":{"status":"not_signed_up"}})
        
        

    #print("4")    
    #return jsonify({"response":{"status":"approved","email":"sd","username":"pj"}})


@app.route('/doctor_signup',methods=['POST'])
def doctor_signup():
    form=request.form
    docid = random.randint(0,1000)
    docid = str(docid)
    name=form["name"]
    years_of_experience=form["years_of_experience"]
    practice_type=form["practice_type"]
    location=form["location"]
    email=form["email"]
    password=form["password"]
    password_hash=generate_password_hash(password)

    if mongo.db.doctor.count({"email":email}, {}) == 0:
     mongo.db.doctor.insert({"id":docid,"name":name,"location":location,"email":email,"password_hash":password_hash,"years_of_experience":years_of_experience,"practice_type":practice_type, "history":[], "appointments":[], "active":[], "requests":[]})
     print('inserted')
     return 'inserted'

    else:
        print('not inserted')
        return'email already present' 



@app.route('/lab_signup',methods=['POST'])
def lab_signup():
    form=request.form
    labid = random.randint(0,1000)
    labid = str(labid)
    name=form["name"]
    location=form["location"]
    email=form["email"]
    password=form["password"]
 
    password_hash=generate_password_hash(password)
    #print(check_password_hash(password_hash,"abcd"))
    if mongo.db.lab.count({"email":email}, {}) == 0:
     mongo.db.lab.insert({"name":name,"location":location,"email":email,"password_hash":password_hash, "id":labid, "history":[], "pending":[]})
     print('inserted')
     return 'inserted'

    else:
        print('not inserted')
        return'email already present' 


    
@app.route('/patient_signup',methods=['POST'])
def patient_signup():
    #print("ok")
    patid = random.randint(0,1000)
    patid = str(patid)
    form=request.form
    name=form["name"]
    age=form["age"]
    blood_group=form["blood_group"]
    gender=form["gender"]
    location=form["location"]
    email=form["email"]
    password=form["password"]
    password_hash=generate_password_hash(password)
    #print(check_password_hash(password_hash,"abcd"))
    if mongo.db.patients.count({"email":email}, {}) == 0:
     mongo.db.patients.insert({"name":name,"id":patid,"history":[],"pending":[],"age":age,"blood_group":blood_group,"gender":gender,"location":location,"email":email,"password_hash":password_hash, "vaccines":[], "reports":[], "current_reports":[]})
     print('inserted')
     return 'inserted'

    else:
        print('not inserted')
        return'email already present' 
              



@app.route('/add',methods=['POST'])
def add_user():
    _json = request.json
    _name = _json["name"]
    _email = _json['email']
    _password = _json['pwd']


  
    if _name and _email and _password and request.method =='POST':
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.user.insert({'name':_name,'email':_email,'pwd':_hashed_password})
        resp = jsonify("User added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify("User Deleted")
    resp.status_code;
    return resp

@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and _id and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.update({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'email':_email,'pwd':_hashed_password}})
        resp = jsonify("User updated")
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/fileupload', methods = ['GET', 'POST'])
def handle_request():
    return '''
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="text" name="name">
            <input type="file" name="image">
            <input type="submit">
        </form>
    '''

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/reports/<pat_id>',methods=['GET'])#---------send reports adjust according to your db
def reports(pat_id):
    user = mongo.db.patients.find_one({"id":pat_id})
    #print(users)
    reports = user["reports"]
    rep_names = []
    for x in reports:
        rep_names.append(x["name"]) #appends name of reports ["Blood-HBG","Sugar","LHT"]
    #print(send)
    resp = {"reports":rep_names}
    resp = dumps(resp)
    return resp

@app.route('/accept',methods=['POST'])
def accept():                                                                                                                                                                                                                                                              
    user = "user1"
    json = request.json
    name=json["name"]
    labid = json["labid"]
    con = mongo.db.labuser.find_one({"id":labid})
    pending = con["pending"]
    users = mongo.db.patients.find_one({"id":name})
#-------Patient database madhun current reports kad     
#-------users = {"id":"1234","Name":"user","reports":["Blood-HBG","Sugar","LHT"]}--ha format thev lab madhe save karayla
    pending.append(users)
    mongo.db.labuser.update({"name":user},{"$set":{"pending":pending}})
    return "request sent"

@app.route('/uploadpd',methods=['POST'])
def uploadpd():
    json = request.json
    filename = json["filename"]
    pid = json["pid"]
    labid = json["labid"]
    return "hi"

@app.route('/upload',methods=['POST'])#--------SAve filename and location in lab and patient db
def upload():
    data = request.files
    json = request.json
    print(data)
    print(json)
    #patientid = json["pid"]
    #labid = json["id"]
    print("kfnsdsak")
    if 'image' in request.files:
        file1 = request.files["image"]
        mongo.save_file(file1.filename, file1)
        #con = mongo.db.labuser.find_one({"id":i})
        #history = con["history"]
        #history.append({"id":id,'image_name':file1.filename})
        #con["history"]=history
        #pending = con["pending"]
        #print(pending)
        #delete = {}
        #for p in pending:
        #    if p["name"] == name:
        #        delete = p
        #pending.remove(delete)
        #con["pending"] = pending
        #mongo.db.labuser.save(con)
    elif 'filename' in request.files:    
        file1 = request.files["filename"]
        mongo.save_file(file1.filename, file1)
        #con = mongo.db.labuser.find_one({"name":"user1"})
        #history = con["history"]
        #history.append({"name":name,'image_name':file1.filename})
        #con["history"]=history
        #pending = con["pending"]
        #delete = {}
        #for p in pending:
        #    if p["name"] == name:
        #        delete = p
        #pending.remove(delete)
        #con["pending"] = pending
        #mongo.db.labuser.save(con)
    return "done"

@app.route('/getlist/<id>',methods=['GET'])
def getlist(id):
    json = request.json
    #users = mongo.db.labuser.find_one({"id":id})
    #send =users["pending"]
    #dic = {"pending":send}
    dic = {"pending":[{"id":"1234","Name":"user","reports":"Blood-HBG"},
		{"id":"1234","Name":"user","reports":"Sugar-level"},
		{"id":"1234","Name":"user","reports":"LHT"},
        {"id":"2234","Name":"user","reports":"Blood-HBG"}]}
    resp = dumps(dic) 
    return resp  

@app.route('/history/<id>',methods=['GET']) 
def history(id):
    json = request.json
    #name=json["name"]
    #users = mongo.db.labuser.find_one({"name":"user1"})
    #send =users["history"]
    #dic = {"history":send}
    #print(dic)
    dic={"history":[{"id":"1234","Name":"user","reports":"Blood-HBG","filename":"438.pdf"}]}
    resp = dumps(dic) 
    return resp

@app.route('/labdata/<id>',methods=['GET'])
def labdata(id): 
    json = request.json
    labId=id
    #labDetails = mongo.db.lab.find_one({"id":labId}) #found the correct doctor account here from database
    #Name = labDetails["Lab_Name"]
    #email = labDetails["email"]
    #location = labDetails["location"]
    #dic = {"Name":Name,"email":email,"location":location}
    dic = {"Data":{"Name":"Name","email":"email","Location":"location"}}
    resp = dumps(dic)
    return resp

@app.route('/doctordata/<docid>',methods=['POST', 'GET'])
def doctordata(docid): 
    doctorDetails = mongo.db.doctor.find_one({"id":int(docid)})
    print(doctorDetails)
    print(docid) #found the correct doctor account here from database
    Name = doctorDetails["name"]
    email = doctorDetails["email"]
    Experience = doctorDetails["years_of_experience"]
    Type = doctorDetails["practice_type"]
    location = doctorDetails["location"]
    dic = {"Name":Name,"email":email,"location":location,"Type":Type,"YoE":Experience}
    resp = dumps(dic)
    return resp

    #----------------------------NEW FUNCTIONS-------------------------------

@app.route('/prescribe',methods=['POST'])
def prescribe():
    form = request.form
    prescription = form["prescription"]
    reports = form["reports"]
    date = form["date"]
    doctorId = form["docid"]
    patientId = form["id"]
    record = {"doctorId":doctorId, "reports":reports,"prescription":prescription, "date":date}
    #mongo.db.patients.update({"id":patientId}, {"$push" : {"prescriptions":record}})
    record_doctor = {"patientId":patientId,"reports":reports, "prescription":prescription, "date":date}
    
    mongo.db.patient_prescription.insert({"doctor_id":doctorId,"patient_id":patientId,"prescription":prescription,"date":date})

    print(record)
    print(record_doctor)
    #mongo.db.doctor.update({"id":doctorId}, {"$push" : {"prescriptions":record_doctor}})
    return 'Prescription sent successfully'


@app.route('/prescriptions',methods=['POST'])
def prescriptions():
    form = request.form
    patientId = form["id"]
    result=[]
    #patient = mongo.db.patients.find_one({"id":patientId})
    #presc = patient["prescriptions"]
    #resp = dumps(presc)
    #print("Here are the prescriptions")
    #return resp

    a=mongo.db.patient_prescription.find({"patient_id":patientId},{"_id":0})
    
    #a=mongo.db.doctor_appointments.find({},{"_id":0})

    for d in a:
        result.append(d) 
      

    print("1")
    print(result)
    return jsonify({"result":result})     

@app.route('/viewprescription/<id>',methods=['GET'])
def viewprescription(id):
    form = request.form
    print(id)
    #patientId = form["id"]
    #patient = mongo.db.patients.find_one({"id":patientId})
    #presc = patient["prescriptions"]
    presc = {"Medicines":["1","2","3","4"],"Reports":[{"Report_Name":"Sugar","Filename":"438.pdf"},
                                                        {"Report_Name":"BP","Filename":"438.pdf"}]}
    resp = dumps(presc)
    print("Here are the prescriptions")
    return resp
#1 ACTIVE PATIENTS:
@app.route('/active',methods=['GET','POST']) #volley will send doctor id
def active():
    json = request.json
    doctorId=json["id"]
    doctorDetails = mongo.db.doctor.find_one({"id":doctorId}) #found the correct doctor account here from database
    activePatients = doctorDetails["active"] #access his active patient list
    send = activePatients
    resp = dumps(send)
    return resp

#2 Treated Patients updation
@app.route('/treated/<id>',methods=['GET','POST']) #get patient id and doctor id from volley android side
def treated(id): #this function will take the patientId from active to history as they are successfully treated and return active patient list
    json = request.json
    #doctorId=json["doctorId"]
    #patientId = json["patientId"]
    #mongo.db.doctor.update({"id":doctorId},{"$push" : {"history":patientId}}) #add the patientId to history
    #mongo.db.doctor.update({"id":doctorId},{"$pull" : {"active":patientId}}) #delete the patientID from active
    #con = mongo.db.doctor.find_one({"id":doctorId})
    #activePatients = con["active"]
    #send = activePatients
    send = {"treated":[{"patientId":"100","Name":"headache"},
                    {"patientId":"101","Name":"headache"}]}
    resp = dumps(send)
    return resp

#3 Send Patient data when clicked
@app.route('/patientdata',methods=['POST']) #when doctor clicks on patient name, this will send the patient details...volley will take the patient id
def patientdata():
    json = request.json
    patientId=json["id"]
    patient = mongo.db.patients.find_one({"id":patientId},{"password":0}) #found the correct patient
    dic = {"patientData" : patient}
    print(dic)
    resp = dumps(dic)
    return resp

#4 Appointment request from patient
@app.route('/requestappointment', methods=['POST','GET']) #patient will fill an appointment form and doctor can view it from requests
def requestAppointment():
    form = request.form
    patientId = form["id"]
    time = form["time"]
    date = form["date"]
    doctorId = form["doctor"]
    illness = form["illness"]
    patientInfo = {"patientid":patientId, "illness":illness, "time":time, "date":date}
    mongo.db.doctor.update({"id":doctorId}, {"$push":{"requests":patientInfo}})
    print("Your appointment request is sent. You will get a notification once doctor accepts!")
    return 'done'

#5 View appointment requests for doctor
@app.route('/viewRequests/<id>', methods=['GET']) 
def viewRequests(id):
    #doctorId = json["id"]
    #doctor = mongo.db.doctor.find_one({"id":doctorId})
    #req = doctor["requests"]
    #print(req)
    req={"requests":[{"patientId":"100","illness":"headache","time":"10 am","data":"17 May"},
                    {"patientId":"100","illness":"headache","time":"10 am","data":"17 May"}]}
    resp = dumps(req)
    return resp

#view appointments
@app.route('/viewappointments/<id>', methods=['GET']) 
def viewappointments(id):
    json = request.json
    #doctorId = json["id"]
    #doctor = mongo.db.doctor.find_one({"id":doctorId})
    #req = doctor["appointments"]
    req={"appointments":[{"patientId":"100","Name":"headache"},
                    {"patientId":"101","Name":"headache"}]}
    resp = dumps(req)
    return resp

#6 Accept/Decline requests
@app.route('/acceptReject', methods=['POST']) #show 2 buttons in android accept or reject and store bool value in accept variable and send it here
def acceptReject():
    json = request.json
    value = json["accept"] # true or false
    patientId = json["id"]
    doctorId = json["docid"]
    #if value=="True":
     #   mongo.db.doctor.update({"id":doctorId},{"$push" : {"appointments":patientId}})
     #   mongo.db.doctor.update({"id":doctorId},{"$push" : {"active":patientId}})
     #   mongo.db.doctor.update({"id":doctorId},{"$pull" : {"requests": {"patientid":patientId}}})
     #   return ' appointment accepted'
        #notify patient that appointment is fixed
    #else:
      #  mongo.db.doctor.update({"id":doctorId},{"$pull" : {"requests": {"patientid":patientId}}})
      #  return ' appointment declined'
        #notify patient their appointment is rejected



if __name__ == "__main__":
   # app.run()
    app.run(debug=True)