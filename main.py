from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
from form import CreateMission
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd04daf94f0fc0f6cbe6095797c18dc2c03d089fa'
Bootstrap(app)

# CONNECT TO DB
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(250), nullable=False)
    creat_date = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    done_date = db.Column(db.DateTime)


db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    form = CreateMission()
    undone_list = Mission.query.filter_by(done=False).all()
    done_list = Mission.query.filter_by(done=True).all()
    if form.validate_on_submit():
        now = datetime.datetime.now()
        new = Mission(
            content=form.content.data,
            creat_date=now,
            done=False
        )
        db.session.add(new)
        db.session.commit()
        return redirect("/")
    return render_template("index.html", form=form, undone=undone_list, done=done_list)


if __name__ == "__main__":
    app.run(debug=True)
