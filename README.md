# bitssh

[![GitHub issues](https://img.shields.io/github/issues/Mr-Sunglasses/bitssh)](https://github.com/Mr-Sunglasses/bitssh)
[![GitHub forks](https://img.shields.io/github/forks/Mr-Sunglasses/bitssh)](https://github.com/Mr-Sunglasses/bitssh/network)
[![GitHub stars](https://img.shields.io/github/stars/Mr-Sunglasses/bitssh)](https://github.com/Mr-Sunglasses/bitssh)
[![GitHub license](https://img.shields.io/github/license/Mr-Sunglasses/bitssh)](https://github.com/Mr-Sunglasses/bitssh/blob/main/LICENSE)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) ![contributions welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3&style=flat-square) ![GitHub contributors](https://img.shields.io/github/contributors-anon/Mr-Sunglasses/bitssh)

A New and Modern SSH connector written in Python.

Terminal user interface for SSH. It uses `~/.ssh/config` to list and connect to hosts.

<p align="center">
    <img src="https://i.ibb.co/5Wm4PNh/bitssh-logo.png" width="320" height="220">
</p>

## Demo

<a href="https://asciinema.org/a/722363" target="_blank"><img src="https://asciinema.org/a/722363.svg" /></a>

## Installation

Install bitssh with docker

```bash

  docker run --rm -it -v ~/.ssh:/root/.ssh mrsunglasses/bitssh:latest	

```

Install bitssh with uv (recommended)
```
  uv tool install bitssh
```

Install bitssh with pip

```bash
  pip3 install bitssh

  bitssh
```

Install from source

```bash
  git clone https://github.com/Mr-Sunglasses/bitssh

  cd bitssh

  python3 -m pip3 install -e .

  bitssh
```

## Usage

### Connecting to a Host

Simply run bitssh to see all your SSH hosts and connect to one:

```bash
bitssh
```

This displays a table of all hosts from `~/.ssh/config` and launches a fuzzy search prompt to select a host. Once selected, bitssh opens an SSH connection to that host.

### Check Version

```bash
bitssh -v
bitssh --version
```

### Adding a Host

**Interactive mode** (guided prompts):

```bash
bitssh add
```

**Non-interactive mode** (CLI flags):

```bash
bitssh add --host myserver --hostname 192.168.1.1
bitssh add --host myserver --hostname 192.168.1.1 --user root --port 2222
bitssh add --host myserver --hostname 192.168.1.1 --user admin --identity-file ~/.ssh/id_rsa
```

| Flag | Description |
|---|---|
| `--host` | Alias for the SSH connection (required) |
| `--hostname` | IP address or domain (required) |
| `--user` | Login username |
| `--port` | SSH port (default: 22) |
| `--identity-file` | Path to private key file |

### Removing a Host

**Interactive mode** (multi-select prompt):

```bash
bitssh remove
```

**Non-interactive mode** (specify one or more hosts):

```bash
bitssh remove --host myserver
bitssh remove --host srv1 srv2
```

### SSH Config Reference

bitssh reads hosts from `~/.ssh/config`. Example configuration:

```ssh-config
Host myserver
    Hostname 192.168.1.1
    User admin
    Port 22

Host production
    Hostname ec2-xxx-xxx-xxx-xxx.compute-1.amazonaws.com
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/aws-key.pem
```

See the [OpenBSD `ssh_config` reference](https://man.openbsd.org/ssh_config.5) for all available options.

## Troubleshooting

``` [...]/.ssh/config: no such file or directory ```

- Check if you have `~/.ssh/config` file
- If you don't, create it with `touch ~/.ssh/config`

Here's a sample `~/.ssh/config` file that is recognized by bitssh:

```bash
Host abc
	Hostname xxx.xx.xx.xx
	User test1
	port 22

Host pqr
	Hostname ec2-xxx-xxx-xxx-xxx.compute-1.amazonaws.com
	User ubuntu
	port 22

Host wxy
	Hostname xxx.xx.xxx.xx
	User test2
	port 22
```

You can check the [OpenBSD `ssh_config` reference](https://man.openbsd.org/ssh_config.5) for more information on how to setup `~/.ssh/config`.

## Documentation

[Documentation](docs/docs.md)

## Contributing

Contributions are always welcome!

See [CONTRIBUTING.md](./CONTRIBUTING.md) for ways to get started.

Please adhere to this project's [code of conduct](./CODE_OF_CONDUCT.md).

## Authors

- [@Mr-Sunglasses](https://www.github.com/Mr-Sunglasses)

## License

[MIT](https://choosealicense.com/licenses/mit/)

## 💪 Thanks to all Wonderful Contributors

Thanks a lot for spending your time helping bitssh grow.
Thanks a lot! Keep rocking 🍻

[![Contributors](https://contrib.rocks/image?repo=Mr-Sunglasses/bitssh)](https://github.com/Mr-Sunglasses/bitssh/graphs/contributors)

## 🙏 Support++

This project needs your shiny star ⭐.
Don't forget to leave a star ⭐️

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
