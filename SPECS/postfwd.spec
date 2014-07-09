Summary: Postfix policyd to combine complex restrictions in a ruleset
Name: postfwd
Version: 1.35
Release: 1%{?dist}
License: BSD
Group: System Environment/Daemons
URL: http://postfwd.org/
Source0: http://postfwd.org/postfwd-%{version}.tar.gz
Source1: postfwd.init
Source2: README.RPM
Source3: postfwd.cf
Source4: postfwd.sysconfig
Patch0: postfwd-group.patch
Patch1: postfwd2-group.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# We require postfix for its directories and gid
Requires: postfix
Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service
BuildArch: noarch

%description
Postfwd is written in perl to combine complex postfix restrictions in a 
ruleset similar to those of the most firewalls. The program uses the postfix 
policy delegation protocol to control access to the mail system before a 
message has been accepted. It allows you to choose an action (e.g. reject, dunno) 
for a combination of several smtp parameters (like sender and recipient address, 
size or the client's TLS fingerprint).

%prep
%setup -q
%patch0 -p0
%patch1 -p0
install -p -m 0644 %{SOURCE2} README.RPM


%build
# We only have perl scripts, so there's nothing to build

%install
rm -rf %{buildroot}

# Configuration files
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/postfwd.cf
install -p -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/postfwd

# Main scripts
install -D -p -m 0755 sbin/postfwd %{buildroot}%{_sbindir}/postfwd
install -D -p -m 0755 sbin/postfwd2 %{buildroot}%{_sbindir}/postfwd2

# Init script
install -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/rc.d/init.d/postfwd

# Man page
install -D -p -m 0644 man/man8/postfwd.8 \
    %{buildroot}%{_mandir}/man8/postfwd.8


%clean
rm -rf %{buildroot}

%pre
/usr/sbin/useradd -s /sbin/nologin -M -r postfwd &>/dev/null || :

%post
/sbin/chkconfig --add postfwd

%preun
if [ $1 -eq 0 ]; then
    /sbin/service postfwd stop &>/dev/null || :
    /sbin/chkconfig --del postfwd
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service postfwd condrestart &>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc plugins/postfwd.plugins.sample doc/* etc/* README.RPM
%{_sysconfdir}/rc.d/init.d/postfwd
%config(noreplace) %{_sysconfdir}/postfwd.cf
%config(noreplace) %{_sysconfdir}/sysconfig/postfwd
%{_sbindir}/postfwd
%{_sbindir}/postfwd2
%{_mandir}/man8/postfwd.8*


%changelog
* Wed Jul 09 2014 Marc Ponschab <marc@ponschab.de> - 1.35-1
- update to latest upstream version

* Sat Apr 20 2013 Marc Ponschab <marc@ponschab.de> 1.34-1
- initial release 1.34
