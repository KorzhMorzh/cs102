import asyncore
import asynchat
import logging
import mimetypes
import os
from urllib.parse import urlparse, unquote
import argparse
from time import strftime, gmtime


def url_normalize(path):  # дано
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1+3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    return path


def read_file(path):
    file = bytes()
    fp = FileProducer(open(path, 'rb'))
    while True:
        cur_chunk = fp.more()
        if not cur_chunk:
            break
        file += cur_chunk

    return file


class FileProducer(object):  # Дано

    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class AsyncServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000, handler_class=None):
        super().__init__()
        self.handler_class = handler_class
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        logging.debug(f"Incoming connection from {addr}")
        self.handler_class(sock)

    def serve_forever(self):  # зациклить прием запросов, не отваливаться после обработки первого пришедшего.
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            logging.debug("Shutting down")
        finally:
            self.close()


class AsyncHTTPRequestHandler(asynchat.async_chat):  # обработка запроса

    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b"\r\n\r\n")
        self.reading_headers = True
        self.ibuffer = ''  # входящий
        self.obuffer = b''  # исходящий
        self.headers = {}
        self.request_method = None
        self.response = ''
        self.request = ''

    def collect_incoming_data(self, data):
        if not self.reading_headers:
            self.obuffer = data
        else:
            self.ibuffer += data.decode('utf-8')

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        if self.reading_headers:
            self.reading_headers = False
            self.headers['method'], self.headers['path'], self.ibuffer = self.ibuffer.split(' ', 2)
            self.headers['protocol'], headers = self.ibuffer.split('\r\n', 1)
            self.parse_headers(headers)
            self.headers['path'] = unquote(self.headers['path'])
            self.headers['path'] = self.translate_path(self.headers['path'])
            if self.headers['method'] == "POST":
                try:
                    content_length = self.headers['Content-Length']
                    if int(content_length) == 0:
                        self.send_error(400)
                    self.set_terminator(int(content_length))
                except KeyError:
                    self.send_error(400)
                    return
            elif not self.headers['method']:
                self.send_error(400)
            else:
                self.request = urlparse('http://' + self.headers['Host'] + self.headers['path']).path
                self.ibuffer = ''
                self.handle_request()
        else:
            self.request = urlparse('http://' + self.headers['Host'] + self.headers['path']).path
            self.ibuffer = ''
            self.handle_request()

    def parse_headers(self, header):
        headers_lst = header.split('\r\n')

        for header in headers_lst:

            keyword, value = header.split(':', 1)
            self.headers[keyword] = value

    def handle_request(self):  # дано
        method_name = 'do_' + self.headers['method']
        if not hasattr(self, method_name):
            self.send_error(405)
            self.handle_close()
            return
        handler = getattr(self, method_name)
        handler()

    def send_header(self, keyword, value):
        self.response += "{}: {}\r\n".format(keyword, value)

    def send_error(self, code, message=None):  # дано
        try:
            short_msg, long_msg = self.responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg

        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "close")
        self.end_headers()
        self.send(bytes(self.response.encode('utf-8')))
        self.close()

    def send_response(self, code, message=None):  # это мы уже отправляем тело ответа
        self.response += "HTTP/1.1 {} {}\r\n".format(code, message)

    def end_headers(self):
        self.response += "\r\n"

    def date_time_string(self):  # формирование заголовка Date        ок
        return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

    def add_header(self, keyword, value):
        self.response += f"{keyword}: {value}\r\n"

    def send_head(self):  # метод для отправки заголовков ответа клиенту
        path = self.translate_path(os.getcwd() + self.request)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
            if not os.path.exists(path):
                self.send_error(403)
                return None
        try:
            file = bytes()
            file_p = FileProducer(open(path, 'rb'))
            while True:
                cur_chunk = file_p.more()
                if not cur_chunk:
                    break
                file += cur_chunk
        except IOError:
            self.send_error(404)
            return None

        _, ext = os.path.splitext(path)
        file_type = mimetypes.types_map[ext.lower()]
        return file, file_type

    def translate_path(self, path):  # преобразование путей
        return url_normalize(path)

    def do_GET(self):  # обработчики конкретных типов запросов, пришедших от клиента
        file, file_type = self.send_head()
        self.send_response(200)
        self.add_header("Server", "127.0.0.1")
        self.add_header("Date", self.date_time_string())
        self.add_header("Content-Type", file_type)
        self.add_header("Content-Length", len(file))
        self.add_header("Connection", "close")
        self.end_headers()
        if file:
            response = bytes(self.response.encode('utf-8')) + file
            self.send(response)
            self.close()

    def do_HEAD(self):  # обработчики конкретных типов запросов, пришедших от клиента
        file, file_type = self.send_head()
        self.send_response(200)
        self.add_header("Server", "127.0.0.1")
        self.add_header("Date", self.date_time_string())
        self.add_header("Content-Type", file_type)
        self.add_header("Content-Length", len(file))
        self.add_header("Connection", "close")
        self.end_headers()
        if file:
            response = bytes(self.response.encode('utf-8'))
            self.send(response)
            self.close()

    def do_POST(self):
        self.send_response(200, "OK")
        self.add_header("Content-Type", self.headers['Content-Type'])
        self.add_header("Content-Length", self.headers['Content-Length'])
        self.add_header("Connection", "close")
        self.end_headers()
        response = bytes(self.response.encode('utf-8')) + self.obuffer
        self.send(response)
        self.close()

    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
    }


def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default=".")
    return parser.parse_args()


def run():
    # server = AsyncServer(host=args.host, port=args.port)
    server = AsyncServer(host="127.0.0.1", port=9000, handler_class=AsyncHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    '''args = parse_args()

    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")
    log = logging.getLogger(__name__)

    DOCUMENT_ROOT = args.document_root
    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run)
        p.start()'''
    run()
