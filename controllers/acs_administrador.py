# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    projeto=db.projeto(db.projeto.id==request.args(0, cast=int))
    paginacao = 35
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        redirect(URL(args=[projeto.id,1]))
    total = db((db.usuario_empresa.empresa==empresa.id)).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.usuario_empresa.empresa==empresa.id)).select(
      limitby=limites,orderby=db.usuario_empresa.id
      )
    consul=(request.args(2))
    if (consul):
        registros = db((db.usuario_empresa.empresa==empresa.id)&((db.usuario_empresa.nome.contains(consul)))).select(limitby=(0,paginacao))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, usuario=usuario, consul=consul ,projeto=projeto)

@auth.requires_login()
def escolher():
    projeto=db.projeto(request.args(0, cast=int))
    usuario=db.usuario_empresa(request.args(1, cast=int))
    projeto.administrador = usuario.id
    projeto.update_record()
    redirect(URL('index', args=[projeto.id,1]))
    return locals()
