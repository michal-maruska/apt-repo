# reprepro -- debian repository

This is used on top of Debian-Sid.
Some packages are just patched, some are original code.
The patched ones have a version containing "maruska".

Sources can be found on my other [github repositories](https://github.com/MichalMaruska?tab=repositories).


## How to start:


Read https://wiki.debian.org/DebianRepository/UseThirdParty to assess risks.
Packages are signed by my gpg key, so cannot be tempered with once uploaded on github.

Get the public key
```shell
wget https://michalmaruska.github.io/maruska.asc && sudo mv maruska.asc /etc/apt/trusted.gpg.d/
```
and modify sources.list:
```shell
wget https://michalmaruska.github.io/maruska-server.sources && sudo mv maruska-server.sources /etc/apt/sources.list.d/
```

And use it:
```shell
apt update
apt install maruska-top-base
```

The "apt" in there is patched to possibly prevent upgrading "maruska" versions to one without the string.
In that case `apt -o 'APt::Install::Protect-Maruska=false'` will allow it, if needed.
