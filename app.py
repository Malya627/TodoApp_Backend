from flask import Flask, request, jsonify, make_response
import database_operation as db
import jwt, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "fuckthefuckbeforethefuckfucksyou"

@app.route('/user', methods = ['GET'])
def GetAllUsers():
    user = db.Get_All_User()
    if(len(user) > 0):
        return jsonify({"res" : user})
    else:
        print(len(user))
        return jsonify({"error" : "No Users Found"})

@app.route('/user/<userID>', methods = ['GET'])
def GetOneUsers(userID):
    user = db.Get_One_User(userID)
    if(len(user) > 0):
        return jsonify({"res" : user})
    else:
        return jsonify({"error" : "No User Found"})
    

@app.route('/user', methods = ['POST'])
def CreateUser():
    data = request.get_json()
    create_user = db.Create_User(data)
    if create_user:
        return jsonify({"success" : "User Inserted Successfully"})
    return jsonify({"error" : "Unable to Insert User"})

@app.route('/user/<userID>', methods = ['DELETE'])
def DeleteUser(userID):
    create_user = db.Delete_User(userID)
    if create_user:
        return jsonify({"success" : "User Deleted Successfully"})
    return jsonify({"error" : "Unable to Delete User"})

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not Verify', 401, {'WWW-Authenticate' : 'Basic realm= "Login Required!"'})
    log, user = db.login(auth.username, auth.password)
    if log:
        token = jwt.encode({'user_id' : user['user_id'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'])
        return jsonify({"success" : token.decode('UTF-8')})
    else:
        return make_response('Could not Verify', 401, {'WWW-Authenticate' : 'Basic realm= "Login Required!"'})


if __name__ == '__main__':
    app.run(debug=True)