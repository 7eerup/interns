from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 모델 정의
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)  # 완료 여부 추가

# 데이터베이스 초기화
with app.app_context():
    db.create_all()

# 메인 페이지 (To-Do 목록)
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# 새로운 Task 추가
@app.route('/add', methods=['POST'])
def add_task():
    content = request.form.get('content')
    if content:
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

# Task 삭제
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

# 완료 상태 토글
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed  # 완료 상태 변경
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)