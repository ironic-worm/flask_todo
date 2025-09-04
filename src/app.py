from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:0000@localhost:5432/postgres"
)
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_done = db.Column(db.Boolean, nullable=False, default=False)


@app.route("/")
def index():
    return render_template("base.html", tasks=Task.query.order_by(Task.id).all())


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("task")
    details = request.form.get("details")
    db.session.add(Task(text=text, details=details if details else None))
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear():
    Task.query.delete()
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/done/<int:task_id>", methods=["POST"])
def done(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = True
    task.completed_at = datetime.utcnow()
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/reopen/<int:task_id>", methods=["POST"])
def reopen(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = False
    task.completed_at = None
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
