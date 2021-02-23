# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
  projeto=db.projeto(db.projeto.id==request.args(0, cast=int))
  empresa=db.empresa(projeto.empresa)
  rows = db((db.vendedor.projeto==projeto.id)).select(orderby=db.vendedor.id)
  return locals()

@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    request.function='Cadastrar Vendedor'
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    projeto = db.projeto(request.args(0, cast=int))
    db.vendedor.empresa.default=usuario.empresa
    db.vendedor.projeto.default=projeto.id
    db.vendedor.projeto.writable=False
    db.vendedor.projeto.readable=False
    db.vendedor.empresa.writable=False
    db.vendedor.empresa.readable=False
    if not usuario:
        redirect(URL('default','index'))
    form = SQLFORM(db.vendedor).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index', args=projeto.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)
