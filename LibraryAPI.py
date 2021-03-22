import mariadb
import json
from flask import Flask, request
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

# Connect to the MariaDB
try:
    conn = mariadb.connect(user='root',
                           password='123456',
                           host='127.0.0.1',
                           port=3306,
                           database='Library')
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")


'''
Request: UserID, Password
Output:
{'code': 0, 'content': 'User'}   Succeed for User(Client) account
{'code': 1, 'content': 'Invalid userID or password.'} Fail
{'code': 0, 'content': 'Staff'}  Succeed for Staff account
'''
@app.route('/login', methods=['POST'])
def login():
    userID = request.form['UserID']
    password = request.form['Password']
    sql = "select * from Login where UserID=? and Password=?"
    cur.execute(sql, (userID, password,))
    result = []
    for data in cur:
        result.append(data)
    if result:
        return json.dumps({'code': 0,
                           'content': result[0][2]})
    else:
        return json.dumps({'code': 1,
                           'content': 'Invalid userID or password.'})


'''
Example output if it fails:
{'code': 1, 'content': ["Duplicate entry 'user10' for key 'PRIMARY'"]}
'''
@app.route('/newUser', methods=['POST'])
def newUser():
    userID = request.form['UserID']
    password = request.form['Password']
    role = request.form['Role']
    sql = "insert into login values(?,?,?)"
    sql2 = "insert into user(userID) values(?)"
    try:
        cur.execute(sql,(userID,password,role))
        conn.commit()
        cur.execute(sql2, (userID,))
        conn.commit()
        return json.dumps({'code': 0,
                           'content': "succeed"})
    except mariadb.Error as err:
        return json.dumps({'code': 1,
                           'content': err.args})


'''
Output: 
[{'ISBN': 'isbn1', 
 'Title': 'book1', 
 'Copies': 3, 
 'PublicationDate': None, 
 'Author': 'author1', 
 'image': None, 
 'REMOVE': 'False'}, 
 {'ISBN': 'isbn2', 
 'Title': 'book2', 
 'Copies': 3, 
 'PublicationDate': None, 
 'Author': 'author2', 
 'image': None, 
 'REMOVE': 'False'}
 ]
'''
@app.route('/book', methods=['POST'])
def book():
    sql = "select * from Books where remove=?"
    cur.execute(sql, ('False',))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data)


@app.route('/addBook', methods=['POST'])
def addBook():
    try:
        isbn = request.form['ISBN']
        title = request.form['Title']
        copies = request.form['Copies']
        date = request.form['PublicationDate']
        image = request.form['Image']
        copies = int(copies)
        author = request.form['Author']
        sql = "INSERT INTO Books(ISBN, Title, Copies,PublicationDate,Image, Author) VALUES(?,?,?,?,?,?)"
        cur.execute(sql, (isbn, title, copies, date, image, author))
        conn.commit()
        return json.dumps({'code': 0,
                           'content': "succeed"})
    except mariadb.Error as err:
        return json.dumps({'code': 1,
                           'content': err.args})


@app.route('/removeBook', methods=['POST'])
def remove():
    isbn = request.form['ISBN']
    sql = "Update Books set remove=? where ISBN=?"
    cur.execute(sql, ('True', isbn))
    conn.commit()
    return 0


@app.route('/recoverBook', methods=['POST'])
def recover():
    isbn = request.form['ISBN']
    sql = "Update Books set remove=? where ISBN=?"
    cur.execute(sql, ('False', isbn))
    conn.commit()
    return 0


'''
Example Output:
[{'UserID': 'User1', 'NAME': 'User1', 'BirthDate': None, 'Email': None, 'Phone': None, 'Address': None}]
'''
@app.route('/profile', methods=['POST'])
def profile():
    userID = request.form['UserID']
    sql = "select * from User where UserID=?"
    cur.execute(sql, (userID,))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data)


@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    userID = request.form['UserID']
    name = request.form['Name']
    birthDate = request.form['BirthDate']
    email = request.form['Email']
    phone = request.form['Phone']
    address = request.form['Address']
    sql = "Update User set Name=?, BirthDate=?, Email=?, Phone=?, Address=? where UserID=?"
    cur.execute(sql, (name, birthDate, email, phone, address, userID))
    conn.commit()
    return 0


'''
Type: ISBN, Title, Author
Example output:
[ 
{'ISBN': 'isbn1', 
 'Title': 'book1', 
 'Copies': 3, 
 'PublicationDate': None, 
 'Author': 'author1', 
 'Image': None, 
 'REMOVE': 'False'}, 
 {'ISBN': 'isbn2', 
 'Title': 'book2', 
 'Copies': 3, 
 'PublicationDate': None, 
 'Author': 'author2', 
 'Image': None, 
 'REMOVE': 'False'}
]
'''
@app.route('/search', methods=['POST'])
def search():
    context = request.form['Context']
    searchType = request.form['Type']
    if searchType == 'ISBN':
        sql = "select * from Books where ISBN=? and remove='False'"
        cur.execute(sql, (context,))
    elif searchType == 'Title':
        sql2 = "select * from Books where Title like ? and remove='False' "
        str1 = '%' + context + '%'
        cur.execute(sql2, (str1,))
    else:
        sql3 = "select * from Books where Author like ? and remove='False'"
        str2 = '%' + context + '%'
        cur.execute(sql3, (str2,))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data)


@app.route('/changePassword', methods=['POST'])
def changePassword():
    userID = request.form['UserID']
    password = request.form['Password']
    sql = "update Login set Password=? where UserID=?"
    cur.execute(sql, (password, userID))
    conn.commit()
    return 0


if __name__ == "__main__":
    app.run(debug=True)
