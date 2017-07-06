%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%global gitdate 20170703
%global commit0 0c10102578e7c762674eaf9460b0903d76f151db
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}


Name:          	i-nex
Version:       	7.6.0
Release: 	1%{?gver}%{dist}
Summary:      	System information tool like hardinfo, sysinfo
Source0: 	https://github.com/i-nex/I-Nex/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source3:	i-nex.desktop
URL:           	https://github.com/eloaders/I-Nex
Group:        	System/X11/Utilities
License:        GPLv3, LGPLv3
BuildRoot:     	%{_tmppath}/build-%{name}-%{version}
 
BuildRequires: 	gambas3-devel 
BuildRequires:  ImageMagick 
BuildRequires:  ImageMagick-devel 
BuildRequires:  git	
BuildRequires:  gcc-c++ 
BuildRequires:  autoconf 
BuildRequires:  make 
BuildRequires:  redhat-lsb 
BuildRequires:  automake 
BuildRequires:  gambas3-gb-image 
BuildRequires:	gambas3-gb-qt5
BuildRequires:  gambas3-gb-form 
BuildRequires:  gambas3-gb-desktop 
BuildRequires:  gambas3-gb-form-dialog >= 3.5.0
BuildRequires:	gambas3-gb-form-stock 
BuildRequires:	gambas3-gb-gui >= 3.5.0
BuildRequires:  gambas3-gb-qt5-ext >= 3.5.0
BuildRequires:	gambas3-gb-settings
BuildRequires:  hicolor-icon-theme 
BuildRequires:  pkgconfig
BuildRequires:  libcpuid-devel >= 0.2.1
BuildRequires:  pkgconfig(libprocps)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pciutils
BuildRequires:  procps
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
#-------------------------------------
Requires:	gambas3-gb-gtk 
Requires:	gambas3-gb-desktop 
Requires:	gambas3-gb-settings 
Requires:	gambas3-gb-form-dialog 
Requires:  	gambas3-gb-qt5 >= 3.5.0
Requires:  	gambas3-gb-qt5-ext >= 3.5.0
Requires:	gambas3-gb-form-mdi 
Requires:	gambas3-gb-form-stock 
Requires:	redhat-lsb 
Requires:	mesa-demos 
Requires:	xorg-x11-server-utils
Requires:       gambas3-gb-dbus 
Requires:	gambas3-runtime 
Requires:	gambas3-gb-image 
Requires:	gambas3-gb-gtk 
Requires:	gambas3-gb-form 
Requires:	util-linux 
Requires:	procps-ng 
Requires:	coreutils 
Requires:	pciutils
Requires:	libcpuid
Requires:	gambas3-runtime
Requires:       gambas3-gb-gui >= 3.5.0
Requires:	hicolor-icon-theme
Requires:  	net-tools
Requires:	python-configobj
Requires:	procps-ng
Requires:	pastebinit
Requires:	procps-ng

%description
i-nex - System information tool like hardinfo, sysinfo.
I-Nex is an application that gathers information for hardware 
components available on your system and displays it using an 
user interface similar to the popular Windows tool CPU-Z.

I-Nex can display information for the following components: CPU, 
GPU, Motherboard, Sound, Hard disks, RAM, Network and USB as well 
as some system info like the hostname, Linux distribution and 
version, Xorg, GCC, GLX versions and Linux Kernel info.


%prep

%autosetup -n I-Nex-%{commit0}
# sed -i 's|python3$|python2|' pastebinit
  # make it dynamic
  sed -i -e 's|^STATIC.*|STATIC = false|' i-nex.mk
  sed -i -e 's|^UDEV_RULES_DIR.*|UDEV_RULES_DIR = /usr/lib/udev/rules.d|' i-nex.mk
 
# A hack to be able to run the program via the name execution. Thanks openSuse!
#+ some info tools are under *sbin
cat > %{name}.sh <<HERE
#!/bin/sh

export LIBOVERLAY_SCROLLBAR=0 PATH=/sbin:/usr/sbin:\$PATH
exec %{_bindir}/%{name}.gambas
HERE

#using system's pastebinit
%__sed -i \
       '\|/usr/share/i-nex/pastebinit/|s|/usr/share/i-nex/pastebinit/||' \
       I-Nex/i-nex/.src/Reports/MPastebinit.module
%__cp I-Nex/i-nex/logo/i-nex.0.4.x.png $RPM_SOURCE_DIR/%{name}.png
%{__sed} -e 's|env LIBOVERLAY_SCROLLBAR=0 /usr/bin/i-nex.gambas|i-nex|' \
         -e '/^Icon=/s|=.*|=%{name}|' debian/%{name}.desktop > %{name}.desktop


%build
cd I-Nex
autoreconf -fiv
%configure
cd ..
make V=1 %{?_smp_mflags}

%install

make V=1 DESTDIR=%{buildroot} install

# A hack to be able to run the program via the name execution.
%{__install} -D -m 755 %{name}.sh %{buildroot}%{_bindir}/%{name}

# Let's use %%doc macro.
rm -rf %{buildroot}%{_datadir}/doc/%{name}

# Let's use system's `pastebinit`.
rm -rf %{buildroot}%{_datadir}/%{name}/pastebinit

%fdupes -s %{buildroot}%{_datadir}

%files
%{_bindir}/i-nex
%{_bindir}/i-nex.gambas
%{_bindir}/i-nex-edid
%{_datadir}/applications/i-nex.desktop
/usr/lib/udev/rules.d/i2c_smbus.rules
%{_datadir}/applications/i-nex-library.desktop
%{_mandir}/man1/i-nex.1.gz
%{_mandir}/man1/i-nex.gambas.1.gz
%{_mandir}/man1/i-nex-edid.1.gz
%{_datadir}/pixmaps/i-nex-16.png
%{_datadir}/pixmaps/i-nex-32.png
%{_datadir}/pixmaps/i-nex-128.png
%{_datadir}/pixmaps/i-nex.png

%changelog

* Mon Jul 03 2017 David Vasquez <davidjeremias82 at gmail dot com> - 7.6.0-2.git0c10102
- Updated to 7.6.0-2.git0c10102

* Wed Jan 11 2017 David Vasquez <davidjeremias82 at gmail dot com> - 7.6.0-1.git32e7049
- Updated to 7.6.0-20170111git32e7049

* Thu Apr 28 2016 David Vasquez <davidjeremias82 at gmail dot com> - 7.4.0-2.git7345b26
- Rebuilt 

* Tue Apr 14 2015 David Vasquez <davidjeremias82 at gmail dot com> - 7.4.0-1.git7345b26
- Updated to 7.4.0-20150414-7345b26 some fixes thanks to Darkness

* Fri Jun 06 2014 David Vasquez <davidjeremias82 at gmail dot com> - 0.6.2-3
- Repacking

* Wed Feb 19 2014 David Vasquez <davidjeremias82 at gmail dot com> - 0.6.2-2
-Updated to 0.6.2
-Patch thanks DA (darkness) 

* Mon Dec 30 2013 David Vasquez <davidjeremias82 at gmail dot com> - 0.6.0-1
-Initial build rpm
