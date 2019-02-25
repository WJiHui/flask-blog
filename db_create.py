#!flask/bin/python
import os 
from migrate.versioning import api
from config import Config
from app import db, create_app 
app = create_app()


SQLALCHEMY_DATABASE_URI  = Config.SQLALCHEMY_DATABASE_URI 
SQLALCHEMY_MIGRATE_REPO = Config.SQLALCHEMY_MIGRATE_REPO 
with app.app_context():
    db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))


