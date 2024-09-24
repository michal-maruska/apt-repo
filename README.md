# reprepro -- debian repository of customized packages


some packages are just patched, some are original code

sources can be found on my other github repositories


how to start:
Get the public key, and sources.list:

wget https://michalmaruska.github.io/maruska.asc && sudo mv maruska.asc /etc/apt/trusted.gpg.d/

tee /etc/apt/sources.list.d/maruska-sid.list
deb [signed-by=/etc/apt/trusted.gpg.d/maruska.asc] https://michalmaruska.github.io/ sid main
C^d

tee /etc/apt/sources.list.d/maruska-release.list
deb [signed-by=/etc/apt/trusted.gpg.d/maruska.asc] https://michalmaruska.github.io/ release main
C^d


apt update

apt install maruska-top-base
