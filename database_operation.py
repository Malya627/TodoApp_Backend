import uuid,string,random
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

client = MongoClient("mongodb+srv://react:react@malya.gso2y.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.TodoList

def Create_User(data):
    hashed_pasword = generate_password_hash(data['password'] , method='sha256')
    user = {
        'name' : data['name'],
        'gender' : data['gender'],
        'user_id' : get_random_string(len(data['name'])),
        'username' : data['username'],
        'password' : hashed_pasword,
    }
    collection = db.users
    insert_id = collection.insert_one(user).inserted_id
    if insert_id:
        return True
    else:
        return False

def Get_All_User():
    collection = db.users
    res = collection.find({},{'_id':0})
    return [r for r in res]

def Get_One_User(user_id):
    collection = db.users
    res = collection.find({'user_id' : user_id},{'_id':0})
    return [r for r in res]

def Delete_User(user_id):
    collection = db.users
    res = collection.delete_one({'user_id' : user_id})
    print(res)
    return True

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def login(username, password):
    collection = db.users
    res = collection.find({'username' : username})
    user = [r for r in res]
    if len(user) == 0:
        return False
    else:
        user_data = user[0]
        if check_password_hash(user_data['password'],password):
            return True,user_data
        else:
            return False,user_data