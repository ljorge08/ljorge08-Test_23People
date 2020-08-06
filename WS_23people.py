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
            read_default_file='conf/mysql.conf' ## This is to hide the password configuration
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


api.add_resource(People, '/people')

## RUN

if __name__ == "__main__":
    print("Starting Web Service")
    app.run(host="127.0.0.1", port=5000, debug=True)
