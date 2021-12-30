from argparse import ArgumentParser
from multiprocessing import Process

from jaft.servers import (FTPService, HTTPService, NCService, SFTPService,
                          SMBService)

DEFAULT_ADDRESS = '0.0.0.0'
DEFAULT_PORT_FTP = 2121
DEFAULT_PORT_SFTP = 2222
DEFAULT_PORT_SMB = 4455
DEFAULT_PORT_HTTP = 8000
DEFAULT_PORT_NC = 4444
DEFAULT_DIRECTORY = '.'


class JAFT:

    def __init__(
        self,
        priv_key_path,
        address=DEFAULT_ADDRESS,
        directory=DEFAULT_DIRECTORY,
        ftp_port=DEFAULT_PORT_FTP,
        sftp_port=DEFAULT_PORT_SFTP,
        smb_port=DEFAULT_PORT_SMB,
        http_port=DEFAULT_PORT_HTTP,
        nc_port=DEFAULT_PORT_NC
    ):
        ftp = FTPService(
            address,
            ftp_port,
            directory
        )
        http = HTTPService(
            address,
            http_port,
            directory
        )
        smb = SMBService(
            address,
            smb_port,
            directory
        )
        sftp = SFTPService(
            address,
            sftp_port,
            directory,
            priv_key_path
        )
        nc = NCService(
            address,
            nc_port,
            directory
        )

        self.processes = [
            Process(target=ftp.start),
            Process(target=http.start),
            Process(target=smb.start),
            Process(target=sftp.start),
            Process(target=nc.start)
        ]

    def run(self):
        for p in self.processes:
            p.daemon = True
            p.start()
        for p in self.processes:
            p.join()

    def stop(self):
        for p in self.processes:
            p.terminate()


def main():
    parser = ArgumentParser(
        add_help=True,
        description='jaft: Jack of All File Transfers'
    )

    parser.add_argument(
        'directory',
        action='store',
        type=str,
        default=DEFAULT_DIRECTORY,
        help='Directory to serve files \
from. Default: %(default)s (Current working directory)'
    )

    parser.add_argument(
        'lhost',
        action='store',
        type=str,
        default='0.0.0.0',
        help='IP address to serve from. Default: %(default)s (All interfaces)'
    )

    parser.add_argument(
        'privkey',
        action='store',
        type=str,
        help='Private key used for SFTP.'
    )

    parser.add_argument(
        '--http',
        action='store',
        type=int,
        default=DEFAULT_PORT_HTTP, metavar='HTTP_PORT', help='Port number \
used for HTTP. Default: %(default)s'
    )

    parser.add_argument(
        '--sftp',
        action='store',
        type=int,
        default=DEFAULT_PORT_SFTP, metavar='SFTP_PORT', help='Port number \
used for SFTP. Default: %(default)s'
    )

    parser.add_argument(
        '--ftp',
        action='store',
        type=int,
        default=DEFAULT_PORT_FTP, metavar='FTP_PORT', help='Port number \
used for FTP. Default: %(default)s'
    )

    parser.add_argument(
        '--smb',
        action='store',
        type=int,
        default=DEFAULT_PORT_SMB, metavar='SMB_PORT', help='Port number \
used for SMB. Default: %(default)s'
    )

    parser.add_argument(
        '--nc',
        action='store',
        type=int,
        default=DEFAULT_PORT_NC, metavar='NC_PORT', help='Port number \
used for NC. Default: %(default)s'
    )

    args = parser.parse_args()

    if not args:
        parser.print_help()
        return

    jaft = JAFT(
        priv_key_path=args.privkey,
        directory=args.directory,
        address=args.lhost,
        ftp_port=args.ftp,
        http_port=args.http,
        smb_port=args.smb,
        sftp_port=args.sftp,
        nc_port=args.nc
    )
    try:
        jaft.run()
    except KeyboardInterrupt:
        jaft.stop()


if __name__ == '__main__':
    main()
