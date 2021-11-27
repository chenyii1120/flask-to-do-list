from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from form import CreateMission
from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# CONNECT TO DB
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(250), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    done_date = db.Column(db.DateTime)


db.create_all()

# localize the time
def get_time():
    now = datetime.datetime.now()
    tw = pytz.timezone("Asia/Taipei")
    tw_now = tw.localize(now)
    return tw_now


@app.route('/', methods=["GET", "POST"])
def home():
    form = CreateMission()
    undone_list = Mission.query.filter_by(done=False).all()
    done_list = Mission.query.filter_by(done=True).all()

    if form.validate_on_submit() and form.content.data != "":
        new = Mission(
            content=form.content.data,
            create_date=get_time(),
            done=False
        )
        db.session.add(new)
        db.session.commit()
        return redirect("/")
    return render_template("index.html", form=form, undone=undone_list, done=done_list)


@app.route("/check/<int:mission_id>")
def check(mission_id):
    target = Mission.query.get(mission_id)
    target.done = True
    target.done_date = get_time()
    db.session.commit()
    return redirect("/")


@app.route("/uncheck/<int:mission_id>")
def uncheck(mission_id):
    target = Mission.query.get(mission_id)
    target.done = False
    target.done_date = get_time()
    db.session.commit()
    return redirect("/")


@app.route("/edit/<int:mission_id>", methods=["POST"])
def edit(mission_id):
    target = Mission.query.get(mission_id)
    target.content = request.values[f'mission-{mission_id}']
    db.session.commit()
    return redirect("/")


@app.route("/delete/<int:mission_id>")
def delete(mission_id):
    target = Mission.query.get(mission_id)
    db.session.delete(target)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
