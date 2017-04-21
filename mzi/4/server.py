#! /usr/bin/python3

from flask import Flask, request, abort, jsonify
from json import load
from uuid import uuid4
from cypher import encrypt, decrypt
from time import time

app = Flask(__name__)

USER_NAME_KEY = 'user'
TGS_NAME = 'tgs_name'
SERVICE_NAME = 'my_service'

tgs_private_keys = {
    TGS_NAME: 'zxcvbn',
}

service_private_keys = {
    SERVICE_NAME: 'oiuytrewq',
}


@app.route('/user_auth/<tgs>', methods=['POST'])
def user_auth(tgs):
    user = request.form[USER_NAME_KEY]

    if tgs == TGS_NAME:
        with open('user_db', 'r') as db:
            user_db = load(db)

        if user in user_db:
            session_key = str(uuid4())
            print(session_key)

            encrypted_session_key = encrypt(session_key, user_db[user])

            tgt = '|'.join([session_key, user, request.remote_addr])
            encrypted_tgt = encrypt(tgt, tgs_private_keys[tgs])

            return jsonify({'sk': encrypted_session_key,
                            'tgt': encrypted_tgt}), 200

    abort(404)


@app.route('/tgs/<service_name>', methods=['POST'])
def tgs(service_name):
    id, tgt = request.form['id'], request.form['tgt']

    if service_name == SERVICE_NAME:
        decrypted_tgt = decrypt(tgt, tgs_private_keys[TGS_NAME])
        print(decrypted_tgt)

        session_key, user, address = decrypted_tgt.split('|')

        decrypted_id = decrypt(id, session_key)
        print(decrypted_id)

        id_user, id_timestamp = decrypted_id.split('|')

        if (_check_timestamp(int(id_timestamp))
                and user == id_user
                and address == request.remote_addr):

            server_session_key = str(uuid4())
            print(server_session_key)

            encrypted_server_session_key = encrypt(server_session_key,
                                                   session_key)

            service_ticket = "|".join([server_session_key,
                                       user,
                                       address,
                                       _get_exp_timestamp()])

            encrypted_service_ticket = encrypt(service_ticket,
                                               service_private_keys[SERVICE_NAME])

            return jsonify({'ssk': encrypted_server_session_key,
                            's_ticket': encrypted_service_ticket}), 200

    abort(404)


@app.route('/my_service', methods=['POST'])
def my_service():
    id, ticket = request.form['id'], request.form['s_ticket']

    decrypted_ticket = decrypt(ticket,
                               service_private_keys[SERVICE_NAME])

    session_key, user, address, exp_timestamp = decrypted_ticket.split('|')

    decrypted_id = decrypt(id, session_key)

    id_user, id_timestamp = decrypted_id.split('|')
    id_timestamp = int(id_timestamp)

    if (_check_timestamp(id_timestamp)
                and user == id_user
                and address == request.remote_addr
                and not _is_expired(int(exp_timestamp))):
        print('ok')

        incremented_timestamp = str(id_timestamp + 1)
        encrypted_incremented_timestamp = encrypt(incremented_timestamp,
                                                  session_key)

        return jsonify({'ts': encrypted_incremented_timestamp}), 200

    abort(404)


def _check_timestamp(timestamp):
    delta = 5 * 60
    current_timestamp = int(time())
    return abs(timestamp - current_timestamp) < delta


def _get_exp_timestamp():
    return str(int(time()) + 60 * 60)


def _is_expired(timestamp):
    return timestamp < int(time())


if __name__ == '__main__':
    app.run()
