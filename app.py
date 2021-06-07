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

# Adding new company
@app.route("/api/add/company", methods = ['POST', 'GET'])
def addCompany():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "company_name" in request_data:
            company_name = request_data['company_name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

        if "company_desc" in request_data:
            company_desc = request_data['company_desc']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "company_mob" in request_data:
            company_mob = request_data['company_mob']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "company_inst" in request_data:
            company_inst = request_data['company_inst']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        cur = db.cursor()
        cur.execute(''' INSERT INTO company
                    (name,description,mobile,instagram)
                    VALUES (%s,%s,%s,%s) ''',
                    (company_name,company_desc,company_mob,company_inst))
        db.commit()
        cur.close()
        return f"Done"

# Eding new company
@app.route("/api/edit/company", methods = ['POST', 'GET'])
def editCompany():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "company_id" in request_data:
            company_id = request_data['company_id']
        else:
            return jsonify({"error": "Forgot something like id...",}), 403

        if "company_name" in request_data:
            company_name = request_data['company_name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

        if "company_desc" in request_data:
            company_desc = request_data['company_desc']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "company_mob" in request_data:
            company_mob = request_data['company_mob']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403

        if "company_inst" in request_data:
            company_inst = request_data['company_inst']
        else:
            return jsonify({"error": "Forgot something like lo...",}), 403
        cur = db.cursor()
        cur.execute(''' UPDATE company SET name = %s,
                    description = %s,
                    mobile = %s,
                    instagram = %s WHERE id = %s ''',
                    (company_name,company_desc,company_mob,company_inst,company_id))
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
@app.route("/api/edit/user", methods = ['POST', 'GET'])
def editUser():
    if request.method == 'GET':
        return "This method is not allowed"
    if request.method == 'POST':
        request_data = request.get_json()

        if "id" in request_data:
            user_id = request_data['id']
        else:
            return jsonify({"error": "Forgot something like id...",}), 403

        if "name" in request_data:
            user_name = request_data['name']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

        if "surname" in request_data:
            user_surname = request_data['surname']
        else:
            return jsonify({"error": "Forgot something like na...",}), 403

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
        cur.execute(''' UPDATE company SET name = %s,
                    surname = %s,
                    uid = %s,
                    avatar = %s,
                    type = %s WHERE id = %s ''',
                    (user_name,user_surname,user_uid,user_avatar,user_type,user_id))
        db.commit()
        cur.close()
        return  jsonify(success)






app.run(host='0.0.0.0', port=5000)

