# -*- coding: utf-8 -*-
import tus

users = {
    'admin@example.it': {
        'uid': 1,
        'token': "123456789abc123456789abc123456789abc",
        'roles': {tus.AUTH_ADMIN},
        'password': "123"
    },
    'power@example.it': {
        'uid': 2,
        'token': "789abc123456789abc123456789abc123456",
        'roles': {tus.AUTH_POWER},
        'password': "456"
    },
    'user@example.it': {
        'uid': 2,
        'token': "c12345656789ab789abc123456789abc1234",
        'roles': set(),
        'password': "789"
    },
}