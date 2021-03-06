# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'), fake_migrate_all=False,
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

db.define_table('empresa',
                #proprietario é o proprio criador
                Field('proprietario','reference auth_user', label='Proprietario', writable=False, readable=False, default=1),
                #dados empresariais
                Field('razaosocial', 'string', label='Razão Social',requires = IS_UPPER()),
                Field('nomefantasia', 'string', label='Nome Fantasia',requires = IS_UPPER()),
                Field('cnpj', 'string', label='CNPJ',default="00.000.000/0001-00"),
                Field('inscricaoestarual', 'string', label='Insc. Est',default="00000"),
                Field('inscricaomunicipal', 'string', label='Insc. Mun',default="00000"),
                Field('crt', 'string', label='CRT',default="00000"),
                #endereço
                Field('cep', 'string', label='CEP',default="60000-000"),
                Field('lougradouro', 'string', label='Lougradouro',default="Rua",requires = IS_UPPER()),
                Field('numero', 'string', label='Numero',default="0",requires = IS_UPPER()),
                Field('bairro', 'string', label='Bairro',default="Centro",requires = IS_UPPER()),
                Field('uf', 'string', label='UF',default="CE",requires = IS_UPPER()),
                Field('cidade', 'string', label='Cidade', default='Juazeiro do Norte',requires = IS_UPPER()),
                Field('complemento', 'string', label='Complemento',default="Sem Complemento",requires = IS_UPPER()),
                #controle de desenvolvedor e limitações
                Field('q_logins', 'integer', label='Q Logins', writable=False, readable=False, default=4),
                Field('q_pessoas', 'integer', label='Q Pessoas', writable=False, readable=False, default=4),
                #contato
                Field('email', 'string', label='Email',default="sem@email.com"),
                Field('telefone', 'string', label='Telefone',default="(88)3500-0000"),
                Field('celular', 'string', label='Celular',default="(88)99000-0000"),
                #informações extras do desenvolvedor
                Field('data_desaceleracao', 'date', label="Desaceleração", writable=False, readable=False, default=request.now, notnull=True),
                Field('data_bloqueio', 'date', label="Data Bloqueio", writable=False, readable=False, default=request.now, notnull=True),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                auth.signature,
                format='%(nomefantasia)s')

db.define_table('usuario_empresa',
                Field('usuario','reference auth_user', writable=False, readable=False, label='Usuario'),
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('tipo', 'string', label='tipo',default='Administrador'),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                format='%(nome)s')

db.define_table('projeto',
                Field('administrador','reference auth_user', writable=False, readable=False, label='Administrador'),
                Field('chefe_equipe','reference auth_user', writable=False, readable=False, label='Chefe'),
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('data_inicial', 'date', label="Data Inicial", default=request.now, notnull=True),
                Field('data_final', 'date', label="Data Final", writable=False, readable=False, default=request.now, notnull=True),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('comissao_prazo', 'double', label='% Comissao Prazo', notnull=True, default=5),
                Field('comissao_vista', 'double', label='% Comissao Vista', notnull=True, default=0),
                Field('total_preco', 'double', label='Total Preço', writable=False, readable=False, notnull=True, default=0),
                Field('total_custo', 'double', label='Total Custo', writable=False, readable=False, notnull=True, default=0),
                Field('total_vale_chefe', 'double', label='Total Vale Chefe', writable=False, readable=False, notnull=True, default=0),
                Field('total_vale_funcionario', 'double', label='Total Vale Funcionario', writable=False, readable=False, notnull=True, default=0),
                Field('q_funcionarios', 'integer', label='Q Funcionarios', writable=False, readable=False, default=0),
                Field('total_vale_vendedor', 'double', label='Total Vale Vendedor', writable=False, readable=False, notnull=True, default=0),
                Field('q_vendedores', 'integer', label='Q Vendedor', writable=False, readable=False, default=0),
                Field('total_despesa_local', 'double', label='Total Valor', writable=False, readable=False, notnull=True, default=0),
                Field('total_adiantamento', 'double', label='Total Valor', writable=False, readable=False, notnull=True, default=0),
                Field('total_saldo_chefe', 'double', label='Total Saldo Chefe', writable=False, readable=False, notnull=True, default=0),
                Field('total_saldo_funcionario', 'double', label='Total Saldo Funcionario', writable=False, readable=False, notnull=True, default=0),
                Field('total_saldo_vendedor', 'double', label='Total Saldo Vendedor', writable=False, readable=False, notnull=True, default=0),
                Field('total_percas', 'double', label='Total Percas', writable=False, readable=False, notnull=True, default=0),
                Field('total_preco_retorno', 'double', label='Total Preço Retorno', writable=False, readable=False, notnull=True, default=0),
                Field('total_custo_retorno', 'double', label='Total Custo Retorno', writable=False, readable=False, notnull=True, default=0),
                Field('total_debito_chefe', 'double', label='Total Debito Chefe', writable=False, readable=False, notnull=True, default=0),
                Field('total_debito_funcionario', 'double', label='Total Debito Funcionario', writable=False, readable=False, notnull=True, default=0),
                Field('total_debito_vendedor', 'double', label='Total Debito Vendedor', writable=False, readable=False, notnull=True, default=0),
                Field('total_venda', 'double', label='Total venda ', writable=False, readable=False, notnull=True, default=0),
                Field('total_recebido', 'double', label='Total recebido', writable=False, readable=False, notnull=True, default=0),
                Field('total_devolucao_dinheiro', 'double', label='Total devolução', writable=False, readable=False, notnull=True, default=0),
                Field('total_atrasado', 'double', label='Total Atrasado', writable=False, readable=False, notnull=True, default=0),
                Field('total_aguardando', 'double', label='Total Aguardando', writable=False, readable=False, notnull=True, default=0),
                Field('total_repasse', 'double', label='Total Repasse', writable=False, readable=False, notnull=True, default=0),
                Field('total_gratificacao', 'double', label='Total Gratificação', writable=False, readable=False, notnull=True, default=0),
                auth.signature,
                format='%(descricao)s')

db.define_table('pessoa',
              Field('empresa','reference empresa', label='Empresa', writable=True, readable=True),
              Field('nome', 'string', label='Nome',requires = IS_UPPER()),
              Field('apelido', 'string', label='Apelido',requires = IS_UPPER()),
              Field('celular', 'string', label='Celular',default="(88)99000-0000"),
              Field('q_projetos', 'integer', label='Q Projetos', writable=False, readable=False, default=0),
              Field('total_venda', 'double', label='Total Venda', writable=False, readable=False, notnull=True, default=0),
              Field('total_recebido', 'double', label='Total Recebido', writable=False, readable=False, notnull=True, default=0),
              Field('observacao', 'text', label='Observação',requires = IS_UPPER()),
              Field('conferido', 'boolean', writable=False, readable=False, default=False),
              format='%(nome)s')


db.define_table('produto',
              Field('empresa','reference empresa', label='Empresa', writable=True, readable=True),
              Field('descricao', 'string', label='Descricao',requires = IS_UPPER()),
              Field('custo_unitario', 'double', label='Custo Unitario', notnull=True, default=0),
              Field('preco_unitario', 'double', label='Preco Unitario', notnull=True, default=0),
              Field('observacao', 'text', label='Observação',requires = IS_UPPER()),
              Field('ativo', 'boolean', default=True),
              format='%(descricao)s')
