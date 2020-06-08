from flask import Flask, render_template, request, redirect, url_for, session, flash, g

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from psycopg2 import connect


app = Flask(__name__,template_folder='')
app.secret_key = '!@3QWeASdZXc'


#This function creates a connection to the database saved in Database.txt

def conn_db():
    if 'db' not in g:
        Database = open('Database.txt')
        dbconfig = Database.readline()
        g.db = connect(dbconfig)
    
    return g.db

def enddb_conn():
    if 'db' in g:
        g.db.close()
        g.pop('db')

@app.route("/")
@app.route("/Home")
@app.route("/home")
def home():
    
    mysession()
    return render_template("index.html")    

@app.route('/About')
@app.route('/about')
def about():
    return render_template('feedback/about2.html')  

@app.route('/CustomizePlot')
@app.route('/customizeplot')
def CustomizePlot():
    return render_template('Visual/CustomizePlot.html')  
    

@app.route('/viewmap')
@app.route('/ViewMap')
def ViewMap():
    return render_template('Visual/ViewMap.html')  


@app.route('/Backend_Developers')
@app.route('/backend_developers')
def Backend_Developers():
    return render_template('Backend Developers.html')  

@app.route('/Frontend_Developers')
@app.route('/frontend_developers')
def Frontend_Developers():
    return render_template('Frontend Developers.html')  

@app.route('/Contact')
@app.route('/contact')
def contact():
    return render_template('feedback/contact.html')  


@app.route('/Register', methods=('GET', 'POST'))
@app.route('/register', methods=('GET', 'POST'))
def Register():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        age      = request.form['age']
        error = None

        if not username:
            error = 'Please fill out this field.'
        elif username.isdigit():
            abort(406)
            
        elif not password:
            error = 'Please fill out this field.'
        elif not email:
            error = 'Please fill out this field.'     
        elif not age:
            error = 'Please fill out this field.'
        else :
            conn = conn_db()
            cur = conn.cursor()
            cur.execute('SELECT userid FROM sys_table WHERE username = %s', (username,))
            if cur.fetchone() is not None:
                error = 'Username already used! try another one please!'
                cur.close()
        


        if error is None:

            conn = conn_db()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO sys_table (username, password, email, age) VALUES (%s, %s,%s, %s)',
                (username, generate_password_hash(password), email, age))
            cur.close()
            conn.commit()
            return redirect(url_for('login'))

        flash(error) 
     return render_template('Auth/Register.html')

@app.route('/Login', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        conn = conn_db()
        cur = conn.cursor()
        error = None
        cur.execute('SELECT * FROM sys_table WHERE username = %s', (username,))
        
        #Named sys because it takes the first row from sys_table in the database
        sys = cur.fetchone()
        cur.close()
        conn.commit()
        
        #sys is defined in the three lines above
        if sys is None:
            error = 'Login failed! Wrong Username!'
        elif not check_password_hash(sys[2], password):
            error = 'Login failed! Wrong Password!'
            
        if error is None:
            session.clear()
            session['userid'] = sys[0]
            return redirect(url_for('home'))
        
        flash(error)
        
    return render_template('Auth/login.html')

@app.route('/Logout')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def mysession():
    userid = session.get('userid')

    if userid is None:
        g.user = None
    else:
        conn = conn_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sys_table WHERE userid = %s', (userid,))
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
    if g.user is not None:
        return True
    else: 
        return False



@app.route('/Comments')
@app.route('/comments')
def Comments():
    myFile = open('Database.txt')
    connStr = myFile.readline()
    conn = connect(connStr)
    cur = conn.cursor()
    cur.execute(
            """SELECT sys_table.username, comment_table.comment_id, comment_table.comment 
               FROM sys_table, comment_table WHERE  
                    sys_table.userid = comment_table.userid """
                    )
    comment_table1 = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    mysession()

    return render_template('feedback/comments.html', comment_table1=comment_table1)


@app.route('/AddComment', methods=('GET', 'POST'))
@app.route('/addcomment', methods=('GET', 'POST'))
@app.route('/Addcomment', methods=('GET', 'POST'))
@app.route('/addComment', methods=('GET', 'POST'))
def AddComment():
    if mysession():
        if request.method == 'POST' :
            comment = request.form['comment']
            error = None
           
            if error is not None :
                flash(error)
                return redirect(url_for('Comments'))
            else : 
                    Database = open('Database.txt')
                    connStr = Database.readline()
                    conn = connect(connStr)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO comment_table (comment, userid) VALUES (%s, %s)', 
                               (comment, g.user[0])
                               )
                    cur.close()
                    conn.commit()
                    conn.close()
                    return redirect(url_for('Comments'))
        else :
            return render_template('feedback/AddComment.html')
    else :
        error = 'Only loggedin users can add comments!'
        flash(error)
        return redirect(url_for('login'))

@app.route('/Search', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def Search():
    if request.method == "POST":
        dataset = request.form['dataset']
        conn = conn_db()
        cur = conn.cursor()
        if not dataset:
            error = " please fill the search"
            flash(error)     
                  
        cur = conn.cursor()      
        cur.execute(
            """SELECT  "Patient_id", "Gender", "Marital_Status", "Religion", "Education_level" FROM data_table WHERE 
            "Patient_id" LIKE %s OR "Gender" LIKE %s OR "Marital_Status" LIKE %s OR "Religion" LIKE %s OR "Education_level" LIKE  %s""",(dataset,dataset,dataset,dataset,dataset,))
                          
        conn.commit()
        data = cur.fetchall()
       
        if len(data) == 0 and dataset == 'all': 
            cur.execute("""SELECT  "Gender", "Marital_Status", "Religion", "Education_level" FROM  data_table """)
            conn.commit()
            data = cur.fetchall()
        return render_template('search.html', data=data,)
    return render_template('search.html')                         


if (__name__)=='__main__':
    app.run(debug=True,use_reloader=False)