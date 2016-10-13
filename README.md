# How to build

- Clone the repository

-  Download original source RPM

```
cat <<EOF > /etc/yum.repos.d/sng.repo
[sng-src]
name=SRPMs for Sanoma specific packages
baseurl=http://package1.sangoma.net/sangoma/src
gpgcheck=0
enabled=0
EOF

yumdownloader --source kmod-dahdi-linux-2.11.1-3.10.0_327.36.1.el7.24.sng7.x86_64 --enablerepo=sng-src
```

- Copy the source rpm into the cloned repo and unpack it

```
rpm2cpio dahdi-linux-kmod-2.11.1-3.10.0_327.36.1.el7.24.sng7.src.rpm | cpio -imdv
```

- Compile using mock:

```
mock --resultdir=. -r nethserver-7-x86_64 -D 'dist .ns7' -D 'version 2.11.1' -D 'release 3.10.0_327.el7' --buildsrpm --spec dahdi-linux-kmod.spec --sources .

mock --resultdir=. -r nethserver-7-x86_64 -D 'dist .ns7' -D 'version 2.11.1' -D 'release 3.10.0_327.el7'  dahdi-linux-kmod-2.11.1-3.10.0_327.el7.ns7.src.rpm
```
