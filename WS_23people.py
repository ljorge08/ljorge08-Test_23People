from flask import jsonify
from flask import flash
from flask import Flask
from flask_restful import Resource, Api
from flask import request
import pymysql as mysql


# Json confuguration
app = Flask(__name__)
api = Api(app)


# Function used to connect to BD

def db_connect():
    try:
        conn = mysql.connect(
            read_default_file='conf/mysql.conf',  ## This is to hide the password configuration
            autocommit = True
        )
        print("Conectado a la base de datos")
        return conn
    except:
        print("Can't connect to data base")
    finally:
        conn.close


## Creating the People class with the GET y  POST methods

class People(Resource):
    def get(self):
        try:
            conn = db_connect()
            cur = conn.cursor(mysql.cursors.DictCursor)
            cur.execute("select id, nationalId, name, lastName, age, originPlanet, PictureURL from users;")
            rows = cur.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        except:
            print("Can't response get the request")

    # Creating the post method
    def post(self):
            header = str(request.headers).upper()
            c_type = header.find("CONTENT-TYPE: APPLICATION/JSON")
            if 0 <= c_type:
                try:
                    conn = db_connect()
                    national_id = request.json['nationalId']
                    firts_name = request.json['name']
                    last_name = request.json['lastName']
                    user_age = request.json['age']
                    origin_planet = request.json['originPlanet']
                    picture_url = request.json['PictureURL']

                    cur = conn.cursor(mysql.cursors.DictCursor)
                    query = "insert into users (nationalId, name, lastName, age, originPlanet, PictureURL)" \
                            " values ('{0}','{1}','{2}',{3},'{4}','{5}'" \
                            ");".format(national_id, firts_name, last_name, user_age, origin_planet, picture_url)
                    print(query)
                    cur.execute(query)
                    message = {'status': 201, 'message': "Person created..." + request.url}
                    resp = jsonify(message)
                    return resp
                except:
                    print("Can't response the post the request")
                    message = {'status': 500,
                               'message': "Can't response the post the request, please check your request..." + request.url}
                    resp = jsonify(message)
                    return resp

            else:
                print("The Post must have a header CONTENT-TYPE: APPLICATION/JSON")
                message = {'status': 400,
                           'message': "The Post must have a header Content-Type: application/json..." + request.url}
                resp = jsonify(message)
                return resp


## Creating the People/National_id class with the GET, PUT and DELETE methods
class peopleId(Resource):
    def get(self, national_id):
        try:
            conn = db_connect()
            cur = conn.cursor(mysql.cursors.DictCursor)
            query = "select id, nationalId, name, lastName, age, originPlanet, PictureURL from users" \
                        " where nationalId='{0}';".format(national_id)
            cur.execute(query)
            rows = cur.fetchall()
            num_fields = len(rows)
            # If the user is in the data base
            if num_fields > 0:
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            else:
                print("The user is not in the Database")
                message = {'status': 404,
                           'message': "The user is not in the Database..." + request.url}
                resp = jsonify(message)
                return resp

        except:
            print("Can't response get_id the request ")

    # Creating the put method
    def put(self, national_id):
        try:
            header = str(request.headers).upper()
            c_type = header.find("CONTENT-TYPE: APPLICATION/JSON")
            if 0 <= c_type:
                conn = db_connect()
                cur = conn.cursor(mysql.cursors.DictCursor)
                # Checking if the user is in the DB
                query = "select id, nationalId, name, lastName, age, originPlanet, PictureURL from users" \
                        " where nationalId='{0}';".format(national_id)
                cur.execute(query)
                rows = cur.fetchall()
                num_fields = len(rows)
                # If the user is the DB
                if num_fields > 0:
                    firts_name = request.json['name']
                    last_name = request.json['lastName']
                    user_age = request.json['age']
                    origin_planet = request.json['originPlanet']
                    picture_url = request.json['PictureURL']
                    query = "update users set name='{1}', lastName='{2}', age={3}, originPlanet='{4}', PictureURL='{5}'" \
                            " where nationalId='{0}';" \
                        .format(national_id, firts_name, last_name, user_age, origin_planet, picture_url)
                    print("Printing update query")
                    print(query)
                    cur.execute(query)
                    message = {'status': 200, 'message': "Put executed..." + request.url}
                    resp = jsonify(message)
                    return resp
                else:
                    print("The user is not in the Database")
                    message = {'status': 404,
                               'message': "The user is not in the Database..." + request.url}
                    resp = jsonify(message)
                    return resp

            else:
                print("The Post must have a header CONTENT-TYPE: APPLICATION/JSON")
                message = {'status': 400,
                    'message': "The Put must have a header Content-Type: application/json..." + request.url}
                resp = jsonify(message)
                return resp

        except:
            print("Can't response the put the request")
            message = {'status': 500,
                       'message': "Can't response the put the request, please check your request..." + request.url}
            resp = jsonify(message)
            return resp

    # Creating de delete method
    def delete(self, national_id):
        try:
            conn = db_connect()
            cur = conn.cursor(mysql.cursors.DictCursor)
            # Checking if the user is in the DB
            query = "select id, nationalId, name, lastName, age, originPlanet, PictureURL from users" \
                    " where nationalId='{0}';".format(national_id)
            cur.execute(query)
            rows = cur.fetchall()
            num_fields = len(rows)
            # If the user is the DB
            if num_fields > 0:
                query = "delete from users" \
                        " where nationalId='{0}';".format(national_id)
                print("Printing update query")
                print(query)
                cur.execute(query)
                message = {'status': 200, 'message': "Delete executed..." + request.url}
                resp = jsonify(message)
                return resp
            else:
                print("The user is not in the Database")
                message = {'status': 404,
                            'message': "The user is not in the Database..." + request.url}
                resp = jsonify(message)
                return resp


        except:
            print("Can't response the put the request")
            message = {'status': 500,
                       'message': "Can't response the put the request, please check your request..." + request.url}
            resp = jsonify(message)
            return resp


api.add_resource(People, '/people')
api.add_resource(peopleId, '/people/<national_id>')

## RUN

if __name__ == "__main__":
    print("Starting Web Service")
    app.run(host="10.128.0.3", port=5000) #Local IP
