# Library Control
This is a project for class CSC 33600, the topic of our team is Online Library.

### Database:

We use MariaDB as our database support.

You need to download the MariaDB and then run the file "Library.sql" to create the database and insert the data.

### Backend:

Backend we use python language, and having Flask framework run on python's virtual environment.

All the python code is on the `LibraryApi.py` file.

Before running this file, your machine should have the `mariadb`, `json`, `flask`, and `flask_cors` packages installed.

Before running the code, you need to modify the 'user', 'password', 'host', 'port' in 'mariadb.connect' to connect to your database.

To run the backend, just simply locate to the directory which `LibraryApi.py` is at in the terminal, and use `python LibraryApi.py` to have the server running.

### Frontend:

We use html, Javascript, CSS to write the frontend.

All the html files and the folder 'Books' should be saved in the same directory.

While the backend is running, you can run the 'Login.html' and then enter the UserID and Password to log into the system.
