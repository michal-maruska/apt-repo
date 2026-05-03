# reprepro -- debian repository

This contains packages built for Debian-Sid/Unstable.
Some packages are just patched, some are original code.

The _patched_ ones have a version containing "maruska".

Here the [published repository](https://michal-maruska.github.io/apt-repo/)

Sources can be found on my other [github repositories](https://github.com/michal-maruska?tab=repositories).


## How to start:


Read https://wiki.debian.org/DebianRepository/UseThirdParty to assess risks.
Packages are signed by my gpg key, so cannot be tempered with once uploaded on github.

Get the public key
```shell
wget https://michal-maruska.github.io/apt-repo/maruska.asc && sudo mv maruska.asc /etc/apt/trusted.gpg.d/
```
and modify sources.list:
```shell
wget https://michal-maruska.github.io/apt-repo/maruska-server.sources && sudo mv maruska-server.sources /etc/apt/sources.list.d/
```

And use it:
```shell
apt update
apt install maruska-top-base
```

The "apt" in there is patched to possibly prevent upgrading "maruska" versions to one without the string.
In that case `apt -o 'APt::Install::Protect-Maruska=false'` will allow it, if needed.

## How it is built:

* there is a [**docker** image](https://github.com/michal-maruska/workflows/) for building in debian-sid,
with access to these packages, as there are dependencies.
* **component** repositories use a shared GH workflow, to build (using that docker image), and in the end trigger ...
* this repo has the configuration and a GH workflow to import the GH Release artifacts of other **component** builds


