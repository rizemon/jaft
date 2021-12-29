from multiprocessing import Process

from jaft.servers import FTPService, HTTPService, NCService, SFTPService, \
    SMBService

DEFAULT_ADDRESS = '0.0.0.0'
DEFAULT_PORT_FTP = 21
DEFAULT_PORT_SFTP = 22
DEFAULT_PORT_SMB = 445
DEFAULT_PORT_HTTP = 80
DEFAULT_PORT_NC = 4444
DEFAULT_DIRECTORY = '.'


class JAFT:

    def __init__(
        self,
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
            directory
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
    jaft = JAFT()
    try:
        jaft.run()
    except KeyboardInterrupt:
        jaft.stop()


if __name__ == '__main__':
    main()
