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
    return dict(message=T('Welcome to HomebrewHelper!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


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


def addBrew():
    # add a new beer
    form = SQLFORM(db.brews).process()

    if form.accepted:
        response.flash = 'Update complete'

    elif form.errors:
        response.flash = 'Please enter valid details'

    recs = db(db.brews).select()  # .created_by==auth.user.id
    return dict(form=form, recs=recs)


def fermentationMonitor():
    # tracks fermentation temps
    form = SQLFORM(db.fermtemp,
                   labels={'brewname': 'Select homebrew to update', 'readingdate': 'Date and time of reading',
                           'brewtemp': 'Temp'}).process()

    recs = ""
    brewtoview = ""

    if form.accepted:
        brewtoview = form.vars.brewname
        response.flash = brewtoview + ' Update Complete!'
        recs = db(db.fermtemp.brewname == brewtoview).select(orderby=db.fermtemp.readingdate)
    elif form.errors:
        response.flash = 'Please enter valid details'

    brewviewform = SQLFORM(db.fermtemp, fields=['brewname'], labels={'brewname': 'Select homebrew to view'},
                           submit_button='View')

    if brewviewform.validate(formname='brewviewform'):
        brewtoview = brewviewform.vars.brewname
        response.flash = 'Displaying ' + brewtoview + '!'
        recs = db(db.fermtemp.brewname == brewtoview).select(
            orderby=db.fermtemp.readingdate)  # .created_by==auth.user.id
    elif brewviewform.errors:
        response.flash = 'Please enter valid details'

    return dict(form=form, brewviewform=brewviewform, recs=recs, brewtoview=brewtoview)


def fermentationMonitorData():
    # returns data in json
    brewname = request.vars.brewname
    return db(db.fermtemp.brewname == brewname).select(db.fermtemp.brewname, db.fermtemp.readingdate,
                                                       db.fermtemp.brewtemp, orderby=db.fermtemp.readingdate).as_json()


def howMuchIsLeft():
    from decimal import Decimal
    # tracks how much beer is remaining in a keg
    form = SQLFORM(db.brewremaining,
                   labels={'brewname': 'Select homebrew to update', 'readingdate': 'Date and time of reading',
                           'amount': 'Pints of brew poured'}).process()

    brewviewform = SQLFORM(db.brewremaining, fields=['brewname'], labels={'brewname': 'Select homebrew to view'},
                           submit_button='View')

    recs = ""
    brewtoview = ""
    response.flash = len(form.vars)
    brewRemaining = 0
    if form.accepted:
        brewRemaining = 124 #Pints in a full keg
        brewtoview = form.vars.brewname
        amountDrank = form.vars.amount
        response.flash = str(amountDrank) + ' pints of ' + brewtoview + ' poured!'
        recs = db(db.brewremaining.brewname == brewtoview).select(orderby=db.brewremaining.readingdate)
        rows = db(db.brewremaining.brewname == brewtoview).select(db.brewremaining.amount.sum())
        brewDrank = rows.first()[db.brewremaining.amount.sum()]
        if isinstance(brewDrank, (int, long)):
            brewRemaining -= brewDrank
    elif form.errors:
        response.flash = 'Please enter valid details'

    if brewviewform.validate(formname='brewviewform'):
        brewRemaining = 124#Pints in a full keg
        brewtoview = brewviewform.vars.brewname
        recs = db(db.brewremaining.brewname == brewtoview).select(
            orderby=db.brewremaining.readingdate)  # .created_by==auth.user.id
        rows = db(db.brewremaining.brewname == brewtoview).select(db.brewremaining.amount.sum())
        brewDrank = rows.first()[db.brewremaining.amount.sum()]
        if isinstance(brewDrank, (int, long)):
            brewRemaining -= brewDrank
        response.flash = 'Displaying ' + brewtoview + '!'
    elif brewviewform.errors:
        response.flash = 'Please enter valid details'

    return dict(form=form, brewviewform=brewviewform, recs=recs, brewtoview=brewtoview, brewRemaining=brewRemaining)
