from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, session


from dotenv import load_dotenv
import datetime
import os
import sqlite3
from sqlite3 import Row
from functools import wraps
from datetime import datetime
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)  
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

#query om alle agendas op te halen
def get_all_agendas():
    conn = get_db_connection()
    agendas = conn.execute('SELECT * FROM agendas').fetchall()
    conn.close()
    return agendas

#authenticatie
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if   session.get("loggedIn", False):
            return render_template("login.html")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'is_admin' in session and session['is_admin']:
            return func(*args, **kwargs)
        else:
            flash('You are not authorized to access this page.', 'error' )
            return redirect(url_for('login'))
    return decorated_function

def is_admin():
    return 'is_admin' in session and session['is_admin']

def checklogin(username, password):
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            user = c.fetchone()

        if user and bcrypt.check_password_hash(user['password'], password):
            return user
        else:
            return None
    except Exception as e:
        print(f"Error during login query: {e}")
        return None

     
     

def logoutsession():
    session.pop('teacher_id', None)
    session['loggedIn'] = False
    return render_template('login.html')
#query om database op te halen
def get_db_connection():
    conn = sqlite3.connect("event_calendar.db")
    conn.row_factory = sqlite3.Row
    return conn

#route om agenda en evenementen te bekijken
@app.route('/agenda/<agenda_name>')

def show_agenda(agenda_name):
    conn = get_db_connection()


    agenda = conn.execute('SELECT * FROM agendas WHERE url_name = ?', (agenda_name,)).fetchone()

    if not agenda:
        conn.close()
        abort(404, description="Agenda niet gevonden")


    events = conn.execute('SELECT * FROM events WHERE agenda_id = ?', (agenda['id'],)).fetchall()

    conn.close()

    return render_template('agenda.html', agenda=agenda, events=events)


#error als route niet bestaat
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#route om alle agendas te zien
@app.route('/alle_agendas',  methods=['GET', 'POST'])
@login_required




def alle_agendas():
    
    
    
    conn = get_db_connection()

   
    page = request.args.get('page', 1, type=int)
    per_page = 20  

    
    offset = (page - 1) * per_page

  
    query = f'SELECT * FROM agendas LIMIT {per_page} OFFSET {offset}'

    
    alle_agendas = conn.execute(query).fetchall()

    conn.close()

    return render_template('alle_agendas.html', alle_agendas=alle_agendas)

#default route waar je in kan loggen
@app.route('/', methods=['GET', 'POST'])

def login():
    
    
    if request.method == 'POST':
        
        username = request.form['name']
        password = request.form['password']
        user = checklogin(username, password)

        if user:
            session["username"]=user["username"]
            session["password"]=user["password"]
            session['is_admin'] = 1 if bool(user['is_admin']) else 0
            


            print(f"Username: {session['username']}")
            print(f"Is admin: {session['is_admin']}")
            
            if session['is_admin']:
                flash('Admin login successful')
                return redirect(url_for('alle_agendas'))
            else:
                flash('Login successful')
                return redirect(url_for('users'))

            
        else:
            flash('Invalid username or password. Please try again.')

    return render_template('login.html')


#authenticatie
def check_credentials(username, password, is_admin=(1)):
    print(f"Checking credentials for {username} with is_admin={is_admin}")
    db = get_db_connection()
    cursor = db.execute('SELECT * FROM teachers WHERE username=? AND teacher_password=? AND is_admin=1', (username, password, is_admin))
    user_data = cursor.fetchone()
    db.close()

    if user_data:
        column_names = [description[0] for description in cursor.description]
        user = dict(zip(column_names, user_data))
        return user
    else:
        return None
#route om uit te loggen
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))



#route om alle gebruikers te zien
@app.route('/users',methods=["GET","POST"])
def users():
    def get_all_users():
        conn = sqlite3.connect("C:/Users/Zairo/Documents/GitHub/inhaal-wp2-mvc-Ryzairo-1/lib/database/event_calendar.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        users = cursor.execute('SELECT * FROM users').fetchall()
        conn.close()
        return users

    users_data = get_all_users()

    return render_template("users.html", users=users_data)
#route om gebruiker aan te maken
@app.route('/createuser', methods=["GET", "POST"])
def create_user():
    msg = ""
    
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            is_admin = 1 if 'is_admin' in request.form else 0
            display_name = request.form['display_name']
            date_created = datetime.datetime.now()
              

            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO users (username, password, is_admin, display_name) VALUES (?, ?, ?, ?)',
                          (username, password, is_admin, display_name))
                conn.commit()
                msg = ""

        except Exception as e:
            conn.rollback()
            msg = f"Niet toegevoegd vanwege een fout: {str(e)}"

        finally:
            flash(msg, 'success')
            return redirect("users")
    return render_template("create_user.html")

#rotue om gebruiker te verwijderen
@app.route('/deleteuser/<int:user_id>', methods=["GET", "POST"])
def delete_user(user_id):
    if request.method == 'POST':
        try:
            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                msg = ""

        except Exception as e:
            conn.rollback()
            msg = f"Niet verwijderd vanwege een fout: {str(e)}"

        finally:
            flash(msg, 'success')
            return redirect(url_for("users"))

       

#route om agenda te maken
@app.route('/create_agenda', methods=['GET', 'POST'])
def create_agenda():
    msg = ""
    
    if request.method == 'POST':
        try:
            title = request.form['agenda_title']
            url_name = request.form['agenda_url']
            external_stylesheet = request.form['external_stylesheet']
            date_created = datetime.now()

            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO agendas (title, url_name, external_stylesheet, date_created) VALUES (?, ?, ?, ?)',
                          (title, url_name, external_stylesheet, date_created))
                conn.commit()
                msg = ""

        except Exception as e:
            conn.rollback()
            msg = f"Niet toegevoegd vanwege een fout: {str(e)}"

        finally:
            flash(msg, 'success')
            return redirect("alle_agendas")
    return render_template("create_agenda.html")

#route om alle evenementen te bekijken
@app.route('/events', methods=['GET', 'POST'])
def events():
    conn = get_db_connection()

    page = request.args.get('page', 1, type=int)
    per_page = 20  
    offset = (page - 1) * per_page

    if request.method == 'GET':
        date_filter = request.args.get('date')
        location_filter = request.args.get('location')
        aanmelder_filter = request.args.get('aanmelder')

        query = 'SELECT * FROM events'
        params = ()

        if date_filter or location_filter or aanmelder_filter:
            query += ' WHERE'
            if date_filter:
                query += ' event_date = ? AND'
                params += (date_filter,)
            if location_filter:
                query += ' location LIKE ? AND'
                params += (f'%{location_filter}%',)
            if aanmelder_filter:
                query += ' aanmelder LIKE ? AND'
                params += (f'%{aanmelder_filter}%',)

            
            query = query[:-4]

        query += f' LIMIT {per_page} OFFSET {offset}'
        
        events = conn.execute(query, params).fetchall()
        conn.close()
        
        return render_template('events.html', events=events)

    elif request.method == 'POST':
      
        pass

    conn.close()
    return render_template('events.html', events=events)

   

#route om lisjt met evenementen te zien en evenementen aan te passsen
@app.route('/events_moderation',  methods=['GET', 'POST'])

def events_moderation():
    conn = get_db_connection()



    events = conn.execute('SELECT * FROM events').fetchall()
    
    
    conn.close()


        

    return render_template('events_moderation.html', events=events)

#route om evenement aan te passen
@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    conn = get_db_connection()

    if request.method == 'GET':
        
        event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
        return render_template('edit_event.html', event=event)

    elif request.method == 'POST':
        
        name = request.form['name']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        location = request.form['location']
        description = request.form['description']

      
        conn.execute('UPDATE events SET name=?, event_date=?, start_time=?, end_time=?, location=?, description=? WHERE id=?',
                     (name, event_date, start_time, end_time, location, description, event_id))
        conn.commit()

        conn.close()
        return redirect(url_for('events_moderation'))

#route om evenement te verwijderen
@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('events_moderation'))


#rotue om event aan te maken
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    agendas = get_all_agendas()
    msg = ""

    if request.method == 'POST':
        try:
            agenda_id = request.form['agenda_id']
            name = request.form['name']
            event_date = request.form['event_date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            location = request.form['location']
            description = request.form['description']
            aanmelder = request.form['aanmelder']
            date_created = datetime.now()

            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO events (agenda_id, name, event_date, start_time, end_time, location, description, date_created, aanmelder) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (agenda_id, name, event_date, start_time, end_time, location, description, date_created, aanmelder))
                conn.commit()
                msg = ""

        except Exception as e:
            conn.rollback()
            msg = f"Event not added due to an error: {str(e)}"

        finally:
            flash(msg, 'success')
            return redirect("events")  

    return render_template("create_event.html", agendas=agendas)


#route voor de admin panel
@app.route('/admin',  methods=['GET', 'POST'])
def admin_panel(): 
    return render_template('admin.html')

@app.route('/test',  methods=['GET', 'POST'])
def test(): 
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)