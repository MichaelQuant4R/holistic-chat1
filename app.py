from flask import (render_template, redirect, url_for,
                   flash, request, jsonify)

### LOCAL IMPORTS ####
from models import (db, app, socketio, User, Chat)
from forms import (RegisterForm, LoginForm, ChatRoomForm)
from chats.chat_section import app_chat
from blender.blender_section import app_mod

from flask_login import (LoginManager, login_required, login_user,
                         logout_user, current_user)

from flask_socketio import (emit, send, join_room, leave_room,
                            disconnect)

from datetime import datetime as dt
import functools
from config import rooms_dict

app.register_blueprint(app_chat)
app.register_blueprint(app_mod)


login_manager = LoginManager(app)
login_manager.login_view = "login"




users = {}

@login_manager.user_loader
def load_user(user_id):
    
    return User.query.get(int(user_id))



@app.route("/", methods = ["GET", "POST"])
@app.route("/home", methods = ["GET", "POST"])
def home():
    
    print("USERS")
    print(users)
    
    
    
        


    
    return render_template("home.html", title = "home", 
                           
                           rooms_dict = rooms_dict)


@app.route("/register", methods = ["GET", "POST"])
def register():
    
    
    if current_user.is_authenticated:
        
        flash("You're already logged in", "info")
        return redirect(url_for("profile", user_id = current_user.id, username = current_user.username))
    
    form = RegisterForm()
    
    ### True or False, if True, data will be saved
    if form.validate_on_submit():
        
        
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        check_user = User.query.filter_by(email = email).first()
        
        if check_user is None:
            
            
            user = User(username,email, password, confirm_password)
            db.session.add(user)
            db.session.commit()
            flash("Welcome! Thanks for registering!", "success")
            return redirect(url_for("login"))
        
        else:
            flash("This email is already registered!", "danger")
            return render_template("register.html", title = "register", 
                           form = form)

        
        
    
    return render_template("register.html", title = "register", 
                           form = form)



@app.route("/login", methods = ["GET", "POST"])
def login():
    
    if current_user.is_authenticated:

        flash("You're already logged in", "info")
        return redirect(url_for("profile", user_id = current_user.id, username = current_user.username))

    form = LoginForm()
    
    ### True or False, if True, data will be saved
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email = email).first()
        
        if user is not None:
            
            
            if user.checking_password(password):
            
                user.logged_in()
                login_user(user)
                
                flash("You've successfully logged in!", "success")
                return redirect(url_for("profile", user_id = user.id, username = user.username))
            
            else:
                
                flash("Incorrect email and/or password!", "danger")
                return render_template("login.html", title = "login", 
                           form = form)
                
        
        else:
            
            flash("Incorrect email and/or password!", "danger")
            return render_template("login.html", title = "login", 
                           form = form)

        
        
    
    return render_template("login.html", title = "login", 
                           form = form)


################ HANDLE CUSTOM ERRORS #############################

@app.errorhandler(404)
def not_found(e):
    
    return render_template("not_found.html", title = "not found"), 404


@app.errorhandler(403)
def forbidden(e):
    
    return render_template("forbidden.html", title = "forbidden"), 403


@app.errorhandler(500)
def internal_server_error(e):
    
    return render_template("internal_server_error.html", title = "internal_server_error"), 500


##############################################################




@app.route("/bubble1")
def bubble1():
    
    random_text = ["Add a unique username!", "a password you'll remember!", "make sure the passwords match!",
                  "username must be 3-25 characters long", "make sure your email is valid"]
    
    return render_template("bubble1.html", title = "bubble 1",
                           random_text = random_text)

@app.route("/bubble2")
def bubble2():
    
    return render_template("bubble2.html", title = "bubble 2")


@app.route("/bubble3")
def bubble3():
    random_text = ["Add a unique username!", "a password you'll remember!", "make sure the passwords match!",
                  "username must be 3-25 characters long", "make sure your email is valid"]
    
    return render_template("bubble3.html", title = "bubble 3",
                           random_text = random_text)





@app.route("/logout")
@login_required
def logout():
    
#     disconnect()
    current_user.logged_out()
    logout_user()
    flash("You've logged out", "info")
    return redirect(url_for("home"))


@app.route("/profile/<int:user_id>/<string:username>")
@login_required
def profile(user_id, username):
    
    
    user = User.query.filter_by(id = user_id).first()
    
    
    if user is None:
        
        
        flash("This user does not exist!", "info")
        return redirect(url_for("home"))
    
    
    
    
    return render_template("profile.html", title = "profile",
                           user = user)



@app.route("/test")
def test():
    
    return render_template("test.html", title = "test")















if __name__ == "__main__":
#     socketio.run(app, debug = False)
    app.run(debug = False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    