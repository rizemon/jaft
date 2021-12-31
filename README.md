# `jaft`: Jack of All File Transfers!

With `jaft`, you can instantly share a specific directory via multiple protocols commonly used for file transfers.


```
usage: jaft [-h] [-d [DIR]] [-l [LHOST]] [-k [KEY]] [--http HTTP_PORT]
            [--sftp SFTP_PORT] [--ftp FTP_PORT] [--smb SMB_PORT] [--nc NC_PORT]

jaft: Jack of All File Transfers

optional arguments:
  -h, --help            show this help message and exit
  -d [DIR], --dir [DIR]
                        Directory to serve files from. Default: . (Current working
                        directory)
  -l [LHOST], --lhost [LHOST]
                        IP address to serve from. Default: 0.0.0.0 (All interfaces)
  -k [KEY], --key [KEY]
                        Private key used for SFTP.
  --http HTTP_PORT      Port number used for HTTP. Default: 8000
  --sftp SFTP_PORT      Port number used for SFTP. Default: 2222
  --ftp FTP_PORT        Port number used for FTP. Default: 2121
  --smb SMB_PORT        Port number used for SMB. Default: 4455
  --nc NC_PORT          Port number used for NC. Default: 4444
```

## Protocols supported

* `HTTP`
* `FTP`
* `SFTP`
* `SMB`
* `NC` (Netcat)

## Features

* Shares the specified directory via the above supported protocols **concurrently**.
* Supports both upload and download operations.
* Anonymous access (Enter any username/password and you are in!)

## Installation

### Requirements
* Linux
* Python3
* Poetry (For dependency management)
* Git (To retrieve the repo)

### Steps

1. Download a copy of this repository:
```bash
$ git clone https://github.com/rizemon/jaft
```

2. Install the required dependencies:
```bash
$ cd jaft
$ poetry install
```

3. Generate an unencrypted SSH Key pair using `ssh-keygen`:
```bash
$ ssh-keygen -f ./id_rsa -q -N ''
```

4. Start `jaft`:
```bash
$ poetry run jaft . 0.0.0.0 ./id_rsa
```

## Testing

### Steps (Using `poetry`)

1. Download a copy of this repository:
```bash
$ git clone https://github.com/rizemon/jaft
```

2. Install the required dependencies:
```bash
$ cd jaft
$ poetry install --no-dev
```

3. Generate an SSH Key pair:
```bash
$ ssh-keygen -f ./id_rsa -q -N ''
```

4. Execute tests:
```bash
$ poetry run pytest 
```

### Steps (Using `act`)

1. Download a copy of this repository:
```bash
$ git clone https://github.com/rizemon/jaft
```

2. Execute `act` to test the Github Action workflow:
```bash
$ cd jaft
$ act
```

## Why `jaft`?

When I was preparing myself for the OSCP (Offensive Security Certified Professional Exam), transferring files from my host machine to a target was a chore to me. My go-to would always be to start a HTTP server using `http.server` or [`updog`](https://github.com/sc0tfree/updog) that will serve the contents of a given directory of attacker tools and then use `curl` (For Linux) or `certutil` (For Windows) from the target machine to retrieve them. However, this might not always go so well as the target might not have these programs installed (e.g Docker containers) or perhaps not even allow for outbound HTTP connections (e.g Firewall rules). 

Therefore, I created `jaft` that is able to readily share my directory of attacker tools on protocols that I normally use for file transfers so that I would not have to repetitively startup and manage various file services.
