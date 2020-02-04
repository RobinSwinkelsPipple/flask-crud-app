import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "rulesdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Rule(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route('/', methods=["GET", "POST"])
def home():
    rules = None
    if request.form:
        try:
            rule = Rule(title=request.form.get("title"))
            db.session.add(rule)
            db.session.commit()
        except Exception as e:
            print("Failed to add rule")
            print(e)
    rules = Rule.query.all()
    return render_template("home.html", rules=rules)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        rule = Rule.query.filter_by(title=oldtitle).first()
        rule.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update rule title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    rule = Rule.query.filter_by(title=title).first()
    db.session.delete(rule)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    # from rulemanager import db
    db.create_all()
    # exit()
    app.run(debug=True)