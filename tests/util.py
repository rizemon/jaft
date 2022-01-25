import os
import random
import socket
import string
import threading
from tempfile import TemporaryDirectory
from time import sleep

import pytest
from jaft.__main__ import JAFT, DEFAULT_PORT_FTP, DEFAULT_PORT_HTTP, \
    DEFAULT_PORT_SMB, DEFAULT_PORT_SFTP

TEST_ADDRESS = '127.0.0.1'


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    with TemporaryDirectory() as tmpdir:
        # Before
        jaft = JAFT(
            directory=tmpdir,
            address=TEST_ADDRESS,
            ftp_port=DEFAULT_PORT_FTP,
            http_port=DEFAULT_PORT_HTTP,
            smb_port=DEFAULT_PORT_SMB,
            sftp_port=DEFAULT_PORT_SFTP
        )

        t = threading.Thread(target=jaft.run)
        t.start()
        # Ensure all services are loaded
        sleep(3.0)

        # During
        yield

        # After
        jaft.stop()


class HelperFunctions:
    @staticmethod
    def test_connection(address, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            try:
                s.connect((address, port))
            except socket.timeout:
                return False
            finally:
                s.close()
        return True

    @staticmethod
    def generate_random_filename():
        # Referenced from https://stackoverflow.com/a/44357246
        return ''.join(
            random.choice(string.ascii_lowercase) for _ in range(16)
        )

    @staticmethod
    def generate_random_filebytes():
        return os.urandom(16)


@pytest.fixture
def helper_functions():
    return HelperFunctions
