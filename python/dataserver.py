from flask import Flask, flash, render_template, session, jsonify, g, request, url_for, redirect, make_response
from passlib.apps import custom_app_context as pwd_context
import psycopg2
import math
import ConfigParser
import datetime
import logging
import zmq 
import em_client

application = Flask(__name__)
application.secret_key = '\xc4\x14aQ\xdf\x12\x99\xea\x83\x80\xec\xdc3\x80\x8f\xd8\xa6{\x81\x03\x16\x13\x94\x16'

# set up logger
application.logger.setLevel(logging.DEBUG)
logfile = "/var/log/dataserver/dataserver.log"
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)        
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
application.logger.addHandler(fh)
# set up config
application.config.update(dict(logname = "logname",
                               logdir = "logdir",
                               loglevel = logging.ERROR,
                               database = "EM",
                               dbuser = "rjn",
                               dbpwd = "zaxxon"))  

def init_resources(): 
    if not hasattr(g, 'resources_inited'):
        # create db connection
        application.logger.debug("creating new db connection")
        g.db = psycopg2.connect(database='EM', user='rjn', password='zaxxon')
        # set up zmq context
        application.logger.debug("creating new zmq context")
        g.zcontext = zmq.Context()
        application.logger.debug("creating new em_client")
        g.em_client = em_client.EM_Client(cfg=None, context=g.zcontext)
        g.resources_inited = True


@application.teardown_appcontext
def close_resources(error):
    if hasattr(g, 'resources_inited'):
        g.db.close()    
        # will destroy z context
        g.em_client.close()
        delattr(g, 'resources_inited');


@application.route('/')
def get_info():
    application.logger.info("Trading Data Server v0")
    return "Trading Data Server v0"

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            # logged in already
            return redirect('orders.html')
        else:
            html = '''
            <form action="%s" method="post">
                <p><input type=text name=username>
                <p><input type=password name=passwd>
                <p><input type=submit value=Login>
            </form>
            ''' % url_for('login')
            return render_template('login.html')
    elif request.method == 'POST':
        user = request.form['username']
        pwd = request.form['passwd']        
        # lookup user, hash in db
        init_resources()
        with g.db:
            application.logger.debug("logging in %s" % user)
            # get cursor and setup to close cursor on completion of suite
            with g.db.cursor() as cur:
                cur.execute("SELECT passwd from em_users WHERE username = %s", (user, ))
                row = cur.fetchone()
                hash = row[0]
                if pwd_context.verify(pwd, hash):
                    # match, set user
                    session['username'] = user
                    return redirect('orders.html')
                else:
                    # failed, redirect back to login with message
                    flash('Login failed')
                    return redirect(url_for('login'))
    
    
@application.route('/ordersdata')
def get_ordersdata():
    application.logger.debug("in ordersdata")
    page = int(request.args.get('page', default=1))
    limit = int(request.args.get('rows', default=10))
    sidx = request.args.get('sidx', default='id')
    sord = request.args.get('sord', default='asc')
    application.logger.debug("args: %d, %d, %s, %s" % (page, limit, sidx, sord))

    init_resources()
    with g.db:
        application.logger.debug("using existing db connection")
        # get cursor and setup to close cursor on completion of suite
        with g.db.cursor() as cur:
            cur.execute("SELECT count(*) from em_targetorders WHERE state = 'CREATED'")
            row = cur.fetchone()
            count = row[0]
            # calculate the total pages for the query 
            if count > 0 and limit > 0: 
                total_pages = int(math.ceil(float(count)/float(limit)))
            else:
                total_pages = 0
            application.logger.debug("using existing db connection")
             
            # if for some reasons the requested page is greater than the total 
            # set the requested page to total page 
            if page > total_pages:
                page = total_pages
             
            # calculate the starting position of the rows 
            start = limit * page - limit
             
            # if for some reasons start position is negative set it to 0 
            # typical case is that the user type 0 for the requested page 
            if start < 0:
                start = 0
             
            qstr = "SELECT id, generatedBy, type, route, state, timecreated FROM em_targetorders WHERE state = 'CREATED' ORDER BY %s %s LIMIT %d OFFSET %d" % (sidx, sord, limit, start)
            cur.execute(qstr)
            rows = cur.fetchall()
            total = len(rows)
            # package up response
            jdict = {"total":total_pages, "page":page, "records":count}
            jdata = [{"id":row[0], "cell":[row[x] for x in range(len(row))]} for row in rows]
            jdict["rows"] = jdata
            try:
                resp = jsonify(jdict)
            except(e):
                print e
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


