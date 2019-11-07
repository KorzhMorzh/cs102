import async_server
import sys


class AsyncWSGIServer(async_server.AsyncServer):

    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


class AsyncWSGIRequestHandler(async_server.AsyncHTTPRequestHandler):

    def get_environ(self):
        env = {'wsgi.version': (1, 0),
               'wsgi.url_scheme': 'http',
               'wsgi.input': sys.stdin,
               'wsgi.errors': sys.stderr,
               'wsgi.multithread': False,
               'wsgi.multiprocess': False,
               'wsgi.run_once': False,
               'REQUEST_METHOD': self.headers['method'],
               'PATH_INFO': self.headers['path'],
               'SERVER_NAME': 'localhost',
               'SERVER_PORT': '9000'}

        return env

    def start_response(self, status, response_headers, exc_info=None):
        response_code, response_message = status.split(" ")[:2]
        self.send_response(response_code, response_message)
        print('status: ', status)
        for key, value in response_headers:
            self.send_header(key, value)
            print(key, ': ', value)
        self.end_headers()

    def handle_request(self):
        env = self.get_environ()
        app = server.get_app()
        print(
            'env ', env,
            'app', app
        )
        result = app(env, self.start_response)
        self.finish_response(result)

    def finish_response(self, result):
        print(result)
        [body] = result
        self.send(bytes(self.response.encode('utf-8')) + body)
        self.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    server = AsyncWSGIServer(handler_class=AsyncWSGIRequestHandler)
    server.set_app(application)
    server.serve_forever()
