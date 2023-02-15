from secrets import token_urlsafe

from api_sqlite.db import models


def add_login_details(session, db, model):
    all_users = model.User()
    all_users.username = session.cookies['username']
    all_users.user = session.cookies['user']
    all_users.branch = session.cookies['branch']
    all_users.token = session.cookies['token']
    all_users.logged_in = True
    all_users.user_id = token_urlsafe(16)
    db.add(all_users)
    db.commit()


def update_login_details(session, db, db_user):
    db_user.user = session.cookies['user']
    db_user.token = session.cookies['token']
    db_user.logged_in = True
    db.commit()
    db.refresh(db_user)


def update_session(db, userid):
    db_user = db.query(models.User).filter(models.User.user_id == userid).first()
    cookies = {
        'username': db_user.username,
        'user': db_user.user,
        'branch': db_user.branch,
        'token': db_user.token,
        'displayBuildit': 'neat',
    }
    return cookies
