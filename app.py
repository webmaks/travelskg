from flask import Flask, jsonify, request
import mysql.connector as mysql
import os
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_pyfile('config.py')


DBNAME = app.config["DBNAME"]
DBUSER = app.config["DBUSER"]
DBPASS = app.config["DBPASS"]
#db = mysql.connect(host='db', database=DBNAME, user=DBUSER, password=DBPASS, use_pure=False, buffered=True)
db = mysql.connect(host='db', database=DBNAME, user=DBUSER, password=DBPASS, buffered=True)
success = { "result": "Done"  }

@app.route('/api')
def api():
    people = [{'name': 'inTourist', 'tour': 'Ala-Archa'},{'name': 'KGTrips', 'tour': 'Pik of Lenin'},
          {'name': 'TourizmKG', 'tour': 'Ala-Kol'}]
    return jsonify(people)

# Getting all companies
@app.route("/api/get/company")
def getAllCompany():
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM company
               ''')
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'name': result[1],
                  'description': result[2],
                  'mobile': result[3],
                  'instagram': result[4],
                  'user_id': result[5],
                  'logo': result[6]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Getting  company by id
@app.route("/api/get/company/<id>")
def getCompany(id):
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM company WHERE id = %s
               ''',(id,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'name': result[1],
                  'description': result[2],
                  'mobile': result[3],
                  'instagram': result[4],
                  'user_id': result[5],
                  'logo': result[6]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload[0]), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Getting  companies by USER's id
@app.route("/api/get/company/user/<id>")
def getCompanyUserID(id):
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM company
                WHERE user_id = %s
               ''',(id,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'name': result[1],
                  'description': result[2],
                  'mobile': result[3],
                  'instagram': result[4],
                  'user_id': result[5],
                  'logo': result[6]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Adding new company
@app.route("/api/add/company", methods = ['POST', 'GET'])
def addCompany():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        name = request_data['name']
        description = request_data['description']
        mobile = request_data['mobile']
        instagram = request_data['instagram']
        user_id = request_data['user_id']
        logo = request_data['logo']

        cur = db.cursor()
        cur.execute(''' INSERT INTO company
                    (name,description,mobile,instagram,user_id,logo)
                    VALUES (%s,%s,%s,%s) ''',
                    (name,description,mobile,instagram,user_id,logo))
        db.commit()
        return f"Done"

# Eding company
@app.route("/api/edit/company/<id>", methods = ['POST', 'GET'])
def editCompany(id):
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        name = request_data['name']
        description = request_data['description']
        mobile = request_data['mobile']
        instagram = request_data['instagram']
        user_id = request_data['user_id']
        logo = request_data['logo']
        cur = db.cursor()
        cur.execute(''' UPDATE company SET name = %s,
                    description = %s,
                    mobile = %s,
                    instagram = %s,
                    user_id = %s,
                    logo = %s,
                    WHERE id = %s ''',
                    (name,description,mobile,instagram,user_id,logo,id))
        db.commit()
        return jsonify(success)

# Delete company
@app.route("/api/del/company/<id>", methods = ['POST', 'GET'])
def delCompany(id):

    if request.method == 'GET':
        return "This method is not allowed"

    cur = db.cursor()
    cur.execute('''
               DELETE FROM company WHERE id = %s)
               ''',(id,))
    return jsonify(success), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Getting all users
@app.route("/api/get/users")
def getAllUsers():
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  users
               ''')
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'name': result[1],
                  'surname': result[2],
                  'uid': result[3],
                  'avatar': result[4],
                  'type': result[5]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Get user by uid
