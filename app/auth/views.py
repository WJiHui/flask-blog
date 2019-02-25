from datetime import datetime
from flask_babel import get_locale
from guess_language import guess_language 
from flask_login import login_user, logout_user, current_user, login_required
from flask import flash, redirect, session, url_for, request, g, render_template, current_app

from .models import User, Post, RequestInfo
from .emails import follower_notification 
from .form import LoginForm, RegisterForm, PostForm, SearchForm

from app.auth import bp 
from app import lm,db

@bp.before_request 
def get_user_info():
        request_info = RequestInfo(
            agent = str(request.user_agent),
            ip = str(request.remote_addr),
            cookie = str(request.cookies)
        )
        db.session.add(request_info)
        db.session.commit()


@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/index/<int:page>',methods=['GET', 'POST'])
@login_required 
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        now_time = datetime.utcnow()
        language = guess_language(form.post.data)
        if language == 'UNKNOW' or len(language)  > 5:
            language = ''
        post = Post(body=form.post.data, timestamp=now_time, author=g.user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        return redirect(url_for('auth.index'))
    user = g.user
    posts = user.followed_posts().paginate(page,
                                           current_app.config['POSTS_AVG_PAGE'], False)
    return render_template('index.html', title='Home', user=user, posts=posts, form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user_name = form.user.data
        user = User.query.filter_by(nickname=user_name).first()
        if user is None:
            form.user.errors.append("The user isn't registered yet")
        else:
            login_user(user, remember=session['remember_me'])
            return redirect(request.args.get('next') or url_for('auth.index'))
    return render_template('login.html', title='sign in', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('auth.index'))
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
                return redirect(request.args.get('next') or
                                url_for('auth.index'))
            else:
                register_form.email.errors.append('This email has been register')
        else:
            register_form.nickname.errors.append('This user has been register')
    return render_template('register.html', title='register', form=register_form)


@bp.before_app_request 
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        # g.user.last_seen = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@bp.route('/user/<nickname>')
@bp.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('auth.index'))
    posts = user.posts.paginate(page, current_app.config['POSTS_AVG_PAGE'], False)
    return render_template('user.html', user=user, posts=posts)

from .form import LoginForm, EditForm
from flask_babel import _
@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(_('Your changes has been saved.'))
        return redirect(url_for('auth.user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('edit.html', form=form)

@bp.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('auth.index'))
    if user == g.user:
        flash('You can not follow yourself.')
        return redirect(url_for('auth.index'), nickname=nickname)
    u = g.user.follow(user)
    if u is None:
        flash("Cannot follow %s." % nickname)
        return redirect(url_for('auth.user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following %s.' % nickname)
    follower_notification(user, g.user)
    return redirect(url_for('auth.user', nickname=nickname))

@bp.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('auth.index'))
    if user == g.user:
        flash("You can't unfollow youself.")
        return redirect(url_for('auth.user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash("Can't unfollow %s." % nickname)
        return redirect(url_for('auth.user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped unfollowing %s.' % nickname)
    return redirect(url_for('auth.user', nickname=nickname))


@bp.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('auth.index'))
    return redirect(url_for('auth.search_results', query=g.search_form.search.data))


@bp.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query,
                                       limit=current_app.config['MAX_SEARCH_RESULTS']).all()
    return render_template('search_results.html', query=query, results=results)
