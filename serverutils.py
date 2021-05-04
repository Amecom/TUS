# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from time import mktime
from datetime import datetime,  timezone

import flask
import hashlib
import ujson

import serverdata

app = flask.Flask(__name__)

AUTH_ALL = 1
AUTH_POWER = 100
AUTH_ADMIN = 255

STR_STAMP = '%Y%m%d%H%M%S'

__version__ = '1.0'

def tus(original_function=None, *, auths=None):
    def _decorate(view):
        @wraps(view)
        def verify(*args, **kwargs):

            payload = flask.request.get_data().decode("utf-8")
            rf = flask.request.form

            # T.ime
            t = rf["t"]
            # U.ser id
            u = int(rf["u"])
            # S.ignature
            s = request.args["s"]

            # deve esserci sempre un json magari
            # e deve essere sempre un dizionario, magari vuoto {}
            data = ujson.loads(request.form.get("json"))

            if abs(get_minutes_diff_from_now_and_stamp(t)) > 15:
                return send_json_error("Time inconsistency", 428)

            access_token = get_token_by_signature(u, payload, s)

            if not access_token:
                return send_json_error("Precondition fails", 428)

            user_auths = get_user_auths(u)

            if auths and not has_any_auth(user_auths, auths):
                return send_json_error("Not allowed", 401)

            return view(data, u, user_auths, access_token, *args, **kwargs)

        return verify

    if original_function:
        return _decorate(original_function)
    return _decorate


def send_json_response(obj, status=200):
    return flask.Response(
        ujson.dumps(obj),
        status=status,
        mimetype='application/json'
    )


def send_json_error(message=None, status=500):
    if message is None:
        message = "Unknow error"
    return send_json_response({"error": message}, status)


# PRIVATE


def get_token_by_signature(uid, request_payload, signature):
    # PSEUDO CODE
    for user in serverdata.users:
        if uid == user['uid']:
            access_token = user['token']
            to_hash = request_payload + access_token
            test_signature = hashlib.md5(to_hash.encode('utf-8')).hexdigest()
            if test_signature == signature:
                return access_token
    return None


def get_user_auths(uid):
    # importante usare get dato che nella tabella user_roles
    # l'uid potrebbe non esistere !
    # PSEUDO CODE
    for user in serverdata.users:
        if uid == user['uid']:
            return user['auths']
    return set()


def has_any_auth(user_auths: set, need_any_auths: set) -> bool:
    return AUTH_ALL in need_any_auths or user_auths & need_any_auths


def get_minutes_diff_from_now_and_stamp(s):     # s = stamp
    """Calcola la differenza in minuti tra adesso e una data in formato stamp.
    Numeri negativi se la data passata e' nel PASSATO"""

    return get_minutes_diff_from_now_and_datetime(stamp_to_datetime(s))


def get_minutes_diff_from_now_and_datetime(d):  # d = datetime
    """Calcola la differenza in minuti tra adesso e una data in formato datetime.
    Numeri negativi se la data passata e' nel passato"""
    now = datetime.now(timezone.utc)
    d1_ts = mktime(d.timetuple())
    d2_ts = mktime(now.timetuple())
    return int(int(d1_ts - d2_ts) / 60)


def stamp_to_datetime(d):
    """Converte una data da stringstamp -> a datetime (python) """
    norm_d = str(d)
    # la stringa di conversione rappresenta ogni parte
    # di una data con due caratteri: %X
    # mentre la data in formato stamp ha sempre 2 cifre
    # ed esclusione dell'anno
    # quindi per calcolare l'esatta lunghezza della stringa
    # di covenrsione deve:
    # 1) riurre la stringa ai primi 14 caratteri
    # (altri potrebbero essere contatori non data)
    norm_d = norm_d[:14]

    # calcolo la lugezza della stringa di conversione contanto
    # i caratteri e sottaendo 2 per l'anno
    str_conversion_lenght = len(norm_d) - 2
    norm_str_stamp = STR_STAMP[:str_conversion_lenght]

    # forzo la conversione in UTC
    return datetime.strptime(norm_d, norm_str_stamp).replace(tzinfo=timezone.utc)
