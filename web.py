# noinspection PyInterpreter
from flask import Flask, flash, redirect, render_template, request, session, abort
import sqlite3 as sql
import os
import hashlib
from sqlalchemy.orm import sessionmaker
from tabledef import *
from tabledeflog import *
import datetime
engine = create_engine('sqlite:///user.db', echo=True)
engineuser = create_engine('sqlite:///userlog.db', echo=True)
app = Flask(__name__)
app.secret_key = os.urandom(24)
search = ""
searchbook = ""
searchmoviestream = ""
chatid = ""

@app.route('/musikdb')
def listdbd():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("select * from music")
         rows = cur.fetchall();
         return render_template("musikdb.html",rows = rows)


@app.route('/moviestreamdb')
def moviebd():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/vid.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("select * from mp4")

         rows = cur.fetchall();
         return render_template("moviestreamdb.html", rows=rows)

@app.route('/searchbookasc')
def searchbookasc():
   global searchbook
   con = sql.connect("static/bot.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT id, title, author, year from books WHERE (upper(title) GLOB upper(?)) OR (upper(author) GLOB upper(?)) ORDER BY id ASC;", (searchbook, searchbook))
   rows = cur.fetchall();
   return render_template("booklist.html", rows=rows)

@app.route('/searchbookdesc')
def searchbookdsc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      global searchbook
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT id, title, author, year from books WHERE (upper(title) GLOB upper(?)) OR (upper(author) GLOB upper(?))  ORDER BY id DESC", (searchbook, searchbook))
      rows = cur.fetchall();
      return render_template("booklist.html", rows=rows)

@app.route('/musikdbasc')
def listdbasc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from music ORDER BY ID ASC")

      rows = cur.fetchall();
      return render_template("musikdb.html", rows=rows)


@app.route('/musikdbdesc')
def listdbdesc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from music ORDER BY ID DESC")

      rows = cur.fetchall();
      return render_template("musikdb.html", rows=rows)

@app.route('/bookdb')
def list2():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("select * from books")

         rows = cur.fetchall();
         return render_template("booklistuf.html", rows=rows)

@app.route('/bookdbasc')
def bookdbasc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from books ORDER BY id asc")

      rows = cur.fetchall();
      return render_template("booklistuf.html", rows=rows)

@app.route('/bookdbdsc')
def bookdbdsc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from books ORDER BY id desc")

      rows = cur.fetchall();
      return render_template("booklistuf.html", rows=rows)


@app.route('/filedb')
def list3():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("select * from files")

         rows = cur.fetchall();
         return render_template("filelist.html", rows=rows)

@app.route('/searchfile')
def searchfile():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         return render_template('searchfile.html')

