#!/usr/bin/env python

import web
import blogutils

t_globals = {
    'datestr': web.datestr,
    'url' : blogutils.title_to_url
}

def logged(session):
    if session.login==1:
        return True
    else:
        return False

def create_render(session):
    if logged(session):
        if session.privilege == 0:
            render = web.template.render('templates/reader', globals=t_globals)
        elif session.privilege == 1:
            render = web.template.render('templates/user', globals=t_globals)
        elif session.privilege == 2:
            render = web.template.render('templates/admin', globals=t_globals)
        else:
            render = web.template.render('templates/common', globals=t_globals)
    else:
        render = web.template.render('templates/common', globals=t_globals)
    return render