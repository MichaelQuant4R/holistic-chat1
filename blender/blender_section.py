from flask import (Blueprint, render_template, redirect, url_for, request, jsonify, flash)
from flask_login import (current_user, login_required)
from models import (db, app, socketio, User, Chat, Join, Leave)
import time

app_mod = Blueprint("blender_section", __name__, template_folder = "templates_model")


@app_mod.route("/models", methods = ["GET", "POST"])
def models_page():
    
    
    return render_template("models.html", title = "models")




