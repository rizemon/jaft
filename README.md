# `jaft`: Jack of All File Transfers!

With `jaft`, you can instantly share a specific directory via multiple protocols commonly used for file transfers.

## Protocols supported

* `HTTP`
* `FTP`
* `SFTP`
* `SMB`
* `NC` (Netcat)

## Features

* Shares the specified directory via the above protocols concurrently.
* Supports both upload and download operations.
* Anonymous access (Enter any username/password and you are in!)

## Installation

### Requirements
* Linux
* Python3
* Poetry (For package management)
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

3. Generate an SSH Key pair:
```bash
$ ssh-keygen -f ./id_rsa -q -N ''
```

4. Start `jaft`:
```bash
$ poetry run jaft . 0.0.0.0
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
