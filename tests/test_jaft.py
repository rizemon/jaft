from jaft import __version__

from .util import *

from jaft.__main__ import DEFAULT_PORT_SMB, DEFAULT_PORT_SFTP, \
    DEFAULT_PORT_FTP, DEFAULT_PORT_HTTP


def test_version():
    assert __version__ == '0.0.2'


def test_ftp_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, DEFAULT_PORT_FTP))


def test_http_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, DEFAULT_PORT_HTTP))


def test_sftp_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, DEFAULT_PORT_SFTP))


def test_smb_service_is_up(helper_functions):
    assert(helper_functions.test_connection(TEST_ADDRESS, DEFAULT_PORT_SMB))
