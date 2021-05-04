# -*- coding: utf-8 -*-
import flask
import ujson
import serverutils
import serverdata

app = flask.Flask(__name__)


@app.route("/")
def home():
    return "Hello!"


@app.route('login', methods=["POST"])
def login():
    # PSEUDO CODE //
    params = ujson.loads(flask.request.form.get("json"))
    email = params['email']
    user = serverdata.users.get(email)
    if user and params['password'] == user['password']:
        return serverutils.send_json_response({
            'user_id': user['uid'],
            'signature': user['token']
        })
    return serverutils.send_json_error("Login error", 500)


@app.route('/get_user_data', methods=["POST"])
@serverutils.tus
def get_user_data(params, uid, auths, _token):
    return example_response(params, uid, auths)


@app.route('/execute_if_admin', methods=["POST"])
@serverutils.tus(auths={serverutils.AUTH_ADMIN})
def execute_if_admin(params, uid, auths, _token):
    return example_response(params, uid, auths)


@app.route('/execute_if_any_roles', methods=["POST"])
@serverutils.tus(auths={serverutils.AUTH_ADMIN, serverutils.AUTH_POWER})
def execute_if_any_roles(params, uid, auths, _token):
    return example_response(params, uid, auths)


@app.route('/execute_arg/<arg>', methods=["POST"])
@serverutils.tus(auths={serverutils.AUTH_ADMIN, serverutils.AUTH_POWER})
def execute_if_any_roles(params, uid, auths, _token, arg):
    print("Recived arg=", arg)
    return example_response(params, uid, auths)


def example_response(params, uid, auths):
    return serverutils.send_json_response({
        'recived_params': params,
        'recived_uid': uid,
        'uid_auths': auths
    })