@application.route('/orders/symbols')
@application.route('/orders/params')
def get_empty_dataset():
    jdict = {"total":0, "page":0, "records":0}
    jdict["rows"] = []
    resp = jsonify(jdict)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
   
@application.route('/orders/symbols/<id>')
def get_order_symbols(id):
    page = int(request.args.get('page', default=1))
    limit = int(request.args.get('rows', default=10))
    sidx = request.args.get('sidx', default='id')
    sord = request.args.get('sord', default='asc')
    
    init_resources()
    with g.db:
        # get cursor and setup to close cursor on completion of suite
        with g.db.cursor() as cur:
            cur.execute("SELECT count(*) from em_targetordersymbols WHERE orderid = %s", (id,))
            row = cur.fetchone()
            count = row[0]
            # calculate the total pages for the query 
            if count > 0 and limit > 0: 
                total_pages = int(math.ceil(float(count)/float(limit)))
            else:
                total_pages = 0
             
            # if for some reasons the requested page is greater than the total 
            # set the requested page to total page 
            if page > total_pages:
                page = total_pages
             
            # calculate the starting position of the rows 
            start = limit * page - limit
             
            # if for some reasons start position is negative set it to 0 
            # typical case is that the user type 0 for the requested page 
            if start < 0:
                start = 0
             
            ostr = "ORDER BY %s %s LIMIT %d OFFSET %d" % (sidx, sord, limit, start)
            qstr = "SELECT id, symbol, quantity, shortflag, liqest FROM em_targetordersymbols WHERE orderid = %s " + ostr
            cur.execute(qstr, (id, ))
            rows = cur.fetchall()
            total = len(rows)
            # package up response
            # for jqGrid
            jdict = {"total":total_pages, "page":page, "records":count}
            jdata = [{"id":str(row[0]), "cell":[row[x] for x in range(1, len(row))]} for row in rows]
            jdict["rows"] = jdata
            try:
                resp = jsonify(jdict)
            except(e):
                print e
                    
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

  
@application.route('/orders/params/<id>')
def get_order_params(id):
    page = int(request.args.get('page', default=1))
    limit = int(request.args.get('rows', default=10))
    sidx = request.args.get('sidx', default='id')
    sord = request.args.get('sord', default='asc')

    init_resources()
    with g.db:
        # get cursor and setup to close cursor on completion of suite
        with g.db.cursor() as cur:
            cur.execute("SELECT count(*) from em_targetorderconfigs WHERE orderid = %s", (id, ))
            row = cur.fetchone()
            count = row[0]
            # calculate the total pages for the query 
            if count > 0 and limit > 0: 
                total_pages = int(math.ceil(float(count)/float(limit)))
            else:
                total_pages = 0
             
            # if for some reasons the requested page is greater than the total 
            # set the requested page to total page 
            if page > total_pages:
                page = total_pages
             
            # calculate the starting position of the rows 
            start = limit * page - limit
             
            # if for some reasons start position is negative set it to 0 
            # typical case is that the user type 0 for the requested page 
            if start < 0:
                start = 0
             
            ostr = "ORDER BY %s %s LIMIT %d OFFSET %d" % (sidx, sord, limit, start)
            qstr = "SELECT id, param, val FROM em_targetorderconfigs WHERE orderid = %s " + ostr
            cur.execute(qstr, (id, ))
            rows = cur.fetchall()
            total = len(rows)
            # package up response
            # for jqGrid
            jdict = {"total":total_pages, "page":page, "records":count}
            jdata = [{"id":str(row[0]), "cell":[row[x] for x in range(1, len(row))]} for row in rows]
            jdict["rows"] = jdata
            try:
                resp = jsonify(jdict)
            except(e):
                print e
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

  
@application.route('/orders/approve', methods=['POST'])
def approve_orders():
    try:
        orderidstr = request.form["orderids[]"]
    except KeyError:
        application.logger.debug("no orderids in form data")       
        return "failure"
    
    application.logger.debug("got orderids: %s" % (orderidstr, ))
    orderids = orderidstr.split(',')
    init_resources()
    for orderid in orderids:
        application.logger.debug("activating orderid: %s" % (orderid, ))    
        g.em_client.approve_target_order(orderid, "web")
    resp = make_response("success")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":

    application.run()


  
