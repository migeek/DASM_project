import socketio, sys, time, requests
import globals as g

sio = socketio.Client()
ip = "0.0.0.0"     #change to ip address of server
url = 'http://' + ip + ':5000'

#connect to socketio
def start_client():
    global url
    sio.connect(url)
    print('my sid is ' + sio.sid)

def dummy_main():
    msg = ""
    while msg != 'quit':
        msg = input('Enter message to send to server: ')
        if msg == "init":
            print("sending box info")
            send_box_info()
        elif msg == "audio":
            print("sending audio file")
            send_audio(100, 1)
        else:
            sio.emit('test event', {'data': msg})
        time.sleep(5)

#disconnect from server
def close_client():
    sio.disconnect()
    print('client closed')

#connect to server
@sio.event
def connect():
    print("I'm connected!")
    print("sending box info")
    send_box_info()

#receive contact info from server
#stores into contacts array in globals.py
@sio.on('contact info')
def contact_info(data):
    print("getting contact info")
    if 'contact1' in data:
        g.contacts[0] = int(data['contact1'])
    if 'contact2' in data:
        g.contacts[1] = int(data['contact2'])
    if 'contact3' in data:
        g.contacts[2] = int(data['contact3'])
    if 'contact4' in data:
        g.contacts[3] = int(data['contact4'])
    print(g.contacts)

#receive message from server
@sio.on('return message')
def return_msg(data):
    if str(data['type']) == "audio":
        recv_audio(data)
    print('received return message from server! ')

#error event
@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

#send audio function
def send_audio(destID: int):
    path = '/api/audio'

    #create unique file name using fileCounter
    fileName = "audio-" + str(g.boxID) + "-" + str(g.fileCounter) + ".mp3"

    with open("./" + fileName, 'rb') as file:
        data = {"uuid":"-jx-1", "alarmType":1, "type": "audio", "timeDuration":10, "sendID":g.boxID, "destID":destID, "fileNum":g.fileCounter}
        files = {'messageFile': file}
        print(url+path)
        req = requests.post(url+path, files=files, data=data)
        print(req.status_code)


def recv_audio(data):
    global url
    sendID = str(data['sendID'])
    fileNum = str(data['fileNum'])

    #create fileName from file received to store locally
    fileName = "audio-" + sendID + "-" + fileNum + ".mp3"
    path = "/api/" + fileName

    print("receiving ", fileName)
    sendID = int(sendID)

    #turn on LED of button corresponding to person to signify there is a message
    if sendID == g.contacts[0]:
        g.person1led.on()
    if sendID == g.contacts[1]:
        g.person2led.on()
    if sendID == g.contacts[2]:
        g.person3led.on()
    if sendID == g.contacts[3]:
        g.person4led.on()

    r = requests.get(url+path, allow_redirects=True)

    open(fileName, 'wb').write(r.content) # change destination

#send box info to client
def send_box_info():
    data = {"type": "setup", "sendID":g.boxID}
    sio.emit('init setup', data)

#uncomment lines below for dummy client

#start_client()
#dummy_main()
#close_client()
