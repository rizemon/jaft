import tempfile
from ftplib import FTP

import paramiko
import requests
from jaft.servers import SMBService
from smb.SMBConnection import SMBConnection
from jaft.__main__ import DEFAULT_PORT_HTTP, DEFAULT_PORT_FTP, \
    DEFAULT_PORT_SFTP, DEFAULT_PORT_SMB

from .util import *


def test_http_service_upload_success(helper_functions):
    file_name = helper_functions.generate_random_filename()
    file_bytes = helper_functions.generate_random_filebytes()
    url = f"http://{TEST_ADDRESS}:{DEFAULT_PORT_HTTP}/{file_name}"
    r = requests.put(url, data=file_bytes)
    assert(r.status_code == 201)

    contents = requests.get(url).content
    assert(contents == file_bytes)


def test_http_service_upload_dirpath(helper_functions):
    url = f"http://{TEST_ADDRESS}:{DEFAULT_PORT_HTTP}/"
    r = requests.put(url)
    assert(r.status_code == 405)


def test_http_service_upload_unknowndir(helper_functions):
    file_name = helper_functions.generate_random_filename()
    file_dir = helper_functions.generate_random_filename()
    file_bytes = helper_functions.generate_random_filebytes()
    url = f"http://{TEST_ADDRESS}:{DEFAULT_PORT_HTTP}/{file_dir}/{file_name}"
    r = requests.put(url, data=file_bytes)
    assert(r.status_code == 404)


def test_ftp_service_upload_success(helper_functions):
    file_name = helper_functions.generate_random_filename()
    file_bytes = helper_functions.generate_random_filebytes()
    ftp = FTP()
    ftp.connect(TEST_ADDRESS, DEFAULT_PORT_FTP)
    ftp.login()

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(file_bytes)
        fp.seek(0)
        resp = ftp.storbinary(f'STOR {file_name}', fp)
        assert(resp == "226 Transfer complete.")

    with tempfile.NamedTemporaryFile() as fp:
        resp = ftp.retrbinary(f'RETR {file_name}', fp.write)
        fp.seek(0)
        assert(fp.read() == file_bytes)


def test_smb_service_upload_success(helper_functions):
    file_name = helper_functions.generate_random_filename()
    file_bytes = helper_functions.generate_random_filebytes()
    conn = SMBConnection("", "", "", "")
    conn.connect(TEST_ADDRESS, DEFAULT_PORT_SMB)

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(file_bytes)
        fp.seek(0)
        conn.storeFile(SMBService.SHARE_NAME, file_name, fp)

    with tempfile.NamedTemporaryFile() as fp:
        conn.retrieveFile(SMBService.SHARE_NAME, file_name, fp)
        fp.seek(0)
        assert(fp.read() == file_bytes)


def test_sftp_service_upload_success(helper_functions):
    file_name = helper_functions.generate_random_filename()
    file_bytes = helper_functions.generate_random_filebytes()

    transport = paramiko.Transport((TEST_ADDRESS, DEFAULT_PORT_SFTP))
    transport.connect(None, "", "")
    sftp = paramiko.SFTPClient.from_transport(transport)

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(file_bytes)
        fp.seek(0)
        sftp.putfo(fp, file_name)

    with tempfile.NamedTemporaryFile() as fp:
        sftp.getfo(file_name, fp)
        fp.seek(0)
        assert(fp.read() == file_bytes)
