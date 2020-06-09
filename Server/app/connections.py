from flask import request
from app.models import Box

from app import sio

sid_list = {}  # bid/socket dict


@sio.on('connect')
def connect():
    print('connected: ' + request.sid)


@sio.on('init setup')
def handle_setup(data):
    if data['type'] == 'setup':
        sid_list[int(data['sendID'])] = request.sid
        bx = Box.query.get(data['sendID'])
        print('box {} connected'.format(bx.bid))
        if bx is not None:
            update_contacts(bx, request.sid)
        else:
            # wait for registration
            pass
    else:
        print('how did you get here?')


@sio.on('disconnect')
def disconnect():
    print('test disconnect')
    for key, val in sid_list.items():
        if val == request.sid:
            print('box {} disconnected'.format(key))
            sid_list.pop(key, None)
            break


def send_audio(data):
    dest = int(data['destID'])
    if str(data['type']) == 'audio':
        if dest in list(sid_list.keys()):
            print('telling client there be data')
            sio.emit('return message', data=data, room=sid_list[dest])
        else:
            print('aaaaaaa')


def update_contacts(bx, sid):
    data = [b.bid for b in Box.query.filter_by(user_id=bx.user_id) if
            b.bid != bx.bid]
    data_dict = {}
    for i in range(len(data)):
        data_dict['contact{}'.format(i + 1)] = data[i]
    sio.emit('contact info', data=data_dict, room=sid)
