from app import app, sio

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port='5000', debug=True)
