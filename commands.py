import json
from bottle import get, post, put, delete, request, abort
import funcs

customers_json_file = 'customers.json'
users_json_file = 'users.json'

@get('/products')
def getProducts():
    return funcs.get_products()

@post('/login')
def login():
    json_file = users_json_file
    username = request.params.get('username')
    pwd = request.params.get('pwd')
    all_users = json.loads(get_all_items(json_file))
    for aUser in all_users:
        if aUser.get('username') == username and aUser.get('pwd') == pwd:
            return {'auth': 'User Authenticated'}
    abort(403, 'Please login')

@get('/users')
def getUsers():
    json_file = users_json_file
    return get_all_items(json_file)

@put('/user')
@post('/user')
def addUser():
    json_file = users_json_file
    add_item(json_file,request)

@post('/user/:username')
def updateUser(username):
    json_file = users_json_file
    aKey = 'username'
    aValue = username
    update_item(json_file,aKey,aValue)

@delete('/user/:username')
def deleteUser(username):
    json_file = users_json_file
    aKey = 'username'
    aValue = username
    delete_item(json_file,aKey,aValue)

@get('/customers')
def getCustomers():
    json_file = customers_json_file
    return get_all_items(json_file)

@put('/customer')
@post('/customer')
def addCustomer():
    json_file = customers_json_file
    add_item(json_file,request)

@post('/customer/:id')
def updateCustomer(id):
    json_file = users_json_file
    aKey = 'id'
    aValue = id
    update_item(json_file,aKey,aValue)

@delete('/customer/:id')
def deleteCustomer(id):
    json_file = users_json_file
    aKey = 'id'
    aValue = id
    delete_item(json_file,aKey,aValue)


def get_all_items(json_file):
    json.load(open(json_file))
    return open(json_file).read()

def add_item(json_file, request):
    json_input = get_input_json(request)
    aList = get_list(json_file)
    aList.append(json_input)
    save_list(aList,json_file)
    return "Success"

def update_item(json_file,aKey,aValue):
    json_input = get_input_json(request)
    aList = get_list(json_file)
    remove_from_list(aList,aKey,aValue)
    aList.append(json_input)
    save_list(aList,json_file)

def delete_item(json_file,aKey,aValue):
    aList = get_list(json_file)
    remove_from_list(aList, aKey, aValue)
    save_list(aList,json_file)


def get_input_json(http_request):
    req = http_request.body.readline()
    if not req:
        abort(400, 'No data received')
    return json.loads(req)

def get_list(list_file):
    aList = json.load(open(list_file))
    return aList

def save_list(aList,json_file):
    open(json_file,'w').write(json.dumps(aList))

def remove_from_list(aList,aKey,aValue):
    for i in range(0,len(aList)):
        aDict = aList[i]
        if aDict.get(aKey) == aValue:
            aList.remove(aDict)
