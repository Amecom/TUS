# -*- coding: utf-8 -*-
"""
This file shows how the TUS protocol can be used to easily and clearly secure specific routes
using decorator

Author: Amedeo Celletti (info@amecom.it)
"""

import flask
import json
import tus
import userdata

app = flask.Flask(__name__)


def _example_response(params, uid, auths):
    """
    Example of response for the routes wrapped with "TUS".
    The received parameters are returned.
    :param params: Object with params sended by client request
    :param uid: User ID
    :param auths: Set of User Id roles
    :return:
    """
    return tus.send_response({
        'recived_params': params,
        'recived_uid': uid,
        'uid_auths': auths
    })


@app.route("/")
def home():
    """
    Test home route
    :return:
    """
    return "Hello!"


@app.route('login', methods=["POST"])
def login():
    """
    *** PSEUDO CODE ***
    The login logic depends on the individual implementations.
    The important, if successful login,
    a "user_id" and the "signature" token are returned.

    The "signature" token must be persistent
    and will be used to sign subsequent requests.

    :return: Object
    """
    params = json.loads(flask.request.form.get("json"))
    email = params['email']
    user = userdata.users.get(email)
    if user and params['password'] == user['password']:
        return tus.send_response({
            'user_id': user['uid'],
            'signature': user['token']
        })
    return tus.send_error("Login error")


"""
EXAMPLES OF ROUTES PROTECTED BY TUS Decorator
"""


@app.route('/execute_if_valid_signature', methods=["POST"])
@tus.tus
def execute_if_valid_signature(params, uid, auths):
    """
    Adding "tus" decorator without arguments the function will be executed
    if the signature applied to the request is valid, with no other checks.
    """
    return _example_response(params, uid, auths)


@app.route('/execute_if_admin', methods=["POST"])
@tus.tus(auths={tus.AUTH_ADMIN})
def execute_if_admin(params, uid, auths):
    """
    Addig "tus" decorator with "auths" parameter the function will
    be executed if the signature applied to the request is valid
    and the user has "admin" role.
    """
    return _example_response(params, uid, auths)


@app.route('/execute_if_any_roles', methods=["POST"])
@tus.tus(auths={tus.AUTH_ADMIN, tus.AUTH_POWER})
def execute_if_any_roles(params, uid, auths):
    """
    In this example the route access is allowed if user has "ADMIN" or "POWER" role.
    The function will be executed if the signature applied to the request is valid,
    and the user has "admin" OR "power" role.
    """
    return _example_response(params, uid, auths)


@app.route('/execute_arg/<arg>', methods=["POST"])
@tus.tus(auths={tus.AUTH_ADMIN, tus.AUTH_POWER})
def execute_if_any_roles(params, uid, auths, arg):
    """
    In this example the route access is allowed if user has "ADMIN" or "POWER" role.
    Compared to the previous example,
    let's see how it is possible to add an additional parameter <arg> through querystring
    """
    print("Recived arg=", arg)
    return _example_response(params, uid, auths)
