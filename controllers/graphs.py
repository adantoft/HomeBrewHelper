# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello!")
    return dict(message=T('Welcome to the graphs controller'))

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def line():

    dataURL = request.vars.dataset
    settings = request.vars.settings or ''

    if True:
        return dict(dataURL=dataURL, settings=settings)
    else:
        return dict()

def liquidGauge():

    dataURL = request.vars.dataset
    settings = request.vars.settings or ''

    if True:
        return dict(dataURL=dataURL, settings=settings)
    else:
        return dict()