import mariadb
import json
from flask import Flask, request, render_template
from flask_cors import CORS


app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'

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
    sql2 = "insert into user(userID, Name) values(?, ?)"
    try:
        cur.execute(sql,(userID,password,role))
        conn.commit()
        cur.execute(sql2, (userID, userID))
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


@app.route('/getRemove', methods=['POST'])
def getRemove():
    sql = "select * from Books where remove=?"
    cur.execute(sql, ('True',))
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
    return '0'


@app.route('/recoverBook', methods=['POST'])
def recover():
    isbn = request.form['ISBN']
    sql = "Update Books set remove=? where ISBN=?"
    cur.execute(sql, ('False', isbn))
    conn.commit()
    return '0'


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
    return '0'


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
        sql = "select * from Books where ISBN like ? and remove='False'"
        str1 = '%' + context + '%'
        cur.execute(sql, (str1,))
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
    return '0'


@app.route('/borrow', methods=['POST'])
def borrow():
    try:
        isbn = request.form['ISBN']
        userID = request.form['UserID']
        staffID = request.form['StaffID']
        sql = "Insert BorrowRecord(UserID, ISBN,StaffID) Values(?,?,?)"
        cur.execute(sql, (userID, isbn, staffID))
        conn.commit()
        sql2 = "Update Books set Copies = Copies - 1 where ISBN =?"
        cur.execute(sql2, (isbn,))
        conn.commit()
        return json.dumps({'content': 'Succeed'})
    except mariadb.Error as err:
        return json.dumps({'content': err.args})


@app.route('/return', methods=['POST'])
def returnBook():
    borrowID = request.form['BorrowID']
    borrowID = int(borrowID)
    staffID = request.form['StaffID']
    issue = request.form['Issue']
    sql1 = "insert ReturnRecord(BorrowID, StaffID, Issue) Values(?, ?, ?)"
    cur.execute(sql1, (borrowID, staffID, issue))
    conn.commit()
    sql2 = "Update BorrowRecord set Returned=? where BorrowID =?"
    cur.execute(sql2, ("True", borrowID))
    conn.commit()
    if 'Damaged' not in issue:
        sql3 = "Update Books set Copies = Copies + 1 where ISBN =?"
        sql4 = """select ISBN from ReturnRecord join  BorrowRecord 
                  on BorrowRecord.BorrowID = ReturnRecord.BorrowID 
                  where BorrowRecord.BorrowID =?"""
        cur.execute(sql4, (borrowID,))
        result = []
        for data in cur:
            result.append(data)
        cur.execute(sql3, result[0])
        conn.commit()
    return '0'


"""

Sample output:
[{'Author': 'author1', 
  'BorrowDate': '2021-03-18 14:08:48', 
  'BorrowID': 1, 
  'DueDate': '2021-04-01 14:08:48', 
  'ISBN': 'isbn1', 
  'Title': 'book1', 
  'image': None}, 
 {'Author': 'author9', 
 'BorrowDate': '2021-03-28 16:22:13', 
 'BorrowID': 6, 
 'DueDate': '2021-04-11 16:22:13', 
 'ISBN': 'isbn9', 
 'Title': 'title9', 
 'image': ''}]
"""
@app.route('/borrowRecord', methods=['POST'])
def borrowRecord():
    userID = request.form['UserID']
    sql = """select BorrowID, Books.ISBN, Title, Author, BorrowDate, DueDate, Image from BorrowRecord 
             join Books on BorrowRecord.ISBN=Books.ISBN
             where UserID = ? and Returned=? and Remove=?"""
    cur.execute(sql, (userID, "False", "False"))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)