@app.route("/api/get/user/<uid>")
def getUser(uid):
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  users
               WHERE uid=%s LIMIT 1
               ''',(uid,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                  'name': result[1],
                  'surname': result[2],
                  'uid': result[3],
                  'avatar': result[4],
                  'type': result[5]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload[0]), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Adding new user
@app.route("/api/add/user", methods = ['POST', 'GET'])
def addUser():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "name" in request_data:
            user_name = request_data['name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

        if "surname" in request_data:
            user_surname = request_data['surname']
        else:
            return jsonify({"error": "Forgot something like surna...",}), 403

        if "uid" in request_data:
            user_uid = request_data['uid']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "avatar" in request_data:
            user_avatar = request_data['avatar']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "type" in request_data:
            user_type = request_data['type']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        cur = db.cursor()
        cur.execute(''' INSERT INTO  users
                    (name,surname,uid,avatar,type)
                    VALUES (%s,%s,%s,%s,%s) ''',
                    (user_name,user_surname,user_uid,user_avatar,user_type))
        db.commit()
        return  jsonify(success)

# Edit user
@app.route("/api/edit/user/<id>", methods = ['POST', 'GET'])
def editUser(id):
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "name" in request_data:
            user_name = request_data['name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

        if "surname" in request_data:
            user_surname = request_data['surname']
        else:
            return jsonify({"error": "Forgot something like su...",}), 403

        if "uid" in request_data:
            user_uid = request_data['uid']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "avatar" in request_data:
            user_avatar = request_data['avatar']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "type" in request_data:
            user_type = request_data['type']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        cur = db.cursor()
        cur.execute(''' UPDATE users SET name = %s,
                    surname = %s,
                    uid = %s,
                    avatar = %s,
                    type = %s WHERE id = %s ''',
                    (user_name,user_surname,user_uid,user_avatar,user_type,id))
        db.commit()
        return  jsonify(success)

# Getting all trips
@app.route("/api/get/trips")
def getAllTrips():
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  trip
               ''')
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                    'description': result[1],
                    'location': result[2],
                    'region': result[3],
                    'type': result[4],
                    'duration_time': result[5],
                    'duration_route': result[6],
                    'difficulty': result[7],
                    'climb': result[8],
                    'requirement': result[9],
                    'included': result[10],
                    'info_mobile': result[11],
                    'warning': result[12]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Get all trips by Company_ID
@app.route("/api/get/trip/company/<id>")
def getAllTripsByCompanyID(id):
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  trip
               WHERE company_id = %s''',(id,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                    'description': result[1],
                    'location': result[2],
                    'region': result[3],
                    'type': result[4],
                    'duration_time': result[5],
                    'duration_route': result[6],
                    'difficulty': result[7],
                    'climb': result[8],
                    'requirement': result[9],
                    'included': result[10],
                    'info_mobile': result[11],
                    'warning': result[12],
                    'company_id': result[13],
                    'main_image': result[14]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Get one trip by ID
@app.route("/api/get/trip/<id>")
def getTripByID(id):
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  trip
               WHERE id = %s''',(id,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                    'description': result[1],
                    'location': result[2],
                    'region': result[3],
                    'type': result[4],
                    'duration_time': result[5],
                    'duration_route': result[6],
                    'difficulty': result[7],
                    'climb': result[8],
                    'requirement': result[9],
                    'included': result[10],
                    'info_mobile': result[11],
                    'warning': result[12],
                    'company_id': result[13],
                    'main_image': result[14]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload[0]), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Getting sorted trips
