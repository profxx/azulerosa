# -*- coding: utf-8
# Teste PipélineHook

from flask import Flask, jsonify, Blueprint, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from flask.cli import FlaskGroup
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from blacklist import BLACKLIST

from api_admin import bp_admin as api_admin


from db import db
from default_data import delivery_data


app = Flask(__name__)

app.config.from_object("config.Config")

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Register Bluprint
app.register_blueprint(api_admin)


# BCrypt
bcrypt = Bcrypt(app)

# Data Base
db.init_app(app)

# Migrate
migrate = Migrate(app, db)


# jwt
jwt = JWTManager(app)


# Load profile jwt
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles': user.get("roles"), "endoints": ['%s' % rule for rule in app.url_map.iter_rules()]}

# Get User Id JWT


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.get("id")

# Message Expire Token


@jwt.expired_token_loader
def my_expire_token_callback(expire_token):

    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'Seu acesso expirou. Faça Login novamente!'
    }), 401


@jwt.token_in_blacklist_loader
def check_blacklist(token):
    return token["jti"] in BLACKLIST


@jwt.unauthorized_loader
def error_load_token(fn):
    return jsonify({"message": "Sem autorização. Faça Login!"}), 401

# Message Error read Token in header


@jwt.invalid_token_loader
def erro_token(e):
    return jsonify({"message": "Token inválido"}), 422

# Error token revoked


@jwt.revoked_token_loader
def token_invalidado():
    return jsonify({"message": "Você não esta  logado. Faça login Novamente"}), 401


# Before first request
@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def hello():
    return redirect("/api/v1/admin")

# Redirect for doc in 404


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "URL not Found"}), 404


cli = FlaskGroup(app)


# Commands
@cli.command('create_db')
def createdb():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Defaults Data


@cli.command('create_data')
def create_data():
    delivery_data()


if __name__ == "__main__":
    cli()