"""
Sample Output:
[{'Author': 'author9', 
  'BorrowDate': '2021-03-28 14:44:49', 
  'DueDate': '2021-04-11 14:44:49', 
   'ISBN': 'isbn9', 
   'Issue': '', 
   'ReturnDate': '2021-03-28 15:05:36', 
   'Title': 'title9', 
   'image': ''}, 
   {'Author': 'author9', 
   'BorrowDate': '2021-03-28 15:03:52', 
   'DueDate': '2021-04-11 15:03:52', 
   'ISBN': 'isbn9', 
   'Issue': '', 
   'ReturnDate': '2021-03-28 16:08:27', 
   'Title': 'title9', 
   'image': ''}]
"""
@app.route('/returnRecord', methods=['POST'])
def returnRecord():
    userID = request.form['UserID']
    sql = """Select Books.ISBN, Title, Author, BorrowDate, ReturnDate, DueDate, Image, Issue from BorrowRecord
             join ReturnRecord on BorrowRecord.BorrowId = ReturnRecord.BorrowId
             join Books on BorrowRecord.ISBN = Books.ISBN
             where UserID =? and Remove = ?"""
    cur.execute(sql, (userID, "False"))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)


@app.route('/order', methods=['POST'])
def order():
    isbn = request.form['ISBN']
    userID = request.form['UserID']
    sql = "insert OrderRecord(ISBN, UserID) Values(?,?)"
    cur.execute(sql, (isbn, userID))
    conn.commit()
    sql2 = "Update Books set Copies = Copies - 1 where ISBN =?"
    cur.execute(sql2, (isbn,))
    conn.commit()
    return '0'


@app.route('/cancelOrder', methods=['POST'])
def cancel():
    orderID = request.form['OrderID']
    orderID = int(orderID)
    sql = "update OrderRecord set Status=? where OrderID=?"
    cur.execute(sql, ("Canceled", orderID))
    conn.commit()
    sql2 = """update Books set Copies = copies + 1
              where ISBN in 
              (select ISBN from OrderRecord where orderID=?)"""
    cur.execute(sql2, (orderID,))
    conn.commit()
    return '0'


@app.route('/completeOrder', methods=['POST'])
def complete():
    orderID = request.form['OrderID']
    orderID = int(orderID)
    staffID = request.form['StaffID']
    sql1 = "select isbn, UserID from OrderRecord where OrderID =?"
    cur.execute(sql1, (orderID,))
    result = []
    for data in cur:
        result.append(data)
    sql2 = "insert BorrowRecord(ISBN, UserID, StaffID) Values(?,?,?)"
    cur.execute(sql2, (result[0][0], result[0][1], staffID))
    conn.commit()
    sql = "update OrderRecord set Status=? where OrderID=?"
    cur.execute(sql, ("Completed", orderID))
    conn.commit()
    return '0'


@app.route('/orderRecord', methods=['POST'])
def orderRecord():
    userID = request.form['UserID']
    sql = """select Books.ISBN, Title, Author, Image, PublicationDate, Date, OrderID from OrderRecord
             join Books on OrderRecord.ISBN = Books.ISBN 
             where UserID = ? and Remove = ? and Status = ?"""
    cur.execute(sql, (userID, "False", "Waiting"))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)


@app.route('/allOrders', methods=['POST'])
def allOrders():
    sql = """select Books.ISBN, Title, Author, Image, PublicationDate, Date, UserID, OrderID from OrderRecord
             join Books on OrderRecord.ISBN = Books.ISBN 
             where Remove = ? and Status = ?"""
    cur.execute(sql, ("False", "Waiting"))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)


@app.route('/allBorrow', methods=['POST'])
def allBorrow():
    sql = """select BorrowID, Books.ISBN, Title, Author, BorrowDate, DueDate, Image, UserID from BorrowRecord 
             join Books on BorrowRecord.ISBN=Books.ISBN
             where Returned=? and Remove=?"""
    cur.execute(sql, ("False", "False"))
    row_headers = [x[0] for x in cur.description]
    result = cur.fetchall()
    json_data = []
    for data in result:
        json_data.append(dict(zip(row_headers, data)))
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    app.run(debug=True)
