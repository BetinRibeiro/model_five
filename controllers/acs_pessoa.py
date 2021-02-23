# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    paginacao = 35
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        redirect(URL(args=1))
    total = db((db.pessoa.empresa==empresa.id)).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.pessoa.empresa==empresa.id)).select(
      limitby=limites,orderby=db.pessoa.id
      )
    consul=(request.args(1))
    if (consul):
        registros = db((db.pessoa.empresa==empresa.id)&((db.pessoa.nome.contains(consul)))).select(limitby=(0,paginacao))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, usuario=usuario, consul=consul)

@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    request.function='Cadastrar Contratado'
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    db.pessoa.empresa.default=usuario.empresa
    db.pessoa.empresa.writable=False
    db.pessoa.empresa.readable=False
    if not usuario:
        redirect(URL('default','index'))
    form = SQLFORM(db.pessoa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)
@auth.requires_login()
def alterar():
    response.view = 'generic.html' # use a generic view
    request.function='Alterar Contratado'
    pessoa=db.pessoa(db.pessoa.id==request.args(0, cast=int))
    db.pessoa.id.writable=False
    db.pessoa.id.readable=False
    db.pessoa.empresa.writable=False
    db.pessoa.empresa.readable=False
    form = SQLFORM(db.pessoa, pessoa.id, deletable=False)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
