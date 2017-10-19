%define   kmodtool bash /usr/lib/rpm/redhat/kmodtool
%{!?kversion: %define kversion 3.10.0-693.el7}

%define kmod_name dahdi-linux
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""

%{!?kvariants: %define kvariants %{?upvar} %{?smpvar}}

Summary: The DAHDI project
Name: dahdi-linux-kmod
Version: %{version}
Release: %{release}%{dist}
License: GPL
Group: Utilities/System
Source: dahdi-linux-%{version}.tar.gz
Source1: GpakDsp.fw
Source2: GpakDsp0708.fw
Source3: rcbfx.fw
Source4: GpakDsp10.fw
Source5: DspLoader.fw
Source6: GpakDsp0704.fw
Source7: modules-load.conf
Source10: kmodtool-dahdi-el7.sh
Patch0: dahdi-no-fwload.diff
Patch4: 0001-rhino.patch
Patch7: install_mod_dir.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.asterisk.org/
Vendor: Digium, Inc.
Packager: Bryan Walters <bwalters@sangoma.com>
Requires: dahdi-linux = %{version}
BuildRequires: kernel = %(echo %{kverrel} | sed -e 's/\(.*\)\.[^\.]*$/\1/')
BuildRequires: redhat-rpm-config
BuildRequires: wget
BuildRequires: kabi-yum-plugins
Requires: dahdi-linux = %{version}
BuildRequires: kernel-devel = %(echo %{kverrel} | sed -e 's/\(.*\)\.[^\.]*$/\1/')

%description
The open source DAHDI project

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

%prep
%setup -c -n %{kmod_name}-%{version}

cd %{kmod_name}-%{version}/

%patch0 -p0
%patch4 -p1
%patch7 -p0

echo %{version} > .version
cd ../
for kvariant in %{kvariants} ; do
    cp -a %{kmod_name}-%{version} _kmod_build_$kvariant
done

mkdir -p _kmod_build_/drivers/dahdi/rhino/r1t1/ _kmod_build_/drivers/dahdi/rhino/rxt1/ _kmod_build_/drivers/dahdi/rhino/rcbfx/
cp %SOURCE1 _kmod_build_/drivers/dahdi/rhino/r1t1/
cp %SOURCE1 _kmod_build_/drivers/dahdi/rhino/rxt1/
cp %SOURCE2 _kmod_build_/drivers/dahdi/rhino/rcbfx/
cp %SOURCE3 _kmod_build_/drivers/dahdi/rhino/rcbfx/
cp %SOURCE4 _kmod_build_/drivers/dahdi/rhino/rcbfx/
cp %SOURCE5 _kmod_build_/drivers/dahdi/rhino/rcbfx/
cp %SOURCE6 _kmod_build_/drivers/dahdi/rhino/rcbfx/

find . -name make_firmware_object | xargs chmod +x

cd %{kmod_name}-%{version}
chmod +x drivers/dahdi/rhino/r1t1/make_firmware_object
chmod +x drivers/dahdi/rhino/rxt1/make_firmware_object
chmod +x drivers/dahdi/rhino/rcbfx/make_firmware_object

%build
for kvariant in %{kvariants}
do
    pushd _kmod_build_$kvariant
    make KVERS="%{kverrel}${kvariant}" modules
    popd
done

%install
for kvariant in %{kvariants}
do
    pushd _kmod_build_$kvariant
    make DESTDIR=$RPM_BUILD_ROOT KVERS="%{kverrel}${kvariant}" install-modules
    popd
done
mkdir -p %{buildroot}/etc/modules-load.d
mv %{S:7} %{buildroot}/etc/modules-load.d/kmod-dahdi-linux.conf

%clean
cd $RPM_BUILD_DIR
%{__rm} -rf %{kmod_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT
