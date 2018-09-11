#!flask/bin/python
import os
import unittest

from app import create_app, db
from app.auth.models import User, Post 
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        print("""test avatar""")
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(128)
        excepted = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(excepted)] == excepted

    def test_make_unique_nickname(self):
        print("""test make unique nickname""")
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        unique_nickname = User.make_unique_nickname('john1')
        assert unique_nickname == True

        unique_nickname = User.make_unique_nickname('john')
        assert unique_nickname == False

    def test_follow(self):
        u1 = User(nickname='john', email='john@example.com')
        u2 = User(nickname='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) == None

        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.is_following(u2)
        assert u1.followed_users.count() == 1
        assert u1.followed_users.first().nickname == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'john'

        u = u1.unfollow(u2)
        assert u is u1
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed_users.count() == 0
        assert u2.followers.count() == 0

    def test_follow_post(self):
        u1 = User(nickname='john', email='john@example.com')
        u2 = User(nickname='susan', email='susan@example.com')
        u3 = User(nickname='wjh', email='wjh@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        import datetime
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p1 = Post(body='post from john', author=u1, timestamp=nowtime)
        p2 = Post(body='post from susan', author=u2, timestamp=nowtime)
        p3 = Post(body='post from wjh', author=u3, timestamp=nowtime)
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()

        f1 = u1.follow(u2)
        f2 = u1.follow(u3)
        f3 = u2.follow(u1)
        f4 = u2.follow(u3)
        f5 = u3.follow(u1)
        f6 = u3.follow(u2)
        
        db.session.add(f1)
        db.session.add(f2)
        db.session.add(f3)
        db.session.add(f4)
        db.session.add(f5)
        db.session.add(f6)
        db.session.commit()

        # print(u1.followers.count())
        # print(dir(u1.followed_users))
        # print(u1.followed_users.all())
        print(u1.followed_posts().all())

if __name__ == '__main__':
    unittest.main()
    # TestSuite = unittest.TestSuite() 
    # TestSuite.addTest(TestCase('test_avatar'))
    # TestSuite.addTest(TestCase('test_make_unique_nickname'))
    # runner = unittest.TextTestRunner()
    # runner.run(TestSuite)
