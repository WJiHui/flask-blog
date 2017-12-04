from flask import render_template
from flask import flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm  
from .models import User, Post 
from .form import LoginForm, RegisterForm, PostForm, SearchForm
from datetime import datetime
from config import POSTS_AVG_PAGE, MAX_SEARCH_RESULTS
from .emails import follower_notification 
from app import babel
from config import LANGUAGES
from flask_babel import gettext


@app.route('/', methods=['GET', "POST"])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>',methods=['GET', 'POST'])
@login_required 
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        now_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        post = Post(body=form.post.data, timestamp=now_time, author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        return redirect(url_for('index'))
    user = g.user
    posts = user.followed_posts().paginate(page, POSTS_AVG_PAGE, False)
    return render_template('index.html', title='Home', user=user, posts=posts, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user_name = form.user.data
        user = User.query.filter_by(nickname=user_name).first()
        if user is None:
            form.user.errors.append("The user isn't registered yet")
        else:
            login_user(user, remember=session['remember_me'])
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title='sign in', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        nickname = register_form.nickname.data 
        email = register_form.email.data 
        user_unique = User.make_unique_nickname(nickname)
        if user_unique:
            email_unique = User.make_unique_emali(email)
            if email_unique:
                about_me = register_form.about_me.data
                newuser = User(nickname=nickname, email=email, about_me=about_me)
                db.session.add(newuser)
                db.session.add(newuser.follow(newuser))
                db.session.commit()
                login_user(newuser)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                register_form.email.errors.append('This email has been register')
        else:
            register_form.nickname.errors.append('This user has been register')
    return render_template('register.html', title='register', form=register_form)


@app.before_request 
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_AVG_PAGE, False)
    return render_template('user.html', user=user, posts=posts)

from .form import LoginForm, EditForm
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes has been saved.'))
        return redirect(url_for('user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('edit.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    print('404')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can not follow yourself.')
        return redirect(url_for('index'), nickname=nickname)
    u = g.user.follow(user)
    if u is None:
        flash("Cannot follow %s." % nickname)
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following %s.' % nickname)
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash("You can't unfollow youself.")
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash("Can't unfollow %s." % nickname)
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped unfollowing %s.' % nickname)
    return redirect(url_for('user', nickname=nickname))


@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, results=results)


@babel.localeselector
def get_locale():
    return request.accecpt_languages.best_match(LANGUAGES.keys())


