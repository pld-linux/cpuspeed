Summary:	CPU Frequency adjusting daemon.
Name:		cpuspeed
Version:	1.2.1
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://carlthompson.net/dl/cpuspeed/cpuspeed-%{version}.tar.gz
# Source0-md5:	430bed9513bd69d9d864cda5951c2af4
Source1:	cpuspeed.init
Patch0:		%{name}-warning.diff
Patch1:		%{name}-idlenice.diff
Patch2:		%{name}-nostrip.diff
URL:		http://carlthompson.net/Software/CPUSpeed/
BuildRequires:	gcc-c++
Requires(post,preun): /sbin/chkconfig
ExclusiveArch:	%{ix86} %{x8664} ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cpuspeed is a daemon that dynamically changes the speed
of your processor(s) depending upon its current workload
if it is capable (needs Intel Speedstep, AMD PowerNow!,
or similar support).

%prep
%setup -q 
%patch0 -p1
%patch1 -p2
%patch2 -p1

%build
%{__make}

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
if [ -f /var/lock/subsys/cpuspeed ]; then
    /etc/rc.d/init.d/cpuspeed restart 1>&2
else 
    echo "Run \"/etc/rc.d/init.d/cpuspeed start\" to start cpuspeed daemon."
fi

%preun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/cpuspeed ]; then
	/etc/rc.d/init.d/cpuspeed stop 1>&2
    fi
    [ ! -x /sbin/chkconfig ] || /sbin/chkconfig --del cpuspeed
fi

%files
%defattr(644,root,root,755)
%doc CHANGES EXAMPLES FEATURES README TODO USAGE
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/sysconfig/*
%attr(754,root,root) /etc/rc.d/init.d/*
