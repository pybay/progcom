#!/usr/bin/env python
import os
from hashlib import sha1
from calendar import timegm
from datetime import datetime
import sys

import pytz
import requests
from raven import Client
from simplejson import JSONDecodeError
from requests.exceptions import RequestException

import logic as l

API_KEY = os.environ['PYCON_API_KEY']
API_SECRET = os.environ['PYCON_API_SECRET']
API_HOST = os.environ['PYCON_API_HOST']

PYBAY_API_TOKEN = "test"
API_TOKEN_PATH = '/home/pybay/api_token.txt'

if os.path.exists(API_TOKEN_PATH):
    with open(API_TOKEN_PATH) as f:
        token = f.read().strip()
        PYBAY_API_TOKEN = token


def api_call(api_suffix):
    result = requests.get(
        "http://pybay.com/api/{}".format(api_suffix),
        params={'token': PYBAY_API_TOKEN},
    )
    result = result.json()
    return result


def fetch_ids():
    raw = api_call('undecided_proposals')
    rv = [x['id'] for x in raw['data']]
    return rv


def fetch_talk(id):
    rv = api_call('proposals/{}/'.format(id))
    if not rv or 'data' not in rv:
        return {}
    rv = rv['data']
    rv['authors'] = rv['speakers']
    del rv['speakers']
    rv.update(rv['details'])
    del rv['details']

    # NOTE: Since we changed the field `what_attendees_will_learn` to
    # `what_will_attendees_learn` in PyBay (https://github.com/pybay/pybay/pull/224)
    # This will case issues in progcom. To avoid this issue, let's rename the field
    # before it gets ingested by Progcom
    what_attendees_will_learn = rv.pop('what_attendees_will_learn')
    rv['what_will_attendees_learn'] = what_attendees_will_learn

    return rv

def main():
    for id in fetch_ids():
        print('FETCHING {}'.format(id))
        try:
            proposal = fetch_talk(id)
            if proposal:
                l.add_proposal(proposal)
        except Exception as e:
            print('ERROR FETCHING {}: {}'.format(id, repr(e)))

if __name__ == '__main__':
    main()
