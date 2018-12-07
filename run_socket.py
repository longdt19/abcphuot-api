from socket_server import socket_app, flask_app


if __name__ == '__main__':
    socket_app.run(flask_app, port=5555)
