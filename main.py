from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User
from forms.user import LoginForm, RegisterForm
from forms.job import JobsForm
from data.jobs import Jobs

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ivan_secret_key'
db_session.global_init('data.db')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_check.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template('jobs.html', title='Работа', jobs=jobs)


@app.route('/jobs_add', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.title.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/jobs')
    return render_template('jobs_add.html', title='Добавление новости', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
