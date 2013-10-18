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
    '/latte', 'Latte',
    '/blog', 'Blog',
    '/blog/(\d+)', 'View',
    '/blog/new', 'New',
    '/blog/delete/(\d+)', 'Delete',
    '/blog/edit/(\d+)', 'Edit',
)


### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', globals=t_globals)
app = web.application(urls, globals())

### Authentication 
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0})

        
class Login:

    def GET(self):
        if user.logged(session):
            render = user.create_render(session)
            raise web.seeother('/latte')
        else:
            render = user.create_render(session)
            return '%s' % render.login()

    def POST(self):
        username, passwd = web.input().user, web.input().passwd
        ident = blog.db.select('users', where='user=$username', vars=locals())[0]
        if hashlib.sha1(ident['salt']+passwd).hexdigest() == ident['pass']:
            session.login = 1
            session.privilege = ident['privilege']
            render = user.create_render(session)
            raise web.seeother('/latte')
        else:
            session.login = 0
            session.privilege = 0
            render = user.create_render(session)
            return render.login_error()

class Latte:
    
    def GET(self):
        if user.logged(session):
            published_posts = blog.get_published_posts()
            unpublished_posts = blog.get_unpublished_posts()
            render = user.create_render(session)
            return render.latte(published_posts, unpublished_posts)
        else:
            raise web.seeother('/login')

class Logout:

    def GET(self):
        session.login = 0
        session.kill()
        render = user.create_render(session.privilege)
        return render.index()


class Index:
    
    def GET(self):
        return render.index()


class Blog:

    def GET(self):
        """ Show page """
        posts = blog.get_published_posts()
        return render.blog(posts)


class View:

    def GET(self, id):
        """ View single post """
        post = blog.get_post(int(id))
        return render.view(post)


class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            size=30,
            description="Post title:"),
        web.form.Textarea('content', web.form.notnull, 
            rows=30, cols=80,
            description="Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        blog.new_post(form.d.title, form.d.content)
        raise web.seeother('/blog')


class Delete:

    def POST(self, id):
        blog.del_post(int(id))
        raise web.seeother('/blog')


class Edit:

    def GET(self, id):
        post = blog.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = New.form()
        post = blog.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        blog.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/blog')

if __name__ == '__main__':
    app.run()