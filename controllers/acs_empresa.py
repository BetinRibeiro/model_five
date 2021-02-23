# -*- coding: utf-8 -*-
import datetime
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('acs_empresa','cadastrar'))
    empresa = db.empresa(usuario.empresa)
    return locals()

@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    a=db.empresa.insert(razaosocial=auth.user.first_name,nomefantasia=auth.user.first_name)
    db.usuario_empresa.insert(empresa=a,usuario=auth.user.id, nome=auth.user.first_name, tipo="Proprietário")
    redirect(URL('index'))
    return locals()

@auth.requires_login()
def alterar():
    response.view = 'generic.html' # use a generic view
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario_empresa.empresa)
    db.empresa.id.writable=False
    db.empresa.id.readable=False
    form = SQLFORM(db.empresa, empresa.id, deletable=False)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
