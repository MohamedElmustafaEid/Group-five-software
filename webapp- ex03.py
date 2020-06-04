from flask import Flask, render_template, request, redirect, url_for, session, flash, g

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from psycopg2 import connect


app = Flask(__name__,template_folder='')
#app.secret_key = '!@3QWeASdZXc'


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
@app.route("/")
@app.route("/")
def home():
    
    mysession()
    return render_template("index.html")    

@app.route('/')
@app.route('/')
def About():
    return render_template('about.html')   

@app.route('/', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def Register():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        age      = request.form['age']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else :
            conn = conn_db()
            cur = conn.cursor()
            cur.execute('SELECT userid FROM sys_table WHERE username = %s', (username,))
            if cur.fetchone() is not None:
                error = 'Username already used! try another one'
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
    
     return render_template('Register.html')

@app.route('/', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
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
            error = 'Login failed! Wrong username'
        elif not check_password_hash(sys[2], password):
            error = 'Login failed! Wrong password'
            
        if error is None:
            session.clear()
            session['userid'] = sys[0]
            return redirect(url_for('home'))
        
        flash(error)
        
    return render_template('Login.html')

@app.route('/')
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
    
@app.route('/Search', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def Search():
    if request.method == "POST":
        dataset = request.form['dataset']
        Database = open('Database.txt')
        connStr = Database.readline()
        conn = connect(connStr)
                
        cur = conn.cursor()      
        cur.execute(
            """SELECT interview_date, gender, marital_status, religion, patient_education_level, ethinc_group FROM data_table WHERE 
            interview_date LIKE %s OR gender LIKE %s OR marital_status LIKE %s OR religion LIKE %s OR patient_education_level LIKE %s OR ethinc_group LIKE %s""",
                         (dataset,dataset))
                          
        conn.commit()
        data = cur.fetchall()
        
        if len(data) == 0 and dataset == 'all': 
            cur.execute("SELECT interview_date, gender, marital_status, religion, patient_education_level, ethinc_group from data_table")
            conn.commit()
            data = cur.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')


if (__name__)=='__main__':
    app.run(debug=True,use_reloader=False)
