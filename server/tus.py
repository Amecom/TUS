# -*- coding: utf-8 -*-
"""

Author: Amedeo Celletti (info@amecom.it)
"""
import flask
import hashlib
import json

# user data used the manage login end roles
import userdata

from functools import wraps
from time import mktime
from datetime import datetime, timezone


# It allows to manage time inconsistencies
# between client and server
MAX_MINUTES_TIME_INCONSISTENCY = 15

# EXAMPLE OF USER ROLE ID
# Each implementation can freely define the roles to manage
AUTH_POWER = 100
AUTH_ADMIN = 255

STR_STAMP = '%Y%m%d%H%M%S'


def tus(original_function=None, *, auths=None):
    """
    Route decorator that allow the use of TUS protocoll.

    The decorated function is collad only if:
        - the request signatur is valid
        - the user has requested role (if roles are specified)

    If called decorated function recives:
        - data: an object with the data sended by the client
        - user ID: user ID (int)
        - user_auths: Set of user roles (can be empty set)
        - *args,
        - **kwargs
    """
    def _decorate(view):
        @wraps(view)
        def verify(*args, **kwargs):

            payload = flask.request.get_data().decode("utf-8")
            rf = flask.request.form
            ra = flask.request.args

            # T.ime
            t = rf["t"]
            # U.ser id
            u = int(rf["u"])
            # S.ignature
            s = ra["s"]

            # deve esserci sempre un json magari
            # e deve essere sempre un dizionario, magari vuoto {}
            data = json.loads(rf.get("json"))

            if abs(get_minutes_diff_from_now_and_stamp(t)) > MAX_MINUTES_TIME_INCONSISTENCY:
                return send_error("Time inconsistency", 428)

            user_token = get_token_by_signature(u, payload, s)

            if not user_token:
                return send_error("Precondition fails", 428)

            user_roles = get_user_roles(u)

            if auths and not has_any_auth(user_roles, auths):
                return send_error("Not allowed for user role", 401)

            return view(data, u, user_roles, *args, **kwargs)

        return verify

    if original_function:
        return _decorate(original_function)
    return _decorate


def send_response(obj, status=200):
    """
    All server response must be on Object with data returned by server route
    :param obj: Server response
    :param status: HTTP status code
    :return:
    """
    return flask.Response(json.dumps(obj), status=status, mimetype='application/json')


def send_error(message=None, status=500):
    """
    Default error response if client can not perform action on server,
    :param message: String of Error description
    :param status:
    :return:
    """
    if message is None:
        message = "Undefined error"
    return send_response({"error": message}, status)


# PSEUDO FUNCTIONS

def get_token_by_signature(uid, request_payload, signature):
    """
    *** PSEUDO CODE Implementations can handle this block depending on the specific data structure. ***
    This function verify if  "signature" is valid if applied to "request_payload" by "uid"
    :param uid: User ID
    :param request_payload: Data recived
    :param signature: Signature recived
    :return: None if the request signature is invalid else user "signature" token
    """
    for user in userdata.users:
        if uid == user['uid']:
            token = user['token']
            to_hash = request_payload + token
            test_signature = hashlib.md5(to_hash.encode('utf-8')).hexdigest()
            if test_signature == signature:
                return token
    return None


def get_user_roles(uid):
    """
    *** PSEUDO CODE Implementations can handle this block depending on the specific data structure. ***
    :param uid: User ID
    :return: Set of User ID roles
    """
    for user in userdata.users:
        if uid == user['uid']:
            return user['roles']
    return set()


# PRIVATE


def has_any_auth(user_auths: set, need_any_auths: set) -> bool:
    return not need_any_auths or user_auths & need_any_auths


def get_minutes_diff_from_now_and_stamp(s):     # s = stamp
    return get_minutes_diff_from_now_and_datetime(stamp_to_datetime(s))


def get_minutes_diff_from_now_and_datetime(d):  # d = datetime
    now = datetime.now(timezone.utc)
    d1 = mktime(d.timetuple())
    d2 = mktime(now.timetuple())
    return int(int(d1 - d2) / 60)


def stamp_to_datetime(d):
    norm_d = str(d)[:14]
    str_conversion_lenght = len(norm_d) - 2
    norm_str_stamp = STR_STAMP[:str_conversion_lenght]
    return datetime.strptime(norm_d, norm_str_stamp).replace(tzinfo=timezone.utc)
