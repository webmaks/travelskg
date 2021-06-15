from flask import Flask, jsonify, request
import mysql.connector as mysql

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_pyfile('config.py')


DBNAME = app.config["DBNAME"]
DBUSER = app.config["DBUSER"]
DBPASS = app.config["DBPASS"]
db = mysql.connect(host='db', database=DBNAME, user=DBUSER, password=DBPASS, use_pure=False)
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
                  'instagram': result[4]
                  }
       payload.append(content)
       content = {}
   cur.close()
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
                  'instagram': result[4]
                  }
       payload.append(content)
       content = {}
   cur.close()
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Adding new company
@app.route("/api/add/company", methods = ['POST', 'GET'])
def addCompany():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "name" in request_data:
            company_name = request_data['name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

        if "description" in request_data:
            company_desc = request_data['description']
        else:
            return jsonify({"error": "Forgot something like de...",}), 403

        if "mobile" in request_data:
            company_mob = request_data['mobile']
        else:
            return jsonify({"error": "Forgot something like mo...",}), 403

        if "instagram" in request_data:
            company_inst = request_data['instagram']
        else:
            return jsonify({"error": "Forgot something like in...",}), 403

        cur = db.cursor()
        cur.execute(''' INSERT INTO company
                    (name,description,mobile,instagram)
                    VALUES (%s,%s,%s,%s) ''',
                    (company_name,company_desc,company_mob,company_inst))
        db.commit()
        cur.close()
        return f"Done"

# Eding company
@app.route("/api/edit/company/<id>", methods = ['POST', 'GET'])
def editCompany(id):
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "name" in request_data:
            company_name = request_data['name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

        if "description" in request_data:
            company_desc = request_data['description']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "mobile" in request_data:
            company_mob = request_data['mobile']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "instagram" in request_data:
            company_inst = request_data['instagram']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        cur = db.cursor()
        cur.execute(''' UPDATE company SET name = %s,
                    description = %s,
                    mobile = %s,
                    instagram = %s WHERE id = %s ''',
                    (company_name,company_desc,company_mob,company_inst,id))
        db.commit()
        cur.close()
        return f"Done"

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
   cur.close()
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
   cur.close()
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
        cur.close()
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
        cur.close()
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
   cur.close()
   return jsonify(payload), 200, {'Content-Type': 'application/json; charset=utf-8'}

# Adding new trip
# Adding new user
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
        cur.close()
        return  jsonify(success)





app.run(host='0.0.0.0', port=5000)

