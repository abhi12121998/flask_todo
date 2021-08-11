
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from jinja2 import Template
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class ToDo(db.Model):
    SNo = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable= False)
    date = db.Column(db.DateTime, default= datetime.utcnow)


    def __repr__(self):
        return f"{self.SNo} - {self.task}"




@app.route("/", methods= ["GET" , "POST"])
def hello_world():
    if request.method == "POST":
        task = request.form['task']
        desc = request.form['desc']
        todo = ToDo(task= task, desc= desc)
        db.session.add(todo)
        db.session.commit()
    todo = ToDo.query.all()
    #print(todo)
    return render_template("index.html", todo=todo)
    #return "<p>Hello, World!</p>"

@app.route("/show")
def show():
    todo = ToDo.query.all()
    print(todo)
    return "first blog of mine"

@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = ToDo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:SNo>", methods= ["GET" , "POST"])
def update(SNo):
    if request.method == "POST":
        task =request.form['task']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(SNo=SNo).first()
        todo.task = task
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = ToDo.query.filter_by(SNo=SNo).first()
    print(todo)
    return render_template("update.html", todo=todo)
if __name__ == "__main__":
    app.run(debug=True, port=8000)