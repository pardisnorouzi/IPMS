import datetime
from flask import Flask , session, redirect, url_for, request, render_template
import oracledb
import hashlib

# Replace with your actual Oracle database credentials
user = 'SYSTEM'
password = 'root'
port = 1521
service_name = 'XEPDB1'
conn_string = "localhost:{port}/{service_name}".format(
    port=port, service_name=service_name)
app = Flask(__name__)
app.secret_key = 'IPMS-Secret'

data = []
id = []




@app.route('/')
def index():
    return render_template('home.html',session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in session:
        # User is already logged in, redirect to index page
        return redirect(url_for('index'))

    err = False
    if request.method == 'POST':
        username = request.form['username']
        passh = hashlib.md5(request.form['password'].encode()).hexdigest()
        

        con = oracledb.connect(user=user, password=password, dsn=conn_string)

        with con.cursor() as cursor:
            cursor.execute("SELECT IPMS.LOGIN.password, IPMS.USERS.* FROM IPMS.LOGIN LEFT JOIN IPMS.USERS ON IPMS.LOGIN.login_id = IPMS.USERS.login_id WHERE LOWER(IPMS.LOGIN.email) = LOWER(:email)", {"email": username})
            result = cursor.fetchone()

            if result:
                print(result)
                print(result[7])
                if result[6] == 0 and result[7] == 0:
                    err = 'Your account was not approved. Contact Coordinator directly for more information.'
                elif passh == result[0]:
                    # Username and password are valid, so set user as logged in
                    session['username'] = username
                    session['usertype'] = result[9]
                    session['isapproved'] = result[7]
                    session['ispending'] = result[6]
                    session['userid'] = result[1]
                    print(session)
                    print(result)
                    return redirect(url_for('dash'))
                else:
                    err = 'Invalid username or password'
            
        
        return render_template('login.html',err=err)
    
    return render_template('login.html',err=err)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('usertype', None)
    session.pop('isapproved', None)
    session.pop('ispending', None)
    session.pop('userid', None)
    return redirect(url_for('index'))

@app.route('/dash')
def dash():
    return render_template('dash.html',session=session)

@app.route('/my_placements', methods=['GET', 'POST'])
def my_placements():
    if 'username' not in session or session['usertype'] != 3 or session['isapproved'] != 1:
        # redirect to index page
        return redirect(url_for('index'))
    err = False
    msg = False
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    data = []
    pr = {}
    user_id = session['userid']

    cur.execute('SELECT COUNT(*) FROM IPMS.STUDENTSPREFERENCES WHERE user_id = :user_id', user_id=user_id)
    has_prefs = cur.fetchone()[0]

    if request.method == 'POST':
        puid = request.form['uid']
        print(0)
        print(user_id)
        print(puid)
        # if user_id != puid:
        #     return redirect(url_for('index'))
        
        action = request.form['act']
        print(1)
        if action == 'save_pr':
            print(2)
            pr[1] = request.form['priority1']
            pr[2] = request.form['priority2']
            pr[3] = request.form['priority3']
            if has_prefs:
                return redirect(url_for('index'))    
            elif len(pr[1]) == 0 or len(pr[2]) == 0 or len(pr[3]) == 0:
                err = 'Please Select all 3 priorities'
            elif pr[1] == pr[2] or pr[2] == pr[3] or pr[1] == pr[3]:
                err = 'Selections must be different'
            else:
                for x in range(1, 4):
                    try: 
                        cur.execute("INSERT INTO IPMS.STUDENTSPREFERENCES(priority_id, user_id, placement_id, is_pending, is_approved, created, updated) VALUES (:0, :1, :2,1,0,SYSTIMESTAMP,SYSTIMESTAMP)", 
                                    (x,  puid, pr[x]))     
                        con.commit()
                    except Exception as e:
                        print("Error inserting data:", e)
                        err = e
                        con.rollback() 
                cur.close()
                con.close()

                return render_template('after_submit.html',e=err)                 
        
    if has_prefs == 0:
        cur.execute("SELECT IPMS.PLACEMENTS.*, IPMS.COMPANIES.* \
                    FROM IPMS.PLACEMENTS \
                    LEFT JOIN IPMS.COMPANIES ON IPMS.PLACEMENTS.company_id = IPMS.COMPANIES.company_id \
                    WHERE IPMS.PLACEMENTS.status_id = 1")
        allplacements = cur.fetchall()

        for row in allplacements:
            # print(row)
            data.append({"plid": row[0], "title": row[1],
                "desc": row[2], "skills": row[3], "comname": row[10],"row":row})
        cur.close()
        con.close() 
        return render_template('all_placements.html',session=session,data=data,user_id=user_id)       

    else:
        cur.execute("SELECT IPMS.STUDENTSPREFERENCES.*, IPMS.PLACEMENTS.*, IPMS.PRIORITIES.*\
                    FROM IPMS.STUDENTSPREFERENCES \
                    LEFT JOIN IPMS.PLACEMENTS ON IPMS.STUDENTSPREFERENCES.placement_id = IPMS.PLACEMENTS.placement_id \
                    LEFT JOIN IPMS.PRIORITIES ON IPMS.STUDENTSPREFERENCES.priority_id = IPMS.PRIORITIES.priority_id \
                    WHERE IPMS.STUDENTSPREFERENCES.user_id = :user_id ORDER BY IPMS.STUDENTSPREFERENCES.priority_id ASC", user_id=user_id)

        allperfs = cur.fetchall()
        for row in allperfs:
            # print(row)
            company_id=row[13]
            cur.execute("SELECT * FROM IPMS.COMPANIES WHERE company_id = :company_id", company_id=company_id)
            company = cur.fetchone()[1]

            is_s = ''
            if row[4] == 1 and row[5] == 0:
                is_c = 'yellow'
                is_s = 'Pending'
            elif row[4] == 0 and row[5] == 1:
                is_c = 'green'
                is_s = 'Approved'
            elif row[4] == 0 and row[5] == 0:
                is_c = 'red'
                is_s = 'Not Approved'
            else:
                is_c = 'black'
                is_i = 'Uknown'

            data.append({"userid":user_id, "prefid": row[0], "prid": row[1],
                    "placid": row[3], "is_p": row[4], "is_a":row[5], "is_s":is_s,"is_c":is_c ,"platitle": row[9], "comname": company,"prname":row[18],"row":row})
            

    cur.close()
    con.close()
    return render_template('my_placements.html',session=session,data=data)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user_account():
    if 'username' in session:
        # User is already logged in, redirect to index page
        return redirect(url_for('index'))
    
    return render_template('new_user.html');

@app.route('/submit_new_user', methods=['GET', 'POST'])
def new_user_submit():
    if 'username' in session:
        # User is already logged in, redirect to index page
        return redirect(url_for('index'))
    
    err = False
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    phone = request.form["phone"]
    passr = request.form["password"]
    passh = hashlib.md5(passr.encode()).hexdigest()
    address = request.form["address"]

    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()

    cur.execute('SELECT COUNT(*) FROM IPMS.LOGIN WHERE email = :email', email=email)
    exists = cur.fetchone()[0]
    
    if exists == 0:
        try: 
            id_var = cur.var(oracledb.NUMBER)
            cur.execute("INSERT INTO IPMS.LOGIN(email, password, created, updated) VALUES (:0, :1,SYSTIMESTAMP,SYSTIMESTAMP) RETURNING login_id INTO :id", 
                        (email,passh,id_var))  
            new_id = id_var.getvalue()

            con.commit()   

            cur.execute("INSERT INTO IPMS.USERS(first_name, last_name, address, telephone, is_pending, is_approved, login_id, user_type_id, created, updated) VALUES (:0, :1, :2,:3,:4,:5,:6,:7,SYSTIMESTAMP,SYSTIMESTAMP)", 
                        (fname,  lname, address,phone,1,0,new_id[0],3))     
            con.commit()

        except Exception as e:
            print("Error inserting data:", e)
            err = e
            con.rollback()
    else:
        err = 'Email already exists'
              
    cur.close()
    con.close()

    return render_template('after_submit.html',e=err)

@app.route('/user_placement', methods=['GET', 'POST'])
def user_placement():
    if 'username' not in session or session['usertype'] != 1 or session['isapproved'] != 1:
        # User is not already logged in, redirect to index page
        return redirect(url_for('index'))
    err = False
    msg = False
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    data = []    

    if request.method == 'POST':
        action = request.form['act']
        user_id = request.form["uid"]

        if action == 'showplacement':
            cur.execute("SELECT IPMS.STUDENTSPREFERENCES.*, IPMS.PLACEMENTS.*, IPMS.PRIORITIES.*\
                    FROM IPMS.STUDENTSPREFERENCES \
                    LEFT JOIN IPMS.PLACEMENTS ON IPMS.STUDENTSPREFERENCES.placement_id = IPMS.PLACEMENTS.placement_id \
                    LEFT JOIN IPMS.PRIORITIES ON IPMS.STUDENTSPREFERENCES.priority_id = IPMS.PRIORITIES.priority_id \
                    WHERE IPMS.STUDENTSPREFERENCES.is_approved = 0 AND IPMS.STUDENTSPREFERENCES.user_id = :user_id ORDER BY IPMS.STUDENTSPREFERENCES.priority_id ASC", user_id=user_id)

            allperfs = cur.fetchall()
            for row in allperfs:
                # print(row)
                company_id=row[13]
                cur.execute("SELECT * FROM IPMS.COMPANIES WHERE company_id = :company_id", company_id=company_id)
                company = cur.fetchone()[1]

                data.append({"userid":user_id, "prefid": row[0], "prid": row[1],
                     "placid": row[3], "platitle": row[9], "comname": company,"prname":row[18],"row":row})
                
            # print(data)
            # Close the cursor and connection
            cur.close()
            con.close()
            return render_template('user_placement.html',data=data,user_id=user_id)    
        elif action == 'approve':
            studentspreferences_id = request.form["placement"]
            cur.execute("UPDATE IPMS.STUDENTSPREFERENCES SET is_pending = 0, is_approved = 0, updated = SYSTIMESTAMP WHERE user_id = :user_id", {'user_id': user_id})
            con.commit()
            cur.execute("UPDATE IPMS.STUDENTSPREFERENCES SET is_approved = 1, updated = SYSTIMESTAMP WHERE user_id = :user_id AND studentspreferences_id = :studentspreferences_id" , {'user_id': user_id, 'studentspreferences_id':studentspreferences_id})
            con.commit()            
            return redirect(url_for('users'))   

    #Default action return to users    
    return redirect(url_for('users'))    


@app.route('/users', methods=['GET', 'POST'])
def users():
    if 'username' not in session or session['usertype'] != 1 or session['isapproved'] != 1:
        # User is not already logged in, redirect to index page
        return redirect(url_for('index'))
    err = False
    msg = False
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    data = []


    if request.method == 'POST':
        action = request.form['act']
        if action=='reject' or action=='appr':
            usersid = request.form["uid"]
            if action=='reject':
                is_pending = 0
                is_approved = 0
            elif action=='appr':
                is_pending = 0
                is_approved = 1
            else:
                is_pending = 1
                is_approved = 0

            cur.execute("UPDATE IPMS.USERS SET is_pending = :is_pending, is_approved = :is_approved, updated = SYSTIMESTAMP WHERE user_id = :user_id", {'user_id': usersid, 'is_pending': is_pending, 'is_approved': is_approved})
            con.commit() 
            msg = "User Status updated!"  


   # Default actions of companies page

    cur.execute('select IPMS.USERS.*, IPMS.LOGIN.email from IPMS.USERS LEFT JOIN IPMS.LOGIN ON IPMS.LOGIN.login_id = IPMS.USERS.login_id')
    allusers = cur.fetchall()

    for row in allusers:
        # print(row)
        user_id = row[0]
        priority_count = 0
        priority = False
        
        cur.execute("SELECT IPMS.STUDENTSPREFERENCES.placement_id, IPMS.PLACEMENTS.title \
                    FROM IPMS.STUDENTSPREFERENCES \
                    LEFT JOIN IPMS.PLACEMENTS ON IPMS.STUDENTSPREFERENCES.placement_id = IPMS.PLACEMENTS.placement_id \
                    WHERE IPMS.STUDENTSPREFERENCES.is_approved = 1 AND IPMS.STUDENTSPREFERENCES.user_id = :user_id", user_id=user_id)
        
        
        appr_placemnt = cur.fetchone()
        if appr_placemnt:
            priority = appr_placemnt[1]
            # print(priority)
        else:
            cur.execute('SELECT COUNT(*) FROM IPMS.STUDENTSPREFERENCES WHERE user_id = :user_id AND is_pending = 1', user_id=user_id)
            priority_count = cur.fetchone()[0]
            # print(priority_count)


        status = 0 # pending
        if row[5]==0: #not pending
            if row[6]==1: #not pending an approved
                status = 1 # approved
            else : #not pending and rejected
                status = 2 # rejected

        data.append({"fname": row[1], "lname": row[2],
                    "add": row[3], "phone": row[4],"user_id":row[0],
                    "pend": row[5],"appr": row[6],"type": row[8], "email": row[11],
                    "status": status, "row": row,
                    "priority_count": priority_count, "priority":priority
                    })
    # Close the cursor and connection
    cur.close()
    con.close()
    # Pass the data to the template to display in the HTML table    

    return render_template('users.html',data=data,e=err,msg=msg)


@app.route('/placements', methods=['GET', 'POST'])
def placements():
    if 'username' not in session or session['usertype'] != 1 or session['isapproved'] != 1:
        # User is already logged in, redirect to index page
        return redirect(url_for('index'))
    err = False
    msg = False
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    data = []

    cur.execute("SELECT status_id, status_type FROM IPMS.STATUS")
    status_types = cur.fetchall()

    cur.execute("SELECT company_id, company_name FROM IPMS.COMPANIES")
    companies = cur.fetchall()

    if request.method == 'POST':
        action = request.form['act']
        if action=='addplacement':
            title = request.form["title"]
            desc = request.form["desc"]
            skills = request.form["skills"]
            statid = request.form["status"]
            coid = request.form["company"]
            userid = session["userid"]


            try: 
                cur.execute("INSERT INTO IPMS.PLACEMENTS(title, description, skills, status_id, company_id, user_id, created, updated) VALUES (:0, :1, :2, :3, :4, :5 ,SYSTIMESTAMP,SYSTIMESTAMP)", 
                            (title,  desc, skills, statid,coid,userid))     
                con.commit()

            except Exception as e:
                print("Error inserting data:", e)
                err = e
                con.rollback()
            
            msg = "Placement Added Successfuly"

        elif action=='deleteplacement':
            placement_id = request.form["id"]
            cur.execute("DELETE FROM IPMS.PLACEMENTS WHERE placement_id = :placement_id", 
                            placement_id=placement_id)     
            con.commit() 
            msg = "Placement Removed Successfuly"

        # elif action=='editcompany':
            # reserved for editing companies

    query = 'SELECT * FROM IPMS.PLACEMENTS \
                LEFT JOIN IPMS.STATUS ON IPMS.PLACEMENTS.status_id = IPMS.STATUS.status_id \
                LEFT JOIN IPMS.COMPANIES ON IPMS.PLACEMENTS.company_id = IPMS.COMPANIES.company_id'
    
    # cur.execute('select * from IPMS.PLACEMENTS')
    cur.execute(query)
    for row in cur:
        print(row)
        data.append({"title": row[1], "desc": row[2],
                    "skills": row[3], "status": row[10], "company": row[14],"placement_id":row[0],"row":row})
    # Close the cursor and connection
    cur.close()
    con.close()
    # Pass the data to the template to display in the HTML table


    return render_template('placements.html',data=data,e=err,msg=msg,status_types=status_types,companies=companies)


@app.route('/companies', methods=['GET', 'POST'])
def companies():
    if 'username' not in session or session['usertype'] != 1 or session['isapproved'] != 1:
        # User is already logged in, redirect to index page
        return redirect(url_for('index'))
    err = False
    msg = False
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    data = []

    if request.method == 'POST':
        action = request.form['act']
        if action=='addcompany':
            compn = request.form["companyname"]
            compa = request.form["companyadd"]
            compp = request.form["companyphone"]
            compe = request.form["companyemail"]

            try: 
                cur.execute("INSERT INTO IPMS.COMPANIES(company_name, address, telephone, email, created, updated) VALUES (:0, :1, :2,:3,SYSTIMESTAMP,SYSTIMESTAMP)", 
                            (compn,  compa, compp, compe))     
                con.commit()

            except Exception as e:
                print("Error inserting data:", e)
                err = e
                con.rollback()
            
            msg = "Company Added Successfuly"

        elif action=='deletecompany':
            company_id = request.form["id"]
            cur.execute("DELETE FROM IPMS.COMPANIES WHERE company_id = :company_id", 
                            company_id=company_id)     
            con.commit() 
            msg = "Company Removed Successfuly"

        # elif action=='editcompany':
            # reserved for editing companies

    # Default actions of companies page

    cur.execute('select * from IPMS.COMPANIES')
    for row in cur:
        data.append({"company_name": row[1], "address": row[2],
                    "telephone": row[3], "email": row[4],"company_id":row[0]})
    # Close the cursor and connection
    cur.close()
    con.close()
    # Pass the data to the template to display in the HTML table


    return render_template('companies.html',data=data,e=err,msg=msg)




if __name__ == '__main__':
    app.run()
