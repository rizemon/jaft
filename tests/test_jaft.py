import socket
import threading
from tempfile import TemporaryDirectory, NamedTemporaryFile
from time import sleep

import pytest
from jaft import __version__
from jaft.__main__ import JAFT
from paramiko import RSAKey

TEST_ADDRESS = '127.0.0.1'
TEST_FTP_PORT = 2121
TEST_HTTP_PORT = 8080
TEST_SMB_PORT = 4455
TEST_SFTP_PORT = 2222
TEST_NC_PORT = 4444


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


@pytest.fixture
def helper_functions():
    return HelperFunctions


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    with TemporaryDirectory() as tmpdir:
        # Before
        tmpfile = NamedTemporaryFile()
        tmpkey = RSAKey.generate(4096)
        tmpkey.write_private_key_file(tmpfile.name)

        jaft = JAFT(
            priv_key_path=tmpfile.name,
            directory=tmpdir,
            address=TEST_ADDRESS,
            ftp_port=TEST_FTP_PORT,
            http_port=TEST_HTTP_PORT,
            smb_port=TEST_SMB_PORT,
            sftp_port=TEST_SFTP_PORT,
            nc_port=TEST_NC_PORT
        )

        t = threading.Thread(target=jaft.run)
        t.start()
        sleep(0.1)
        # During
        yield
        # After
        jaft.stop()


def test_version():
    assert __version__ == '0.0.1'


def test_ftp_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, TEST_FTP_PORT))


def test_http_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, TEST_HTTP_PORT))


def test_sftp_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, TEST_SFTP_PORT))


def test_smb_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, TEST_SMB_PORT))


def test_nc_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, TEST_NC_PORT))
