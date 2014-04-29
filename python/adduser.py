from passlib.apps import custom_app_context as pwd_context
import psycopg2
import ConfigParser
import datetime
import logging

"""
simple app to get a user name, password, db user name, db password and role
and insert it into users table
password and db password are encrypted
"""

def getinput():
    """
    get input from stdin
    return in dict
    """
    vals = {}
    vals['uname'] = raw_input('Enter user name: ')
    vals['upwd'] = raw_input('Enter password: ')
    vals['dbname'] = raw_input('Enter database user name: ')
    vals['dbpwd'] = raw_input('Enter database password: ')
    while True:
        role = raw_input('Enter role (ADMIN, TRADER or WATCHER): ')
        if role in ('ADMIN', 'TRADER', 'WATCHER'):
            vals['role'] = role
            break
        else:
            print "Role entered not one of ADMIN, TRADER or WATCHER"
    return vals

def createuser(uname, upwd, dbname, dbpwd, role):
    """
    encrypt passwords and insert into db
    """
    supwd = pwd_context.encrypt(upwd)
    sdbpwd = pwd_context.encrypt(dbpwd)
    db = psycopg2.connect(database='EM', user='rjn', password='zaxxon')
    with db:
        with db.cursor() as cur:
            cur.execute("INSERT em_users(username, passwd, role, dbusername, dbpasswd) VALUES(%s, %s, %s, %s, %s)", (uname, upwd, role, dbname, dbpwd))
            
    
    pass

if __name__ == "__main__":
    
    vals = getinput()
    createuser(vals['uname'], vals['upwd'], vals['dbname'], vals['dbpwd'], vals['role'])
    