@app.route("/api/get/sort/trips/<sorted>")
def getAllTripsSorted(sorted):
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  trip
               ORDER by %s ''',(sorted,))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                    'description': result[1],
                    'location': result[2],
                    'region': result[3],
                    'type': result[4],
                    'duration_time': result[5],
                    'duration_route': result[6],
                    'difficulty': result[7],
                    'climb': result[8],
                    'requirement': result[9],
                    'included': result[10],
                    'info_mobile': result[11],
                    'warning': result[12]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Paginator for trips
@app.route("/api/get/trips/<id>")
def getPageTrips(id):
   startPage = int(id) * 5
   endPage = startPage + 5
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  trip
               WHERE id >= %s and id <= %s ''',(startPage, endPage))
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                    'description': result[1],
                    'location': result[2],
                    'region': result[3],
                    'type': result[4],
                    'duration_time': result[5],
                    'duration_route': result[6],
                    'difficulty': result[7],
                    'climb': result[8],
                    'requirement': result[9],
                    'included': result[10],
                    'info_mobile': result[11],
                    'warning': result[12],
                    'company_id': result[13],
                    'main_image': result[14]
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Adding new trip
@app.route("/api/add/trip", methods = ['POST', 'GET'])
def addTrip():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        description = request_data['description']
        location = request_data['location']
        region = request_data['region']
        type = request_data['type']
        duration_time = request_data['duration_time']
        duration_route = request_data['duration_route']
        difficulty = request_data['difficulty']
        climb = request_data['climb']
        requirement = request_data['requirement']
        included = request_data['included']
        info_mobile = request_data['info_mobile']
        warning = request_data['warning']

        cur = db.cursor()
        cur.execute(''' INSERT INTO  users
                    (description,location,region,type,
                    duration_time,duration_route,difficulty,climb,
                    requirement,included,info_mobile,warning)
                    VALUES (%s,%s,%s,%s,
                            %s,%s,%s,%s,
                            %s,%s,%s,%s) ''',
                    (description,location,region,type,
                    duration_time,duration_route,difficulty,climb,
                    requirement,included,info_mobile,warning))
        db.commit()
        return  jsonify(success)

# Getting all trip_schedules
@app.route("/api/get/trip_scheduler")
def getAllTripScheduler():
   cur = db.cursor()
   cur.execute('''
               SELECT * FROM  trip_scheduler
               ''')
   rv = cur.fetchall()
   payload = []
   content = {}
   for result in rv:
       content = {'id': result[0],
                    'trip_id': result[1],
                    'start_datetime': result[2],
                    'finish_datetime': result[3],
                    'price': result[4],
                    'meeting_point': result[5],
                    'meeting_point_lat': result[6],
                    'meeting_point_lng': result[7],
                    'seats': result[8],
                  }
       payload.append(content)
       content = {}
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Adding new trip_schedules
@app.route("/api/add/trip_scheduler")
def addTripScheduler():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()
        trip_id = request_data['trip_id']
        start_datetime = request_data['start_datetime']
        finish_datetime = request_data['finish_datetime']
        price = request_data['price']
        meeting_point = request_data['meeting_point']
        meeting_point_lat = request_data['meeting_point_lat']
        meeting_point_lng = request_data['meeting_point_lng']
        seats = request_data['seats']

        cur = db.cursor()
        cur.execute(''' INSERT INTO  trip_scheduler
                    (trip_id, start_datetime, finish_datetime,
                    price,meeting_point,meeting_point_lat,
                    meeting_point_lng,seats)
                    VALUES (%s,%s,%s,%s,
                            %s,%s,%s,%s) ''',
                    (trip_id, start_datetime, finish_datetime,
                    price,meeting_point,meeting_point_lat,
                    meeting_point_lng,seats))
        db.commit()
        return  jsonify(success)

# Eding trip_scheduler
@app.route("/api/edit/trip_scheduler/<id>", methods = ['POST', 'GET'])
def editTripScheduler(id):
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        trip_id = request_data['trip_id']
        start_datetime = request_data['start_datetime']
        finish_datetime = request_data['finish_datetime']
        price = request_data['price']
        meeting_point = request_data['meeting_point']
        meeting_point_lat = request_data['meeting_point_lat']
        meeting_point_lng = request_data['meeting_point_lng']
        seats = request_data['seats']
        cur = db.cursor()
        cur.execute(''' UPDATE trip_scheduler SET trip_id = %s,
                    start_datetime = %s,
                    finish_datetime = %s,
                    price = %s,
                    meeting_point = %s,
                    meeting_point_lat = %s,
                    meeting_point_lng = %s,
                    seats = %s
                    WHERE id = %s ''',
                    (trip_id,start_datetime,finish_datetime,price,
                    meeting_point,meeting_point_lat,meeting_point_lng,seats,id))
        db.commit()
        return jsonify(success)

# List directory Files
@app.route("/api/files/<file>")
def listFiles(file):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "./Files/", file)
    data = json.load(open(json_url))
    #return render_template('showjson.jade', data=data)
    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}

app.run(host='0.0.0.0', port=7000)

