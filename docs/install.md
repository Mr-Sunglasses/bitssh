## Installation

Install bitssh with pip

```bash
  pip3 install bitssh

  bitssh
```

Install bitssh with uv

```bash
  uv tool install bitssh

  bitssh
```

Install bitssh from source

```bash
  git clone https://github.com/Mr-Sunglasses/bitssh

  cd bitssh

  python3 -m pip3 install -e .

  bitssh
```

## Troubleshooting

### [...]/.ssh/config: no such file or directory

- Check if you have `~/.ssh/config` file
- If you don't, create it with `touch ~/.ssh/config`

Here's a sample `~/.ssh/config` file that is recognized by bitssh:

```nginx
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

## Usage Docs

[Usage](usage.md)


## Docs Homepage

[Docs](docs.md)
