""" Basic blog using webpy 0.3 """
import web
import blog
import user
import hashlib

### Url mappings

web.config.debug = False

urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', "Logout",
    '/work', 'Work',
    '/americano', 'Americano',
    '/blog', 'Blog',
    '/blog/(\d+)', 'BlogPost',
    '/blog/new', 'New',
    '/blog/delete/(\d+)', 'Delete',
    '/blog/edit/(\d+)', 'Edit',
    '/jarvis', "Jarvis"
)


app = web.application(urls, globals())

### Authentication 
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0})


### Templates
t_globals = {
    'datestr': web.datestr,
}
render = web.template.render('templates/common', cache=blog.cache, globals=t_globals)

def gen_head():
    if session.login==1:
        if session.privilege == 2:
            render = web.template.render('templates/admin', globals=t_globals)
            return render.header()
        else:
            render = web.template.render('templates/common', globals=t_globals)
            return render.header()
    else:
        render = web.template.render('templates/common', globals=t_globals)
        return render.header()

def gen_offleft():
    if session.login==1:
        if session.privilege == 2:
            render = web.template.render('templates/admin', globals=t_globals)
            return render.offleft()
        else:
            render = web.template.render('templates/common', globals=t_globals)
            return render.offleft()
    else:
        render = web.template.render('templates/common', globals=t_globals)
        return render.offleft()

class Login:

    def GET(self):
        if user.logged(session):
            render = user.create_render(session)
            raise web.seeother('/americano')
        else:
            render = user.create_render(session)
            return '%s' % render.login(gen_head(), gen_offleft())

    def POST(self):
        username, passwd = web.input().user, web.input().passwd
        ident = blog.db.select('users', where='user=$username', vars=locals())[0]
        if hashlib.sha1(ident['salt']+passwd).hexdigest() == ident['pass']:
            session.login = 1
            session.privilege = ident['privilege']
            render = user.create_render(session)
            raise web.seeother('/americano')
        else:
            session.login = 0
            session.privilege = 0
            render = user.create_render(session)
            return render.login_error()

class Americano:
    
    def GET(self):
        if user.logged(session):
            published_posts = blog.get_published_posts()
            unpublished_posts = blog.get_unpublished_posts()
            render = user.create_render(session)
            return render.americano(gen_head(), gen_offleft(), published_posts, unpublished_posts)
        else:
            raise web.seeother('/login')

class Logout:

    def GET(self):
        session.login = 0
        session.kill()
        raise web.seeother('/blog')


class Index:
    
    def GET(self):
        render = web.template.render('templates/common', globals=t_globals)
        return render.index(gen_head(), gen_offleft())


class Blog:

    def GET(self):
        """ Show page """
        posts = blog.get_published_posts()
        render = web.template.render('templates/common', globals=t_globals)
        return render.blog(gen_head(), gen_offleft(), posts)


class BlogPost:

    def GET(self, id):
        """ View single post """
        post = blog.get_post(int(id))
        render = web.template.render('templates/common', globals=t_globals)
        return render.blogpost(gen_head(), gen_offleft(), post)


class New:

    def GET(self):
        render = user.create_render(session)
        return render.new(gen_head(), gen_offleft())

    def POST(self):
        title, body, published = web.input().title, web.input().body, int(web.input().published)
        if user.logged(session):
            if session.privilege == 2:
                if title == "" or body == "":
                    render = user.create_render(session)
                    return render.new(gen_head(), gen_offleft())
                blog.new_post(title, body, published)
        if published == 1:
            raise web.seeother('/blog')
        else:
            raise web.seeother('/americano')


class Delete:

    def POST(self, id):
        if user.logged(session):
            if session.privilege == 2:
                blog.del_post(int(id))
        raise web.seeother('/americano')

class Work:

    def GET(self):
        render = web.template.render('templates/common', globals=t_globals)
        return render.work(gen_head(), gen_offleft())


class Edit:

    def GET(self, id):
        post = blog.get_post(int(id))
        if post is None:
            post_id = blog.new_post("title", "<p>body</p>", 0)
            post = blog.get_post(post_id)
            print post_id
            raise web.seeother("/blog/edit/"+str(post_id))
        render = user.create_render(session)
        return render.edit(gen_head(), gen_offleft(), post)


    def POST(self, id):
        title, body, published = web.input().title, web.input().body, int(web.input().published)
        if user.logged(session):
            if session.privilege == 2:
                post = blog.get_post(int(id))
                if title == "" or body == "":
                    render = user.create_render(session)
                    return render.edit(gen_head(), gen_offleft(), post)
                blog.update_post(int(id), title, body, published)
        if published == 1:
            raise web.seeother('/blog')
        else:
            raise web.seeother('/americano')

if __name__ == '__main__':
    app.run()