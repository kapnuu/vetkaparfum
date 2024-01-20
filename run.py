import os

from waitress import serve

from vetka import app

app.secret_key = os.urandom(16)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = int(os.getenv('HTTP_PORT') or 55010)
    # app.run(host=HOST, port=PORT, debug=True, ssl_context=None)
    serve(app, host=HOST, port=PORT)
