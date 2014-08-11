#!/usr/bin/env python

import web
import datetime
import re
import config
import random
import string
import hashlib

con = config.Config()
cache = True

def get_posts():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('entries', order='id DESC')

def get_published_posts():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('entries', where='published=1 AND trash=0', order='posted_on DESC')

def get_unpublished_posts():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('entries', where='published=0 AND trash=0', order='posted_on DESC')

def get_trashed_posts():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('entries', where='trash=1', order='id DESC')

def throw_away(id):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(), trash=1)

def empty_trash():
    posts = get_trashed_posts()
    for post in posts:
        del_post(post.id)

def put_back(id):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(), trash=0)

def get_post(id):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    try:
        return db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, published):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    dt = datetime.datetime.utcnow()
    return db.insert('entries', title=re.sub('<[^<]+?>', '', title), markdown=" ", html=" ", posted_on=dt, published=published)

def del_post(id):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, md, mu, published):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    dt = datetime.datetime.utcnow()
    if published == 1 and get_post(id).published == 0:
        db.update('entries', where="id=$id", vars=locals(),
            title=re.sub('<[^<]+?>', '', title), markdown=md, html=mu, posted_on=dt, published=published)
    else:
        db.update('entries', where="id=$id", vars=locals(),
            title=re.sub('<[^<]+?>', '', title), markdown=md, html=mu, published=published)

def update_thumb_for_post(id, url):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(), thumb_url=url)

def update_post_body(id, md, mu):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(), markdown=md, html=mu)

def update_post_title(id, title):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(), title=re.sub('<[^<]+?>', '', title))

def generateUser(username, password, email):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    slt = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
    pswd = hashlib.sha1(slt+password).hexdigest()
    return db.insert('users', user=username, passwd=pswd, email=email, privilege=2, salt=slt)

def get_user():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('users', where='id=1', vars=locals())

def update_user(username, password, email):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('users', where="id=1", vars=locals(), user=username, passwd=password, email=email)
