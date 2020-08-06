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
            read_default_group='files' ## This is to hide the password configuration
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



api.add_resource(People, '/people')

## RUN

if __name__ == "__main__":
    print("Starting Web Service")
    app.run(host="127.0.0.1", port=5000)
