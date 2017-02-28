# How to build

Compile using mock:

```
wget http://downloads.asterisk.org/pub/telephony/dahdi-linux/dahdi-linux-2.11.1.tar.gz

mock --resultdir=. -r nethserver-7-x86_64 -D 'dist .ns7' -D 'version 2.11.1' -D 'release 3.10.0_514.el7' --buildsrpm --spec dahdi-linux-kmod.spec --sources .

mock --resultdir=. -r nethserver-7-x86_64 -D 'dist .ns7' -D 'version 2.11.1' -D 'release 3.10.0_514.el7'  dahdi-linux-kmod-2.11.1-3.10.0_514.el7.ns7.src.rpm
```
