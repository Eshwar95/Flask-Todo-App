from flask import Flask, render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#linking to sql lite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_contents = request.form['content']
        new_task = Todo(content = task_contents)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was an issue adding the task. Contact Support! '
    else:
        list_tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = list_tasks)


@app.route('/delete/<int:id>')
def delete(id):
    tasks_to_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(tasks_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was an error in deleting the task that was previously created'


@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):

    task= Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'unable to update and redrirect to the index page'
    
    else:
        return render_template('update.html',task = task)





if __name__ =="__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)
