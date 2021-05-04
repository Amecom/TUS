# -*- coding: utf-8 -*-
import serverutils

users = {
    'admin@example.it': {
        'uid': 1,
        'token': "123456789abc123456789abc123456789abc",
        'auths': {serverutils.AUTH_ADMIN},
        'password': "123"
    },
    'power@example.it': {
        'uid': 2,
        'token': "789abc123456789abc123456789abc123456",
        'auths': {serverutils.AUTH_POWER},
        'password': "456"
    },
    'user@example.it': {
        'uid': 2,
        'token': "c12345656789ab789abc123456789abc1234",
        'auths': set(),
        'password': "789"
    },
}