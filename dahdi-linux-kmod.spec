%define   kmodtool bash /usr/lib/rpm/redhat/kmodtool
%{!?kversion: %define kversion 3.10.0-327.el7}

%define kmod_name dahdi-linux
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%if "%{distname}" == "sles"
%define upvar -default
%else
%define upvar ""
%endif

%if "%{distname}" == "sles"
%define smpvar -smp -bigsmp
%else
%endif

%if "%{distname}" == "sles"
%ifarch i586 i686
%define xenvar -xen -xenpae
%endif
%ifarch x86_64 ia64
%define xenvar -xen
%endif
%else
%ifarch i686 x86_64 ia64
%define xenvar xen
%endif

%ifarch i686
%define paevar PAE
%endif
%endif

%{!?kvariants: %define kvariants %{?upvar} %{?smpvar}}

#Workaround for 64 bit CPUs
%define _lib lib

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
Patch0: dahdi-no-fwload.diff
Patch1: 0001-oslec.patch
#Patch2: 0001-openvox.patch
#Patch3: 0001-allo.com.patch
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

%description
The open source DAHDI project

# magic hidden here:
# expanded 'magic'

%package       -n kmod-dahdi-linux
Summary:          dahdi-linux kernel module(s)
Group:            System Environment/Kernel
%global _use_internal_dependency_generator 0
Provides:         dahdi-linux-kmod = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   	kmod
# FIXME Replace when kernel version updates
#Provides:         kernel-modules >= %{kversion}
Requires: dahdi-linux = %{version}
BuildRequires: kernel-devel
%description   -n kmod-dahdi-linux
This package provides the dahdi-linux kernel modules built for
the Linux kernel %{kversion} for the %{_target_cpu}
family of processors.


#%post          -n kmod-dahdi-linux
#if [ -e "/boot/System.map-%{kversion}" ]; then
#    /sbin/depmod -aeF "/boot/System.map-%{kversion}" "%{kversion}" > /dev/null || :
#fi

#Only run find if we have that directory
#if [ -e "/lib/modules/%{kversion}/extra/dahdi-linux" ]; then
#  modules=( $(find /lib/modules/%{kversion}/extra/dahdi-linux | grep '\.ko$' 2>/dev/null) )
#  if [ -x "/sbin/weak-modules" ]; then
#      printf '%s\n' "${modules[@]}"     | /sbin/weak-modules --add-modules
#  fi
#fi
#%preun         -n kmod-dahdi-linux
#rpm -ql kmod-dahdi-linux-%{kmod_version}-%{kmod_release}.%{_target_cpu} | grep '\.ko$' > /var/run/rpm-kmod-dahdi-linux-modules
#%postun        -n kmod-dahdi-linux
#if [ -e "/boot/System.map-%{kversion}" ]; then
#    /sbin/depmod -aeF "/boot/System.map-%{kversion}" "%{kversion}" > /dev/null || :
#fi

#modules=( $(cat /var/run/rpm-kmod-dahdi-linux-modules) )
#rm /var/run/rpm-kmod-dahdi-linux-modules
#if [ -x "/sbin/weak-modules" ]; then
#    printf '%s\n' "${modules[@]}"     | /sbin/weak-modules --remove-modules
#fi


%files         -n kmod-dahdi-linux
%defattr(644,root,root,755)
/lib/modules/%{kversion}.%{_target_cpu}

%prep
%setup -c -n %{kmod_name}-%{version}

cd %{kmod_name}-%{version}/

%patch0 -p0
%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
%if "%{distname}" != "sles"
%patch7 -p0
%endif

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
		%if "%{distname}" == "sles"
				make KVERS="%{kverrel}${kvariant}" CONFIG_DAHDI_DYNAMIC_ETH=n modules
		%else
				make KVERS="%{kverrel}${kvariant}" modules
		%endif
		popd
done

%install
for kvariant in %{kvariants}
do
		pushd _kmod_build_$kvariant
		%if "%{distname}" == "sles"
				make DESTDIR=$RPM_BUILD_ROOT KVERS="%{kverrel}${kvariant}" CONFIG_DAHDI_DYNAMIC_ETH=n install-modules
		%else
				make DESTDIR=$RPM_BUILD_ROOT KVERS="%{kverrel}${kvariant}" install-modules
		%endif
		popd
done

%clean
cd $RPM_BUILD_DIR
%{__rm} -rf %{kmod_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT
