import sqlite3
from dotenv import dotenv_values
from werkzeug.security import check_password_hash
import datetime

now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
env = dotenv_values(".env")


# def register_account(form):
#     conn = sqlite3.connect(database="bug_tracker.db")
#     cur = conn.cursor()
#     sql = ''' INSERT INTO user (first_name, last_name, password, email)
#              VALUES(?,?,?,?); '''
#     cur.execute(sql, (form['fname'], form['lname'],
#                       generate_password_hash(form["pass"], method="pbkdf2:sha256", salt_length=8), form['email']))
#     conn.commit()
#     user = asd.query.filter_by(email=form["email"]).first()
#     login_user(user)
#     conn.close()


def login_demo_admin():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT email, password 
              FROM user 
              WHERE email = 'test@test.com'; '''
    cur.execute(sql)
    data = cur.fetchone()
    password = data[1]
    return check_password_hash(password, "1234")


def login_demo_project_manager():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT email, password 
              FROM user 
              WHERE email = 'admin@email.com'; '''
    cur.execute(sql)
    data = cur.fetchone()
    password = data[1]
    return check_password_hash(password, "asdf123")


def login_demo_developer():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT email, password 
              FROM user 
              WHERE email = 'admin@email.comm'; '''
    cur.execute(sql)
    data = cur.fetchone()
    password = data[1]
    return check_password_hash(password, "123456")


def check_password(user):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT email, password 
              FROM user 
              WHERE email = '{user['email']}'; '''
    cur.execute(sql)
    data = cur.fetchone()
    password = data[1]
    return check_password_hash(password, user["pass"])


def check_email_exist(email):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT email 
              FROM user 
              WHERE email = '{email}'; '''
    cur.execute(sql)
    data = cur.fetchone()
    if data is None:
        return False
    return True


def register_google_account(user):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' INSERT INTO user (first_name, last_name, password, email) 
              VALUES(?,?,?,?); '''
    cur.execute(sql, (user['given_name'],
                user['family_name'], "None", user['email']))
    conn.commit()
    conn.close()


def check_account(email):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT * FROM user 
               WHERE email = '{email}'; '''
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()
    if data is None:
        return False
    return True


def get_account(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT * FROM user 
               WHERE user_id = '{id}'; '''
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()
    return data


def get_account_by_fullname(first_name, last_name):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT * FROM user 
               WHERE first_name = '{first_name}' AND last_name = '{last_name}'; '''
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()
    return data


def get_users():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' SELECT id, first_name, last_name, email, role 
               FROM user; '''
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data


def update_user(form):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' UPDATE user 
              SET first_name = ?, last_name = ?, email = ?, role = ?
              WHERE id = '{form["id"]}'; '''
    cur.execute(sql, (form["first_name"],
                form["last_name"], form["email"], form["role"]))
    conn.commit()
    conn.close()


def get_projects():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' SELECT * from project; '''
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data


