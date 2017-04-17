#! /usr/bin/python3

from requests import post, codes
from cypher import encrypt, decrypt
from time import time

SERVER_URL = 'http://127.0.0.1:5000/'

user = 'maximka'
password = 'qwe123'


def process_response(encrypted_session_key, my_key):
    decrypted_session_key = decrypt(encrypted_session_key, my_key)

    timestamp = get_timestamp()
    encrypted_id = encrypt("|".join([user, timestamp]),
                           decrypted_session_key)

    return encrypted_id, decrypted_session_key, timestamp


def get_timestamp():
    return str(int(time()))


def main():
    response = post(SERVER_URL + 'user_auth/my_tgs', data={'user': user})

    if response.status_code == codes.ok:
        content = response.json()
        print('Response from user_auth/my_tgs:', content)

        encrypted_id, tgs_session_key, _ = process_response(content['sk'],
                                                            password)
        print('TGS session key:', tgs_session_key)

        response = post(SERVER_URL + 'tgs/my_service',
                        data={'id': encrypted_id, 'tgt': content['tgt']})

        if response.status_code == codes.ok:
            content = response.json()
            print('Response from tgs/my_service:', content)

            encrypted_id, service_session_key, timestamp = \
                    process_response(content['ssk'], tgs_session_key)

            print('Service session key:', service_session_key)

            response = post(SERVER_URL + 'my_service',
                            data={'id': encrypted_id,
                                  's_ticket': content['s_ticket']})

            if response.status_code == codes.ok:
                content = response.json()
                print('Response from my_service:', content)

                decrypted_timestamp_from_service = decrypt(content['ts'],
                                                           service_session_key)

                if int(decrypted_timestamp_from_service) - int(timestamp) == 1:
                    print('Authenticated')
                    return

    print('Authentication failed')


if __name__ == '__main__':
    main()
