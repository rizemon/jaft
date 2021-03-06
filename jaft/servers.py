import logging
import signal
from abc import ABC, abstractmethod
from functools import partial
from http.server import SimpleHTTPRequestHandler
from os.path import dirname, isdir, join
from socket import AF_INET, SOCK_STREAM, socket, timeout as stimeout
from socketserver import TCPServer
from threading import Thread
from time import sleep

import coloredlogs
from impacket.smbserver import SimpleSMBServer
from paramiko import RSAKey, SFTPServer, Transport
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from sftpserver.stub_sftp import StubServer, StubSFTPServer

"""
Classes:
-> Service
-> HTTPService
-> FTPService
-> SMBService
-> SFTPService
"""

logger = logging.getLogger('jaft')
pyftpdlib_logger = logging.getLogger('pyftpdlib')
smbserver_logger = logging.getLogger('impacket.smbserver')
httpserver_logger = logging.getLogger('http.server')

# Only enable INFO logging for jaft
coloredlogs.install(
        level=logging.INFO,
        logger=logger,
        fmt='%(asctime)s [%(name)s:%(filename)s:%(lineno)d] \
%(levelname)s %(message)s'
)
for lg in [pyftpdlib_logger, smbserver_logger, httpserver_logger]:
    coloredlogs.install(
        level=logging.WARNING,
        logger=lg,
        fmt='%(asctime)s [%(name)s:%(filename)s:%(lineno)d] \
%(levelname)s %(message)s'
    )


class Service(ABC):

    def __init__(self, address, port, directory, priv_key_path=''):
        self.address = address
        self.port = port
        self.directory = directory
        self.priv_key_path = priv_key_path

    @abstractmethod
    def start(self):
        return NotImplemented

    @staticmethod
    def ignore_keyboard_interrupt(func):
        def _wrapper(*args):
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            func(*args)
        return _wrapper


class FTPService(Service):

    @Service.ignore_keyboard_interrupt
    def start(self):
        handler = FTPHandler
        handler.authorizer = self._AnyAuthorizer(directory=self.directory)
        ftpd = self._FTPServerWrapper((self.address, self.port), handler)

        logger.info(f'Started FTP Service on {self.address}:{self.port}')
        ftpd.serve_forever()

    class _FTPServerWrapper(FTPServer):

        def serve_forever(self, *args, **kwargs):
            return super().serve_forever(*args, **kwargs)

    class _AnyAuthorizer(DummyAuthorizer):

        def __init__(self, directory):
            self.directory = directory
            super().__init__()

        def validate_authentication(self, *args, **kwargs):
            pass

        def has_user(self, *args, **kwargs):
            return True

        def get_home_dir(self, *args, **kwargs):
            return self.directory

        def has_perm(self, *args, **kwargs):
            return True

        def get_msg_login(self, *args, **kwargs):
            return ''

        def get_msg_quit(self, *args, **kwargs):
            return ''


class HTTPService(Service):

    @Service.ignore_keyboard_interrupt
    def start(self):
        TCPServer.allow_reuse_address = True

        wrapper = partial(self._HTTPServerWrapper, directory=self.directory)

        with TCPServer(
            (self.address, self.port),
            wrapper,
        ) as httpd:
            logger.info(f'Started HTTP Service on {self.address}:{self.port}')
            try:
                httpd.serve_forever()
            except Exception:
                httpd.shutdown()

    class _HTTPServerWrapper(SimpleHTTPRequestHandler):

        def do_PUT(self):
            full_path = self.translate_path(self.path)

            if full_path.endswith('/') or isdir(full_path):
                self.send_response(405, 'Method Not Allowed')
                self.end_headers()
                return

            if not isdir(dirname(full_path)):
                self.send_response(404, 'Not Found')
                self.end_headers()
                return

            size = int(self.headers['Content-Length'])

            with open(full_path, 'wb') as f:
                bytes_from_file = self.rfile.read(size)
                f.write(bytes_from_file)

            self.send_response(201, 'Created')
            self.end_headers()

        def log_message(self, *args, **kwargs):
            if (len(args) != 4):
                return
            client_ip = self.client_address[0]
            request_line = args[1]
            status_code = args[2]
            httpserver_logger.info(f'{client_ip} "{request_line}" \
{status_code}')


class SMBService(Service):

    SHARE_NAME = 'jaft'

    @Service.ignore_keyboard_interrupt
    def start(self):
        smbd = SimpleSMBServer(
            listenAddress=self.address,
            listenPort=self.port
        )
        smbd.addShare(self.SHARE_NAME, self.directory)
        smbd.setSMB2Support(True)

        logger.info(f'Started SMB Service on {self.address}:{self.port}')
        smbd.start()


class SFTPService(Service):

    MAX_CONNECTIONS = 10

    @Service.ignore_keyboard_interrupt
    def start(self):
        try:
            key = RSAKey.from_private_key_file(
                self.priv_key_path
            )
        except FileNotFoundError:
            key = RSAKey.generate(4096)

        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((self.address, self.port))
        server_socket.listen(self.MAX_CONNECTIONS)

        logger.info(f'Started SFTP Service on {self.address}:{self.port}')

        while True:
            conn, _ = server_socket.accept()
            client_thread = self._SFTPConnection(conn, key, self.directory)
            client_thread.setDaemon(True)
            client_thread.start()

    # Referenced from
    # https://gist.github.com/Girgitt/2df036f9e26dba1baaddf4c5845a20a2
    class _SFTPConnection(Thread):
        def __init__(self, conn, key, directory):
            self.conn = conn
            self.key = key
            self.directory = directory
            super().__init__()

        def run(self):
            transport = Transport(self.conn)
            transport.add_server_key(self.key)
            StubSFTPServer.ROOT = self.directory

            transport.set_subsystem_handler(
                'sftp',
                SFTPServer,
                StubSFTPServer
            )
            transport.start_server(server=StubServer())

            with transport.accept() as _:
                while transport.is_active():
                    sleep(1)
                transport.close()

            self.conn.close()
