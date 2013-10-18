import web, datetime

db = web.database(dbn='mysql', db='blog', user='admin', pw='andre')

def get_posts():
    return db.select('entries', order='id DESC')

def get_published_posts():
    return db.select('entries', where='published=1', order='id DESC')

def get_unpublished_posts():
    return db.select('entries', where='published=0', order='id DESC')

def get_post(id):
    try:
        return db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text):
    db.insert('entries', title=title, content=text, posted_on=datetime.datetime.utcnow(), published=1)

def del_post(id):
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('entries', where="id=$id", vars=locals(),
        title=title, content=text)