def get_project_by_id(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT * from project 
               WHERE id = {id}; '''
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()
    return data


def get_tickets_by_project_id(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT * FROM ticket 
               WHERE project_id = '{id}'; '''
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data


def get_ticket_by_id(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT * 
               FROM ticket 
               WHERE id = '{id}'; '''
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()
    return data


def get_project_devs(project_id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT DISTINCT user.id, user.first_name, user.last_name, user.role, user.email 
               FROM project_dev 
               LEFT JOIN user 
               ON user.id = project_dev.user_id 
               WHERE project_id = {project_id}; '''
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data


def get_user_projects(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT DISTINCT *
               FROM project_dev 
               LEFT JOIN project
               ON project.id = project_dev.project_id
               WHERE user_id = '{id}'; '''
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data


def get_comments(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT * 
               FROM comment 
               WHERE ticket_id = '{id}'; '''
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data


def delete_project(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' DELETE FROM project 
               WHERE id = {id}; '''
    cur.execute(sql)
    conn.commit()
    conn.close()


def del_dev_from_project(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' DELETE FROM project_dev 
               WHERE user_id = {id}; '''
    cur.execute(sql)
    conn.commit()
    conn.close()


def del_duplicate_devs():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' SELECT id, user_id, project_id, count(*)
               FROM project_dev
               GROUP by user_id, project_id
               HAVING COUNT(*)>1; '''
    cur.execute(sql)
    data = cur.fetchall()
    for id, user_id, project_id, count in data:
        while count > 1:
            sql = f''' DELETE from project_dev
                       WHERE id = {id} '''
            cur.execute(sql)
            conn.commit()
            count -= 1
    conn.close()


def add_project(form, user):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' INSERT INTO project(name, description,author)
              VALUES(?,?,?); '''
    cur.execute(sql, (form['project-name'], form['project-description'],
                      f"{user.first_name} {user.last_name}"))
    conn.commit()
    conn.close()


def add_project_dev(user_id, project_id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' INSERT INTO project_dev(user_id, project_id)
              VALUES(?,?); '''
    cur.execute(sql, (user_id, project_id))
    conn.commit()
    conn.close()


def add_ticket(form, user):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    developer = form['developer'].split()
    sql = ''' INSERT INTO ticket(title, description, developer, created, author, ticket_priority, ticket_status, ticket_type, project_id, user_id)
              VALUES(?,?,?,?,?,?,?,?,?,?); '''
    cur.execute(sql, (form["title"], form["description"], f"{developer[1]} {developer[2]}", datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                      f"{user.first_name} {user.last_name}", form["priority"],
                      form["status"], form["type"], form["project_id"], developer[0]))
    conn.commit()
    conn.close()


def update_ticket(form):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    developer = form['developer'].split()
    sql = f'''UPDATE ticket 
              SET title = ? , description = ? , developer = ? , ticket_priority = ? , ticket_status = ? ,
              ticket_type = ? , updated = ? , user_id = ? WHERE id = '{form['ticket_id']}'; '''
    cur.execute(sql, (form['title'], form['description'], f"{developer[1]} {developer[2]}", form['priority'],
                      form['status'], form['type'], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), developer[0]))
    conn.commit()
    conn.close()


def update_project(form):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' UPDATE project 
              SET name = ?, description = ?
              WHERE id = '{form["id"]}'; '''
    cur.execute(sql, (form["name"], form["description"]))
    conn.commit()
    conn.close()


def delete_comment(ticket_id, id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' DELETE 
               FROM comment 
               WHERE id = {id} and ticket_id = {ticket_id}; '''
    cur.execute(sql)
    conn.commit()
    conn.close()


def del_ticket_by_id(id):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = f''' DELETE 
               FROM ticket 
               WHERE id = {id}; '''
    cur.execute(sql)
    conn.commit()
    conn.close()


def add_comment(form, user):
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' INSERT INTO comment(author, message, created, ticket_id, user_id)
              VALUES(?,?,?,?,?); '''
    cur.execute(sql, (f"{user.first_name} {user.last_name}",
                form["message"], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), form["ticket_id"], user.id))
    conn.commit()
    conn.close()


def create_table_user():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' CREATE TABLE IF NOT EXISTS user(
               id integer PRIMARY KEY,
               email VARCHAR(250) UNIQUE,
               password VARCHAR(250) NOT NULL,
               first_name VARCHAR(50) NOT NULL,
               last_name VARCHAR(50) NOT NULL,
               role VARCHAR(50)
               ); '''
    cur.execute(sql)
    conn.commit()
    conn.close()


def create_table_projects():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' CREATE TABLE IF NOT EXISTS project(
                id integer PRIMARY KEY,
                name VARCHAR(100),
                description VARCHAR(250),
                author VARCHAR(100)
                ); '''
    cur.execute(sql)
    conn.commit()
    conn.close()


def create_table_project_dev():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' CREATE TABLE IF NOT EXISTS project_dev(
                id integer PRIMARY KEY,
                user_id integer NOT NULL,
                project_id integer NOT NULL,
                CONSTRAINT FK_project FOREIGN KEY (project_id) REFERENCES project (id),
                CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES user (id)
                ); '''

    cur.execute(sql)
    conn.commit()
    conn.close()


def create_table_ticket():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' CREATE TABLE IF NOT EXISTS ticket(
                id integer PRIMARY KEY,
                title VARCHAR(100),
                description VARCHAR(250),
                developer VARCHAR(100),
                status VARCHAR(50),
                created VARCHAR(100),
                author VARCHAR(100),
                ticket_priority VARCHAR(50),
                ticket_status VARCHAR(50),
                ticket_type VARCHAR(50),
                updated VARCHAR(100)
                user_id integer NOT NULL,
                project_id NOT NULL,
                CONSTRAINT FK_project FOREIGN KEY (project_id) REFERENCES project (id)
                CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES user (id)
                ); '''
    cur.execute(sql)
    conn.commit()
    conn.close()


def create_table_ticket_comment():
    conn = sqlite3.connect(database="bug_tracker.db")
    cur = conn.cursor()
    sql = ''' CREATE TABLE IF NOT EXISTS comment(
                id integer PRIMARY KEY,
                author VARCHAR(100),
                message VARCHAR(1000),
                created VARCHAR(100),
                ticket_id integer NOT NULL,
                user_id integer NOT NULL,
                CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES user (id)
                CONSTRAINT fk_ticket FOREIGN KEY (ticket_id) REFERENCES ticket (id)
                ); '''
    cur.execute(sql)
    conn.commit()
    conn.close()
