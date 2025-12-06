from flask import Flask, render_template,url_for,session,redirect,request,flash,make_response
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from base64 import b64encode
import os
# from weasyprint import HTML


app=Flask(__name__)
app.secret_key = "priya"

app.config['UPLOAD_FOLDER'] = 'static/uploads'

def savefile(file):
    if file:
        return file.read()
    return None


def init_db():
  conn=sqlite3.connect("users.db")
  c=conn.cursor()
  c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            visitkey INTEGER UNIQUE,
            name TEXT,
            title TEXT,
            phone TEXT ,
            email TEXT ,
            linkedin TEXT ,
            profile TEXT,
            website TEXT,
            insta TEXT,
            github TEXT
            



            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS education(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    degree TEXT,
    school TEXT,
    fromyear TEXT,
    toyear TEXT,
    description TEXT
)""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS work(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    jobtitle TEXT,
    company TEXT,
    jobfromyear TEXT,
    jobtoyear TEXT,
    jobdescription TEXT
  
  )""")

  c.execute("""CREATE TABLE IF NOT EXISTS languages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            lang TEXT,
            fluency TEXT,
            langdescription TEXT
            
            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS skills(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            skill TEXT,
            skilltype TEXT,
            skillfluency TEXT,
            skilldescription TEXT
            
            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS hobbies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            hobby TEXT,
            hobbydescription TEXT
            
            )""")
  
  
  c.execute("""CREATE TABLE IF NOT EXISTS certifications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            certificationtitle TEXT,
            certschool TEXT,
            certificationdate TEXT,
            certificationdescription TEXT,
            cimagepath BLOB
            
            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS hackathons(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            hackathon TEXT,
            organizedby TEXT,
            hackyprojecttitle TEXT,
            hackyprojectdescription TEXT,
            hackyprojectlink TEXT,
            hackyprojectgitlink TEXT,
            hackydescription TEXT,
            hackimgpath BLOB,
            hackimg2 BLOB,
            hackimg3 BLOB
            
            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS clubs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            clubname TEXT,
            clubposition TEXT,
            clubfromdate TEXT,
            clubtodate TEXT,
            clubdescription TEXT
            
            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS clubwork(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            clubnameforwork TEXT,
            clubworktitle TEXT,
            clubsologrp TEXT,
            clubdescription TEXT,
            workperiodfrom TEXT,
            workperiodto TEXT
            
            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS awards(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            awardtitle TEXT,
            awarddescription TEXT,
            awardimgpath BLOB
            
            )""")
  
  c.execute("""CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            projectname TEXT,
            projectdescription TEXT,
            projectfrom TEXT,
            projectto TEXT,
            projectgithublink TEXT,
            projectdeploymentlink TEXT,
            proimg1path BLOB,
            proimg2path BLOB,
            proimg3path BLOB,
            proimg4path BLOB,
            proimg5path BLOB
            
            )""")

  conn.commit()
  conn.close()
init_db()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=["GET","POST"])
@app.route('/login',methods=["GET","POST"])
def login():
 error=None
 if request.method=="POST":
   username=request.form['username']
   password=request.form['password']
   conn=sqlite3.connect("users.db")
   c=conn.cursor()
   c.execute("SELECT password FROM users WHERE username=?",(username,))
   user=c.fetchone()

   if user and check_password_hash(user[0],password):
    session['username']=username
    #return "You're logged in successfully"
    return redirect(url_for("index"))
   else: 
     error="Invalid Username or password!"
 return render_template("login.html",error=error)


@app.route('/signup',methods=["GET","POST"])
def signup():
  error=None
  if request.method=="POST":
    username=request.form['username']
    password=generate_password_hash(request.form['password'])
    visitkey=request.form['visitkey']

    try:
      conn=sqlite3.connect('users.db')
      c=conn.cursor()
      c.execute("INSERT INTO users (username,password, visitkey) VALUES (?,?,?)",(username,password,visitkey))
      conn.commit()
      conn.close()
      return redirect(url_for('login'))

    except Exception as e:
      error="Username already exists!"
      return render_template("signup.html",error=error)


  return render_template("signup.html",error=error)
     
   
  return render_template("login.html",error=error)
@app.route('/index')
def index():
  if 'username' not in session:
        return redirect(url_for('login'))

  username = session['username']
  conn=sqlite3.connect('users.db')
  c=conn.cursor()
  c.execute("SELECT name, title, phone, email, linkedin, profile, website, insta, github FROM users WHERE username = ?", (username,))
  basic = c.fetchall()
  conn.commit()
  conn.close()
  return render_template("index.html",basic=basic)

@app.route("/download_pdf")
def download_pdf():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT name, title, phone, email, linkedin, profile, website, insta, github FROM users WHERE username = ?", (username,))
    basic = c.fetchall()

    c.execute("SELECT degree, school, fromyear, toyear, description FROM education WHERE username = ?", (username,))
    education = c.fetchall()

    c.execute("SELECT jobtitle, company, jobfromyear,jobtoyear, jobdescription FROM work WHERE username = ?", (username,))
    work = c.fetchall()

    c.execute("SELECT lang, fluency, langdescription FROM languages WHERE username = ?", (username,))
    languages = c.fetchall()

    c.execute("SELECT skill, skilltype, skillfluency, skilldescription FROM skills WHERE username = ?", (username,))
    skills = c.fetchall()

    c.execute("SELECT hobby, hobbydescription FROM hobbies WHERE username = ?", (username,))
    hobbies = c.fetchall()

    c.execute("SELECT certificationtitle, certschool, certificationdate, certificationdescription, cimagepath FROM certifications WHERE username = ?", (username,))
    certifications = c.fetchall()

    c.execute("SELECT hackathon, organizedby, hackyprojecttitle, hackyprojectdescription, hackyprojectlink, hackyprojectgitlink, hackydescription, hackimgpath, hackimg2, hackimg3 FROM hackathons WHERE username = ?", (username,))
    hackathons = c.fetchall()

    c.execute("SELECT clubname, clubposition, clubfromdate, clubtodate, clubdescription FROM clubs WHERE username = ?", (username,))
    clubs = c.fetchall()

    c.execute("SELECT clubnameforwork, clubworktitle, clubsologrp, clubdescription, workperiodfrom, workperiodto FROM clubwork WHERE username = ?", (username,))
    clubwork = c.fetchall()

    c.execute("SELECT awardtitle, awarddescription, awardimgpath FROM awards WHERE username = ?", (username,))
    awards = c.fetchall()

    c.execute("SELECT projectname, projectdescription, projectfrom, projectto, projectgithublink, projectdeploymentlink, proimg1path, proimg2path, proimg3path, proimg4path, proimg5path FROM projects WHERE username = ?", (username,))
    projects = c.fetchall()


    conn.close()
    rendered = render_template(
        "portfoliodownloadable.html",  
        basic=basic,
        education=education,
        work=work,
        skills=skills,
        languages=languages,
        hackathons=hackathons,
        projects=projects,
        certifications=certifications,
        awards=awards,
        hobbies=hobbies,
        clubs=clubs,
        clubwork=clubwork
    )
    pdf = HTML(string=rendered, base_url='').write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=portfolio.pdf'
    return response

@app.route('/portfolio')
def portfolio():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT name, title, phone, email, linkedin, profile, website, insta, github FROM users WHERE username = ?", (username,))
    basic = c.fetchall()

    c.execute("SELECT degree, school, fromyear, toyear, description FROM education WHERE username = ?", (username,))
    education = c.fetchall()

    c.execute("SELECT jobtitle, company, jobfromyear,jobtoyear, jobdescription FROM work WHERE username = ?", (username,))
    work = c.fetchall()

    c.execute("SELECT lang, fluency, langdescription FROM languages WHERE username = ?", (username,))
    languages = c.fetchall()

    c.execute("SELECT skill, skilltype, skillfluency, skilldescription FROM skills WHERE username = ?", (username,))
    skills = c.fetchall()

    c.execute("SELECT hobby, hobbydescription FROM hobbies WHERE username = ?", (username,))
    hobbies = c.fetchall()

    c.execute("SELECT certificationtitle, certschool, certificationdate, certificationdescription, cimagepath FROM certifications WHERE username = ?", (username,))
    certifications = c.fetchall()

    c.execute("SELECT hackathon, organizedby, hackyprojecttitle, hackyprojectdescription, hackyprojectlink, hackyprojectgitlink, hackydescription, hackimgpath, hackimg2, hackimg3 FROM hackathons WHERE username = ?", (username,))
    hackathons = c.fetchall()

    c.execute("SELECT clubname, clubposition, clubfromdate, clubtodate, clubdescription FROM clubs WHERE username = ?", (username,))
    clubs = c.fetchall()

    c.execute("SELECT clubnameforwork, clubworktitle, clubsologrp, clubdescription, workperiodfrom, workperiodto FROM clubwork WHERE username = ?", (username,))
    clubwork = c.fetchall()

    c.execute("SELECT awardtitle, awarddescription, awardimgpath FROM awards WHERE username = ?", (username,))
    awards = c.fetchall()

    c.execute("SELECT projectname, projectdescription, projectfrom, projectto, projectgithublink, projectdeploymentlink, proimg1path, proimg2path, proimg3path, proimg4path, proimg5path FROM projects WHERE username = ?", (username,))
    projects = c.fetchall()


    conn.close()

    return render_template("portfolio.html", basic=basic, education=education, work=work, languages=languages, skills=skills, hobbies=hobbies, certifications=certifications, hackathons=hackathons, clubs=clubs, clubwork=clubwork, awards=awards, projects=projects)



import base64

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

  

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
         
        name = request.form['name']
        title = request.form['title']
        phone = request.form['phone']
        email = request.form['email']
        linkedin = request.form['linkedin']
        website=request.form['website']
        insta=request.form['insta']
        github=request.form['github']
        profile = request.form.get('profile')

        degrees = request.form.getlist("degree[]")
        schools = request.form.getlist("school[]")
        admyears = request.form.getlist("fromyear[]")
        gradyears = request.form.getlist("toyear[]")
        descriptions = request.form.getlist("description[]")

        jobtitles=request.form.getlist("jobtitle[]")
        companies=request.form.getlist("company[]")
        jobfromyears=request.form.getlist("jobfromyear[]")
        jobtoyears=request.form.getlist("jobtoyear[]")
        jobdecriptions=request.form.getlist("jobdescription[]")

        #languages ku
        languages=request.form.getlist("language[]")
        fluencies=request.form.getlist("fluency[]")
        langdescriptions=request.form.getlist("langdescription[]")


        #skills ku
        skills=request.form.getlist("skill[]")
        skilltypes=request.form.getlist("skilltype[]")
        skillfluencies=request.form.getlist("skill_level[]")
        skilldescriptions=request.form.getlist("skilldescription[]")

        #hobbies ku
        hobbies=request.form.getlist("hobby[]")
        hobbydescriptions=request.form.getlist("hobbydescription[]")

        #certifications ku
        certtitles=request.form.getlist("certification[]")
        certschools=request.form.getlist("certschool[]")
        certdates=request.form.getlist("certificationdate[]")
        certdescs=request.form.getlist("certificationdescription[]")
        certpics=request.files.getlist("cimagepath[]")
        savedcertpic=[savefile(pic) for pic in certpics]

        #projects ku
        protitles=request.form.getlist("proname[]")
        prodescs=request.form.getlist("prodesc[]")
        prostartdates=request.form.getlist("profromdate[]")
        protodates=request.form.getlist("protodate[]")
        progitlink=request.form.getlist("progitlink[]")
        prodeplink=request.form.getlist("prodeplink[]")
        proimgs1=request.files.getlist("proimg1[]")
        proimgs2=request.files.getlist("proimg2[]")
        proimgs3=request.files.getlist("proimg3[]")
        proimgs4=request.files.getlist("proimg4[]")
        proimgs5=request.files.getlist("proimg5[]")
        savedpro1pic=[savefile(pic) for pic in proimgs1]
        savedpro2pic=[savefile(pic) for pic in proimgs2]
        savedpro3pic=[savefile(pic) for pic in proimgs3]
        savedpro4pic=[savefile(pic) for pic in proimgs4]
        savedpro5pic=[savefile(pic) for pic in proimgs5]


        #hackathons ku
        hacknames=request.form.getlist("hackname[]")
        harkorgbys=request.form.getlist("hackorgname[]")
        hackprotitles=request.form.getlist("hackproname[]")
        hackprodescs=request.form.getlist("hackprodescription[]")
        hackprodeplinks=request.form.getlist("hackprodeplink[]")
        hackprogitlinks=request.form.getlist("hackyprogitlink[]")
        hackdescs=request.form.getlist("hackydesc[]")
        hackimg1s=request.files.getlist("hackypic[]")
        hackimg2s=request.files.getlist("hackypic2[]")
        hackimg3s=request.files.getlist("hackypic3[]")
        savedhack1pic=[savefile(pic) for pic in hackimg1s ]
        savedhack2pic=[savefile(pic) for pic in hackimg2s ]
        savedhack3pic=[savefile(pic) for pic in hackimg3s ]

        #awards ku
        awardsnames=request.form.getlist("award[]")
        awardsdecs=request.form.getlist("awarddescription[]")
        awardspics=request.files.getlist("awardpic[]")
        savedawardpic=[savefile(pic) for pic in awardspics]
        

        #clubs ku 
        clubsnames=request.form.getlist("clubname[]")
        clubsposs=request.form.getlist("clubpos[]")
        clubsfromdates=request.form.getlist("clubfromdate[]")
        clubstodates=request.form.getlist("clubprotodate[]")
        clubsdescs=request.form.getlist("clubdesc[]")


        # #clubworks ku
        clubnameforworks=request.form.getlist("clubnameforwork[]")
        clubprosnames=request.form.getlist("clubproname[]")
        clubsologrpinfos=request.form.getlist("clubsologrp[]")
        clubprofromdates=request.form.getlist("clubprofromdate[]")
        clubprotodates=request.form.getlist("clubprotodate[]")
        clubworkdescs=request.form.getlist("clubworkdesc[]")
        
        

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("""
            UPDATE users SET name=?, title=?, phone=?, email=?, linkedin=?, profile=?, insta=?, website=?, github=? WHERE username=?
                  """, (name, title, phone, email, linkedin, profile, insta, website, github, session["username"]))



        for d, s, ay, gy, desc in zip(degrees, schools, admyears, gradyears, descriptions):
            c.execute("""
                INSERT INTO education (username, degree, school, fromyear, toyear, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session["username"], d, s, ay, gy, desc))
        for jt,co,fd,td,jd in zip(jobtitles,companies,jobfromyears,jobtoyears,jobdecriptions):
            c.execute("""
                 INSERT INTO work (username,jobtitle,company,jobfromyear,jobtoyear,jobdescription) VALUES (?,?,?,?,?,?)
                      """,(session['username'],jt,co,fd,td,jd))
        
        #lang
        for l,f,ld in zip(languages,fluencies,langdescriptions):
            c.execute("""
              INSERT INTO languages (username,lang,fluency,langdescription) VALUES (?,?,?,?)
        """,(session['username'],l,f,ld))
            
        #skill
        for s,st,sf,sd in zip( skills,skilltypes,skillfluencies,skilldescriptions):
            c.execute("""
              INSERT INTO skills (username,skill,skilltype,skillfluency,skilldescription) VALUES (?,?,?,?,?)
        """,(session['username'],s,st,sf,sd))
            
        #hobby
        for h,hd in zip(hobbies,hobbydescriptions):
            c.execute("""
              INSERT INTO hobbies (username,hobby,hobbydescription) VALUES (?,?,?)
        """,(session['username'],h,hd))

        #certifications ku
        for cert_title, cs, cd, cds, scp in zip(certtitles, certschools, certdates, certdescs, savedcertpic):
            c.execute("""
    INSERT INTO certifications(username, certificationtitle, certschool, certificationdate, certificationdescription, cimagepath)
    VALUES (?, ?, ?, ?, ?, ?)
""", (session['username'], cert_title, cs, cd, cds, scp))



        #projects ku
        for pt,pd,psd,ped,pgl,pdl,sp1,sp2,sp3,sp4,sp5 in zip(protitles, prodescs, prostartdates, protodates, progitlink, prodeplink, savedpro1pic, savedpro2pic, savedpro3pic, savedpro4pic, savedpro5pic):
            c.execute("""
              INSERT INTO projects (username,projectname, projectdescription, projectfrom, projectto, projectgithublink, projectdeploymentlink, proimg1path, proimg2path, proimg3path, proimg4path, proimg5path) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,(session['username'],pt,pd,psd,ped,pgl,pdl,sp1,sp2,sp3,sp4,sp5))
            
        #hackathons ku
        for hn,ho,hp,hpt,hpd,hpdl,hpgl,sp1,sp2,sp3 in zip(hacknames, harkorgbys, hackprotitles, hackprodescs, hackprodeplinks, hackprogitlinks, hackdescs, savedhack1pic, savedhack2pic, savedhack3pic):
            c.execute("""
              INSERT INTO hackathons (username, hackathon, organizedby, hackyprojecttitle, hackyprojectdescription, hackyprojectlink, hackyprojectgitlink, hackydescription, hackimgpath, hackimg2, hackimg3) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,(session['username'], hn,ho,hp,hpt,hpd,hpdl,hpgl,sp1,sp2,sp3))
            
        #clubs ku
        for cn,cp,cfd,ctd,cd in zip(clubsnames, clubsposs, clubsfromdates, clubstodates, clubsdescs):
            c.execute("""
              INSERT INTO clubs (username, clubname, clubposition, clubfromdate, clubtodate, clubdescription) VALUES (?,?,?,?,?,?)
        """,(session['username'],cn,cp,cfd,ctd,cd))
            
        #clubs work ku
        for clubname, worktitle, sologrp, desc, fromd, tod in zip(clubnameforworks, clubprosnames, clubsologrpinfos, clubworkdescs, clubprofromdates, clubprotodates):

            c.execute("""
        INSERT INTO clubwork(username,clubnameforwork,  clubworktitle, clubsologrp, 
                             clubdescription, workperiodfrom, workperiodto)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session['username'], clubname, worktitle, sologrp, desc, fromd, tod))

            
        #awards ku
        for an,ad,ap in zip(awardsnames,awardsdecs,savedawardpic):
            c.execute("""
              INSERT INTO awards (username, awardtitle, awarddescription, awardimgpath) VALUES (?,?,?,?)
        """,(session['username'],an,ad,ap))

        conn.commit()
        conn.close()

        return redirect(url_for("portfolio"))

    return render_template("input.html")

@app.route('/public_portfolio', methods=['GET', 'POST'])
def public_portfolio():
    error=None;
    if request.method == 'POST':
        username = request.form['username']
        visitkey = request.form['visitorkey']

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username=? AND visitkey=?", (username, visitkey))
        row = c.fetchone()
        conn.close()

        if not row:
            error= "Invalid username or visitor key"

        return redirect(f'/visitorview/{username}/{visitkey}')

    return render_template("visitor.html",error=error)



@app.route('/visitorview/<username>/<visitkey>')
def visitorview(username, visitkey):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username=? AND visitkey=?", (username, visitkey))
    row = c.fetchone()
    if not row:
        conn.close()
        return "Invalid visitor key!"

    c.execute("SELECT name, title, phone, email, linkedin, profile, website, insta, github FROM users WHERE username = ?", (username,))
    basic = c.fetchall()

    c.execute("SELECT degree, school, fromyear, toyear, description FROM education WHERE username = ?", (username,))
    education = c.fetchall()

    c.execute("SELECT jobtitle, company, jobfromyear,jobtoyear, jobdescription FROM work WHERE username = ?", (username,))
    work = c.fetchall()

    c.execute("SELECT lang, fluency, langdescription FROM languages WHERE username = ?", (username,))
    languages = c.fetchall()

    c.execute("SELECT skill, skilltype, skillfluency, skilldescription FROM skills WHERE username = ?", (username,))
    skills = c.fetchall()

    c.execute("SELECT hobby, hobbydescription FROM hobbies WHERE username = ?", (username,))
    hobbies = c.fetchall()

    c.execute("SELECT certificationtitle, certschool, certificationdate, certificationdescription, cimagepath FROM certifications WHERE username = ?", (username,))
    certifications = c.fetchall()

    c.execute("SELECT hackathon, organizedby, hackyprojecttitle, hackyprojectdescription, hackyprojectlink, hackyprojectgitlink, hackydescription, hackimgpath, hackimg2, hackimg3 FROM hackathons WHERE username = ?", (username,))
    hackathons = c.fetchall()

    c.execute("SELECT clubname, clubposition, clubfromdate, clubtodate, clubdescription FROM clubs WHERE username = ?", (username,))
    clubs = c.fetchall()

    c.execute("SELECT clubnameforwork, clubworktitle, clubsologrp, clubdescription, workperiodfrom, workperiodto FROM clubwork WHERE username = ?", (username,))
    clubwork = c.fetchall()

    c.execute("SELECT awardtitle, awarddescription, awardimgpath FROM awards WHERE username = ?", (username,))
    awards = c.fetchall()

    c.execute("SELECT projectname, projectdescription, projectfrom, projectto, projectgithublink, projectdeploymentlink, proimg1path, proimg2path, proimg3path, proimg4path, proimg5path FROM projects WHERE username = ?", (username,))
    projects = c.fetchall()


    conn.close()

    return render_template("visitorview.html", basic=basic, education=education, work=work, languages=languages, skills=skills, hobbies=hobbies, certifications=certifications, hackathons=hackathons, clubs=clubs, clubwork=clubwork, awards=awards, projects=projects)


@app.route("/deletedb", methods=["POST","GET"])
def deletedb():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    tables = [
        "users",
        "education",
        "work",
        "languages",
        "skills",
        "hobbies",
        "certifications",
        "hackathons",
        "clubs",
        "clubwork",
        "awards",
        "projects"
    ]

    for table in tables:
        c.execute(f"DELETE FROM {table} WHERE username = ?", (username,))

    conn.commit()
    conn.close()

    flash("Your portfolio data was deleted successfully!", "success")
    return redirect(url_for('index'))

   

if __name__=="__main__":
   app.run(host="0.0.0.0", debug=True)