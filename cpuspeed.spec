Summary:	CPU Frequency adjusting daemon
Summary(pl.UTF-8):   Demon regulujący częstotliwość pracy CPU
Name:		cpuspeed
Version:	1.2.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://carlthompson.net/dl/cpuspeed/%{name}-%{version}.tar.gz
# Source0-md5:	430bed9513bd69d9d864cda5951c2af4
Source1:	%{name}.init
Patch0:		%{name}-warning.diff
Patch1:		%{name}-idlenice.diff
Patch2:		%{name}-nostrip.diff
URL:		http://carlthompson.net/Software/CPUSpeed/
BuildRequires:	gcc-c++
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
ExclusiveArch:	%{ix86} %{x8664} ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cpuspeed is a daemon that dynamically changes the speed of your
processor(s) depending upon its current workload if it is capable
(needs Intel Speedstep, AMD PowerNow!, or similar support).

%description -l pl.UTF-8
cpuspeed to demon dynamicznie zmieniający szybkość procesora(ów) w
zależności od aktualnego obciążenia - o ile procesor to obsługuje
(wymaga Intel Speedstep, AMD PowerNow! albo podobnych rozszerzeń).

%prep
%setup -q
%patch0 -p1
%patch1 -p2
%patch2 -p1

%build
%{__make} \
	CC="%{__cc} -fno-exceptions -Wall" \
	COPTS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_sbindir}}

install cpuspeed $RPM_BUILD_ROOT%{_sbindir}
install cpuspeed.conf $RPM_BUILD_ROOT/etc/sysconfig/cpuspeed
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/cpuspeed

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add cpuspeed
%service cpuspeed restart

%preun
if [ "$1" = "0" ]; then
	%service cpuspeed stop
	/sbin/chkconfig --del cpuspeed
fi

%files
%defattr(644,root,root,755)
%doc CHANGES EXAMPLES FEATURES README TODO USAGE
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(754,root,root) /etc/rc.d/init.d/*
