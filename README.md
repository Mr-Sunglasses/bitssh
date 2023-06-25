
# bitssh

A New and Modern SSH connector written in Python.

Terminal user interface for SSH.
It uses ```~/.ssh/config``` to list and connect to hosts.



https://github.com/Mr-Sunglasses/bitssh/assets/81439109/f3164d7e-ea61-461d-92f3-0a470dc9eb65





## Installation

Install bitssh with Python and Setup Tools

```bash
  git clone https://github.com/Mr-Sunglasses/bitssh

  cd bitssh

  python3 setup.py install

  bitssh
```

Run the Binary

```bash
  git clone https://github.com/Mr-Sunglasses/bitssh

  cd bitssh

  cd bin

  chmod +x bitssh

  ./bitssh
  
```
## Troubleshooting

## [...]/.ssh/config: no such file or directory


- Check if you have `~/.ssh/config` file
- If you don't, create it with `touch ~/.ssh/config`


Here's a sample `~/.ssh/config` file:
```nginx
Host *
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_rsa

Host "My server"
  HostName server1.example.com
  User root
  Port 22

Host "Go through Proxy"
  HostName server2.example.com
  User someone
  Port 22
  ProxyCommand ssh -W %h:%p proxy.example.com
```

You can check the [OpenBSD `ssh_config` reference](https://man.openbsd.org/ssh_config.5) for more information on how to setup `~/.ssh/config`.



## License

[MIT](https://choosealicense.com/licenses/mit/)


## Support

For support, email itskanishkp.py@gmail.com.