@app.route('/searchfileres',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      search = request.form['search']
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row
      search = "*" + search + "*"
      cur = con.cursor()
      cur.execute("SELECT ID, NAME, FILETYPE FROM files WHERE (upper(NAME) GLOB upper(?)) OR (upper(FILETYPE) GLOB upper(?)) OR (upper(tags) GLOB upper(?));", (search, search, search))

      rows = cur.fetchall();
      return render_template("filelist.html",rows = rows)

@app.route('/searchmusictitle')
def searchmusica():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         return render_template('searchmusica.html')

@app.route('/abuse')
def abuse():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      return render_template('abuse.html')

@app.route('/searchmusicarres', methods=['POST', 'GET'])
def searchmusicares():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if request.method == 'POST':
         global search
         search = request.form['search']
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row
         search = "*" + search + "*"
         cur = con.cursor()
         cur.execute("SELECT ID, TITLE, ALBUM, ARTIST, categorie, PATH FROM music WHERE (upper(TITLE) GLOB upper(?)) OR (upper(ARTIST) GLOB upper(?)) OR (upper(categorie) GLOB upper(?)) OR (ID GLOB ?);", (search, search, search, search))
         rows = cur.fetchall();
         return render_template("musiclist.html", rows=rows)

@app.route('/searchmusicarresasc')
def searchmusicaresasc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      global search
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT ID, TITLE, ALBUM, ARTIST, categorie, PATH FROM music WHERE (upper(TITLE) GLOB upper(?)) OR (upper(ARTIST) GLOB upper(?)) OR (upper(categorie) GLOB upper(?)) OR (ID GLOB ?) ORDER BY ID DESC;", (search, search, search, search))
      rows = cur.fetchall();
      return render_template("musiclist.html", rows=rows)

@app.route('/searchmusicarresdesc')
def searchmusicaresdesc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      global search
      con = sql.connect("static/bot.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT ID, TITLE, ALBUM, ARTIST, PATH FROM music WHERE (upper(TITLE) GLOB upper(?)) OR (upper(ARTIST) GLOB upper(?)) OR (upper(categorie) GLOB upper(?)) OR (ID GLOB ?) ORDER BY ID ASC;", (search, search, search, search))
      rows = cur.fetchall();
      return render_template("musiclist.html", rows=rows)

@app.route('/searchbookres',methods = ['POST', 'GET'])
def bookre():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if request.method == 'POST':
         global searchbook
         searchbook = request.form['search']
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row
         searchbook = "*" + searchbook + "*"
         cur = con.cursor()
         cur.execute("SELECT ID, TITLE, AUTHOR, YEAR, LANGUAGE FROM books WHERE (upper(TITLE) GLOB upper(?) OR (upper(AUTHOR) GLOB upper(?)) OR (upper(YEAR) GLOB upper(?)));", (searchbook, searchbook, searchbook))

         rows = cur.fetchall();
         return render_template("booklist.html",rows = rows)

@app.route('/searchbook')
def searchbook():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         return render_template('searchbook.html')

@app.route('/setmusiccat')
def searchmusiccat():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      return render_template('setmusiccat.html')

@app.route('/setmusiccatres',methods = ['POST', 'GET'])
def musicrec():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      if request.method == 'POST':
         artist = str(request.form['artist'])
         categorie = str(request.form['categorie'])
         con = sql.connect("static/bot.db")
         stmnt = "UPDATE music SET categorie = '" + categorie + "' where upper(ARTIST) GLOB upper('" + artist + "');"
         with con:
            cur = con.cursor()
            cur.execute(stmnt)
         con.commit()
         con.close()
         return render_template("setmusiccatfinal.html")

@app.route('/setseriescat')
def setseriescat():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      return render_template('setmoviecat.html')


@app.route('/setseriescatres', methods=['POST', 'GET'])
def seriecatres():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      if request.method == 'POST':
         mvid = str(request.form['ID'])
         mvname = str(request.form['NAME'])
         mvgenre = str(request.form['GENRE'])
         mvseries = str(request.form['SERIES'])
         con = sql.connect("static/vid.db")
         stmnt = "UPDATE mp4 SET name = '" + mvname + "', series = '" + mvseries + "', genre = '" + mvgenre + "' where ID = '" + mvid + "';"
         with con:
            cur = con.cursor()
            cur.execute(stmnt)
         con.commit()
         con.close()
         return render_template("setserfinal.html")


@app.route('/createuser')
def userc():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      return render_template('createuser.html')

@app.route('/createuserres',methods = ['POST', 'GET'])
def userec():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      if request.method == 'POST':
         username = str(request.form['username'])
         password = str(request.form['password'])
         con = sql.connect("userlog.db")
         stmnt = 'insert into users (id, username, password) VALUES (NULL, "' + username + '", "' + password + '");'
         with con:
            cur = con.cursor()
            cur.execute(stmnt)
         con.commit()
         con.close()
         return render_template("userfinal.html")

@app.route('/downloadmusicmass')
def massdownloadmusic():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         return render_template('downloadmusicmass.html')

@app.route('/downloadmm',methods = ['POST', 'GET'])
def massdownloadmusicresult():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if request.method == 'POST':
         ids = str(request.form['ids'])
         link = "https://telegram.me/teletransferxbot?start=music-" + ids
      return redirect(link, code=302)

@app.route('/downloadbooksmass')
def massdownloadbooks():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         return render_template('downloadbooksmass.html')

@app.route('/downloadmb',methods = ['POST', 'GET'])
def massdownloadbooksresult():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if request.method == 'POST':
         ids = str(request.form['ids'])
         link = "https://telegram.me/teletransferxbot?start=books-" + ids
      return redirect(link, code=302)

@app.route('/streamm<path>')
def my_view_func(path):
   if not session.get('premium'):
      flash("This is an Premium Feature!")
      return render_template('index.html')
   elif session.get('premium'):
      pathbuffer = path.replace("<", "")
      pathbuffer = pathbuffer.replace(">", "")
      print(pathbuffer)
      return render_template('streamm.html', value=pathbuffer)

@app.route('/searchmoviestreamres',methods = ['POST', 'GET'])
def movres():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if request.method == 'POST':
         global searchmoviestream
         searchmoviestream = request.form['search']
         con = sql.connect("static/vid.db")
         con.row_factory = sql.Row
         searchmoviestream = "*" + searchmoviestream + "*"
         cur = con.cursor()
         print(searchmoviestream)
         cur.execute("select * from mp4 where (upper(NAME) GLOB upper(?)) OR (upper(series) GLOB upper(?)) OR (upper(genre) GLOB upper(?))",(searchmoviestream, searchmoviestream, searchmoviestream))

         rows = cur.fetchall();
         return render_template("moviestreamdblist.html", rows = rows)

@app.route('/searchmoviestream')
def searchmov():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      return render_template('searchmoviestream.html')

@app.route('/searchmoviestreamasc')
def mp4asc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      global searchmoviestream
      searchmoviestream = "*" + searchmoviestream + "*"
      con = sql.connect("static/vid.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from mp4 where (upper(NAME) GLOB upper(?)) OR (upper(series) GLOB upper(?)) OR (upper(genre) GLOB upper(?)) ORDER BY id asc", (searchmoviestream, searchmoviestream, searchmoviestream))

      rows = cur.fetchall();
      return render_template("moviestreamdblist.html", rows=rows)

@app.route('/searchmoviestreamdesc')
def mp4dsc():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      global searchmoviestream
      searchmoviestream = "*" + searchmoviestream + "*"
      con = sql.connect("static/vid.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from mp4 where (upper(NAME) GLOB upper(?)) OR (upper(series) GLOB upper(?)) OR (upper(genre) GLOB upper(?)) ORDER BY id desc", (searchmoviestream, searchmoviestream, searchmoviestream))

      rows = cur.fetchall();
      return render_template("moviestreamdblist.html", rows=rows)




@app.route('/searchmoviestreamascdb')
def mp4ascdb():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      global searchmoviestream
      con = sql.connect("static/vid.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from mp4 ORDER BY id asc")

      rows = cur.fetchall();
      return render_template("moviestreamdb.html", rows=rows)

@app.route('/searchmoviestreamdescdb')
def mp4dscdb():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      global searchmoviestream
      con = sql.connect("static/vid.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from mp4 ORDER BY id desc")

      rows = cur.fetchall();
      return render_template("moviestreamdb.html", rows=rows)

@app.route('/adminlogin', methods=['POST'])
def do_admin_login():
   POST_USERNAME = str(request.form['username'])
   POST_PASSWORD = str(request.form['password'])
   con = sql.connect("user.db")
   con.row_factory = sql.Row
   stmnt = "SELECT * FROM users WHERE (username = '" + POST_USERNAME + "') AND (password = '" + POST_PASSWORD + "');"
   cur = con.cursor()
   cur.execute(stmnt)
   rows = cur.fetchall();
   if rows:
      session['admin_logged_in'] = True
      return render_template("admin.html")
   else:
      flash('wrong password!')
      return render_template("adminlogin.html")

@app.route('/admin')
def admin():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   else:
      return render_template("admin.html")


@app.route('/login', methods=['POST'])
def do_user_login():

   POST_USERNAME = str(request.form['username'])
   POST_PASSWORD = str(request.form['password'])
   POST_PASSWORD = hashlib.md5(POST_PASSWORD.encode())
   POST_PASSWORD = POST_PASSWORD.hexdigest()

   con = sql.connect("userlog.db")
   con.row_factory = sql.Row
   stmnt = "SELECT * FROM users WHERE (username = '" + POST_USERNAME + "') AND (password = '" + POST_PASSWORD + "');"
   cur = con.cursor()
   cur.execute(stmnt)
   rows = cur.fetchall();
   if rows:
      con = sql.connect("userlog.db")
      stmnt = "SELECT ACTIVE FROM users WHERE (username = '" + POST_USERNAME + "') AND (password = '" + POST_PASSWORD + "');"
      cur = con.cursor()
      cur.execute(stmnt)
      rows = cur.fetchall();
      for row in rows:
        row = row
        isactive = str(row)
        isactive = isactive.replace("(", "")
        isactive = isactive.replace(",)", "")
        print(isactive)
        isactive = int(isactive)

      if isactive < 1:
        flash("You have been banned! Shut Up!")
        return render_template("banned.html")
      elif isactive > 0:
         con = sql.connect("userlog.db")
         stmnt = "SELECT premium FROM users WHERE (username = '" + POST_USERNAME + "') AND (password = '" + POST_PASSWORD + "');"
         cur = con.cursor()
         cur.execute(stmnt)
         rows = cur.fetchall();
         for row in rows:
            row = row
            premium = str(row)
            premium = premium.replace("(", "")
            premium = premium.replace(",)", "")
            premium = premium.replace("'", "")
            premium = premium.replace("')", "")

         print(premium)
         con.close()
         global chatid
         stmnta = "SELECT userid FROM users WHERE (username = '" + POST_USERNAME + "') AND (password = '" + POST_PASSWORD + "');"
         con = sql.connect("userlog.db")
         cur = con.cursor()
         cur.execute(stmnta)
         rowc = cur.fetchall();
         for rowa in rowc:
            rowa = rowa
            chatid = str(rowa)
            chatid = chatid.replace("(", "")
            premium = chatid.replace(",)", "")
            chatid = chatid.replace("'", "")
            chatid = chatid.replace("')", "")
            chatid = chatid.replace(",)", "")

            print(chatid)
            chatid = int(chatid)
         con.close()
         if premium == 'premium':
            session['premium'] = False
            session['logged_in'] = True
            msg = "Welcome " + POST_USERNAME + "!"
            flash(msg)
            return render_template("index.html")
         else:
            session['premium'] = True
            session['logged_in'] = True
            msg = "Welcome " + POST_USERNAME + "! You are a Premium user!"
            flash(msg)
            return render_template("index.html")
      else:
        return render_template("login.html")
   else:
      flash('wrong password!')
      return render_template("login.html")

@app.route('/')
def home():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      return render_template("index.html")

@app.route("/logout")
def logout():
   session['logged_in'] = False
   session['admin_logged_in'] = False
   return home()

@app.route('/signup')
def signup():
      return render_template("signup.html")

@app.route('/signupres', methods=['POST'])
def do_user_register():
   POST_USERNAME = str(request.form['username'])
   POST_EMAIL = str(request.form['email'])
   POST_PASSWORD = str(request.form['password'])
   POST_PASSWORD_SECOND = str(request.form['passwordse'])
   POST_CHATID = int(request.form['chatid'])    
   ACTIVE = 1
   if not POST_CHATID:
      flash("Fill in CHAT-ID")
      return render_template("signup.html")
   if POST_PASSWORD == POST_PASSWORD_SECOND:
      con = sql.connect("userlog.db")
      con.row_factory = sql.Row
      stmnt = "SELECT * FROM users WHERE username = '" + POST_USERNAME + "';"
      cur = con.cursor()
      cur.execute(stmnt)
      rows = cur.fetchall();
      if not rows:
         POST_PASSWORD = hashlib.md5(POST_PASSWORD.encode())
         POST_PASSWORD = POST_PASSWORD.hexdigest()
         con = sql.connect("userlog.db")
         with con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (id, username, password, email, active, userid, premium) VALUES (NULL, ?, ?, ?, ?, ?, '0')",(POST_USERNAME, POST_PASSWORD, POST_EMAIL, ACTIVE, POST_CHATID))
            stmnt = 'CREATE TABLE "' + str(POST_CHATID) + '" ( "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "favtype"	TEXT NOT NULL, "favid"	INTEGER NOT NULL, "favname"	INTEGER NOT NULL);'
            cur.execute(stmnt)
            con.commit()
         con.close()
         return home()
      else:
         flash("Username already taken!")
         return render_template("signup.html")
   else:
      flash('Password does not match!')
      return render_template("signup.html")


@app.route('/mkfav<uri>')
def mkfav(uri):
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      global chatid
      print(uri)
      favtypes = uri
      favtypes = favtypes.replace("<","")
      favtypes = favtypes.replace(">", "")
      favtypes = favtypes[:1]
      print(favtypes)
      if favtypes == "m":
         favid = uri
         favid = favid.replace("m", "")
         favid = favid.replace(">", "")
         favid = favid.replace("<", "")
         favid = str(favid)
         print(favid)
         con = sql.connect("static/bot.db")
         with con:
            cur = con.cursor()
            stmnt = "select * from music where id = '" + favid + "';"
            cur.execute(stmnt)
            rows = cur.fetchall();
         print(rows)
         title = rows[0][2] + " " + rows[0][3]
         title = str(title)
         print(rows[title])
      return render_template("index.html")



@app.route('/userlist')
def userlist():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      con = sql.connect("userlog.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("select * from users")
      rows = cur.fetchall();
      return render_template("userlist.html",rows = rows)

@app.route('/deluser<ids>')
def deluser(ids):
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      id = ids.replace("<", "")
      id = id.replace(">", "")
      con = sql.connect("userlog.db")
      with con:
         cur = con.cursor()
         stmnt = "UPDATE users SET active = 0 WHERE id = '" + id + "';"
         cur.execute(stmnt)
      con.commit()
      con.close()
      flash("User Deleted!")
      return render_template("userlist.html")

@app.route('/banuser<ids>')
def banuser(ids):
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      id = ids.replace("<", "")
      id = id.replace(">", "")
      con = sql.connect("userlog.db")
      with con:
         stmnt = "UPDATE users SET active = 0 WHERE id = '" + id + "';"
         cur = con.cursor()
         cur.execute(stmnt)
      con.commit()
      con.close()
      flash("User Banned!")
      print(ids)
      return render_template("userlist.html")

@app.route('/unbanuser<ids>')
def unbanuser(ids):
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      id = ids.replace("<", "")
      id = id.replace(">", "")
      con = sql.connect("userlog.db")
      with con:
         stmnt = "UPDATE users SET active = 1 WHERE id = '" + id + "';"
         cur = con.cursor()
         cur.execute(stmnt)
      con.commit()
      con.close()
      flash("User unbanned!")
      return render_template("userlist.html")

@app.route('/mkpremium<ids>')
def mkpremium(ids):
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      id = ids.replace("<", "")
      id = id.replace(">", "")
      con = sql.connect("userlog.db")
      with con:
         stmnt = "UPDATE users SET premium = 'premium' WHERE id = '" + id + "';"
         cur = con.cursor()
         cur.execute(stmnt)
      con.commit()
      con.close()
      flash("User is premium!")
      print(ids)
      return render_template("userlist.html")

@app.route('/umkpremium<ids>')
def umkpremium(ids):
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      id = ids.replace("<", "")
      id = id.replace(">", "")
      con = sql.connect("userlog.db")
      with con:
         stmnt = "UPDATE users SET premium = 'nonpremium' WHERE id = '" + id + "';"
         cur = con.cursor()
         cur.execute(stmnt)
      con.commit()
      con.close()
      flash("Premium removed!")
      print(ids)
      return render_template("userlist.html")



@app.route('/delfile')
def delfile():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      return render_template('deletefile.html')

@app.route('/delfileres',methods = ['POST', 'GET'])
def delfileres():
   if request.method == 'POST':
      delid = request.form['fileid']
      con = sql.connect("static/bot.db")
      cur = con.cursor()
      stmnt = "DELETE FROM files where ID = '" + delid + "';"
      cur.execute(stmnt)
      con.commit()
      con.close()
      flash("DELETED!")
      return render_template("admin.html")

@app.route('/delstream')
def delstream():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      return render_template('delstream.html')

@app.route('/delstreamres',methods = ['POST', 'GET'])
def delstreamres():
   if request.method == 'POST':
      delid = request.form['fileid']
      con = sql.connect("static/vid.db")
      cur = con.cursor()
      stmnt = "DELETE FROM mp4 where ID = '" + delid + "';"
      cur.execute(stmnt)
      con.commit()
      con.close()
      flash("DELETED!")
      return render_template("admin.html")

@app.route('/vid<uri>')
def vidplay(uri):
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      id = uri.replace("<", "")
      id = id.replace(">", "")
      con = sql.connect("static/vid.db")
      cur = con.cursor()
      stmnt = "SELECT PATH FROM mp4 where ID = '" + id + "';"
      cur.execute(stmnt)
      rows = cur.fetchall();
      con.close()
      path = str(rows)
      path = path.replace("[('", "")
      path = path.replace("',)]", "")
      print(path)
      return render_template('vidplayer.html', value=path)

@app.route('/getpremium')
def getpremium():
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      return render_template("premium.html")

@app.route('/premiumpayres', methods=['POST'])
def do_premium_pay():
   POST_PSCCODE = str(request.form['pscpin'])
   POST_CHATID = int(request.form['chatid'])
   now = datetime.datetime.now()
   now = str(now)
   if not POST_CHATID:
      flash("Fill in CHAT-ID")
      return render_template("premium.html")
   if not POST_CHATID:
      flash("Fill in PSC Pin")
      return render_template("premium.html")
   if POST_PSCCODE and POST_CHATID:
      con = sql.connect("userlog.db")
      with con:
            cur = con.cursor()
            cur.execute("INSERT INTO premiumpay (id, date, chatid, psccode) VALUES (NULL, ?, ?, ?)",(now, POST_CHATID, POST_PSCCODE))
            con.commit()
      con.close()
      flash("Payment accepted")
      return render_template("index.html")
   else:
      flash("Unknown Error!")
      return render_template("index.html")

@app.route('/paylist')
def showpay():
   if not session.get('admin_logged_in'):
      return render_template('adminlogin.html')
   elif session.get('admin_logged_in'):
      con = sql.connect("userlog.db")
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("select * from premiumpay")
      rows = cur.fetchall();
      return render_template("showpayment.html",rows = rows)

@app.route('/vidbyseries<ids>')
def vidbyseries(ids):
   ids = str(ids)
   ids = ids.replace(">", "")
   ids = ids.replace("<", "")
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/vid.db")
         con.row_factory = sql.Row
         print(ids)
         cur = con.cursor()
         stmnt = "select * from mp4 where upper(series) GLOB  upper('*" + ids +"*');"
         cur.execute(stmnt);

         rows = cur.fetchall();
         return render_template("moviestreamdb.html", rows=rows)
@app.route('/vidbygenre<ids>')
def vidbygenre(ids):
   ids = str(ids)
   ids = ids.replace(">", "")
   ids = ids.replace("<", "")
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/vid.db")
         con.row_factory = sql.Row
         print(ids)
         cur = con.cursor()
         stmnt = "select * from mp4 where upper(genre) GLOB  upper('*" + ids +"*');"
         cur.execute(stmnt);

         rows = cur.fetchall();
         return render_template("moviestreamdb.html", rows=rows)

@app.route('/musicbyartist<ids>')
def musicbyartist(ids):
   ids = str(ids)
   ids = ids.replace(">", "")
   ids = ids.replace("<", "")
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row
         print(ids)
         cur = con.cursor()
         stmnt = "select * from music where upper(ARTIST) GLOB  upper('*" + ids +"*');"
         cur.execute(stmnt);

         rows = cur.fetchall();
         return render_template("musiclist.html", rows=rows)

@app.route('/musicbyalbum<ids>')
def musicbyalbum(ids):
   ids = str(ids)
   ids = ids.replace(">", "")
   ids = ids.replace("<", "")
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row
         print(ids)
         cur = con.cursor()
         stmnt = "select * from music where upper(ALBUM) GLOB  upper('*" + ids +"*');"
         cur.execute(stmnt);

         rows = cur.fetchall();
         return render_template("musiclist.html", rows=rows)

@app.route('/musicbyyear<ids>')
def musicbyyear(ids):
   ids = str(ids)
   ids = ids.replace(">", "")
   ids = ids.replace("<", "")
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      if not session.get('premium'):
         flash("This is an Premium Feature!")
         return render_template('index.html')
      elif session.get('premium'):
         con = sql.connect("static/bot.db")
         con.row_factory = sql.Row
         print(ids)
         cur = con.cursor()
         stmnt = "select * from music where upper(ALBUM) GLOB  upper('*" + ids +"*');"
         cur.execute(stmnt);

         rows = cur.fetchall();
         return render_template("musiclist.html", rows=rows)

@app.route('/playmusic<uri>')
def playmusic(uri):
   if not session.get('logged_in'):
      return render_template('login.html')
   elif session.get('logged_in'):
      id = uri.replace("<", "")
      id = id.replace(">", "")
      con = sql.connect("static/bot.db")
      cur = con.cursor()
      stmnt = "SELECT PATH FROM music where ID = '" + id + "';"
      cur.execute(stmnt)
      rows = cur.fetchall();
      con.close()
      path = str(rows)
      path = path.replace("[('", "")
      path = path.replace("',)]", "")
      print(path)
      return render_template('vidplayer.html', value=path)
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host='213.202.252.16', port=80, threaded=True)
