# -*- coding: utf-8 -*-
def investimento():
    projeto=db.projeto(request.args(0, cast=int))
    return locals()
