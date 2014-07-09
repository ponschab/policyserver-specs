%define confdir %{_sysconfdir}/postfix

Summary: Postfix Greylisting Policy Server
Name: postgrey
Version: 1.34
Release: 1%{?dist}
# File headers only state "GNU GPL", but the LICENSE sections state v2 and "any
# later version"
License: GPLv2+
Group: System Environment/Daemons
URL: http://postgrey.schweikert.ch/
Source0: http://postgrey.schweikert.ch/pub/postgrey-%{version}.tar.gz
Source1: postgrey.init
Source2: README-rpm
Patch0: postgrey-1.28-group.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# We require postfix for its directories and gid
Requires: postfix
Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service
BuildArch: noarch

%description
Postgrey is a Postfix policy server implementing greylisting.  When a request
for delivery of a mail is received by Postfix via SMTP, the triplet CLIENT_IP /
SENDER / RECIPIENT is built.  If it is the first time that this triplet is
seen, or if the triplet was first seen less than 5 minutes, then the mail gets
rejected with a temporary error. Hopefully spammers or viruses will not try
again later, as it is however required per RFC.


%prep
%setup -q
%patch0 -p1 -b .group
install -p -m 0644 %{SOURCE2} README-rpm


%build
# We only have perl scripts, so just "build" the man page
pod2man \
    --center="Postgrey Policy Server for Postfix" \
    --section="8" \
    postgrey > postgrey.8


%install
rm -rf %{buildroot}

# Configuration files
mkdir -p %{buildroot}%{confdir}
install -p -m 0644 postgrey_whitelist_{clients,recipients} \
    %{buildroot}%{confdir}/
# Local whitelist file
echo "# Clients that should not be greylisted.  See postgrey(8)." \
    > %{buildroot}%{confdir}/postgrey_whitelist_clients.local

# Main script
install -D -p -m 0755 postgrey %{buildroot}%{_sbindir}/postgrey

# Spool directory
mkdir -p %{buildroot}%{_var}/spool/postfix/postgrey

# Init script
install -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/rc.d/init.d/postgrey

# Man page
install -D -p -m 0644 postgrey.8 \
    %{buildroot}%{_mandir}/man8/postgrey.8

# Optional report script
install -D -p -m 0755 contrib/postgreyreport \
    %{buildroot}%{_sbindir}/postgreyreport


%clean
rm -rf %{buildroot}


%pre
/usr/sbin/useradd -d %{_var}/spool/postfix/postgrey -s /sbin/nologin \
    -M -r postgrey &>/dev/null || :

%post
/sbin/chkconfig --add postgrey

%preun
if [ $1 -eq 0 ]; then
    /sbin/service postgrey stop &>/dev/null || :
    /sbin/chkconfig --del postgrey
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service postgrey condrestart &>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc Changes COPYING README README-rpm
%{_sysconfdir}/rc.d/init.d/postgrey
%config(noreplace) %{confdir}/postgrey_whitelist_clients
%config(noreplace) %{confdir}/postgrey_whitelist_recipients
%config(noreplace) %{confdir}/postgrey_whitelist_clients.local
%{_sbindir}/postgrey
%{_sbindir}/postgreyreport
%{_mandir}/man8/postgrey.8*
%dir %attr(0751,postgrey,postfix) %{_var}/spool/postfix/postgrey/


%changelog
* Tue Jun  7 2011 Matthias Saou <matthias@saou.eu> 1.34-1
- Update to 1.34.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <matthias@saou.eu> 1.32-1
- Update to 1.32.
- Update init script to the new style.
- Slightly update README-rpm instructions.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Matthias Saou <matthias@saou.eu> 1.31-1
- Update to 1.31.

* Mon Aug  6 2007 Matthias Saou <matthias@saou.eu> 1.30-1
- Update to 1.30.
- Update License field.

* Fri Jun 22 2007 Matthias Saou <matthias@saou.eu> 1.28-1
- Update to 1.28.
- Update URL to the new homepage.

* Mon Feb 12 2007 Matthias Saou <matthias@saou.eu> 1.27-4
- Silence %%setup.
- Fix init script mode in the srpm.
- Remove explicit perl(IO::Multiplex) requirement, not needed on FC6 (but
  probably still on RHEL4).
- Add a comment line to the empty local whitelist file.

* Mon Dec  4 2006 Matthias Saou <matthias@saou.eu> 1.27-3
- Add man page generation (Mike Wohlgemuth).

* Fri Dec  1 2006 Matthias Saou <matthias@saou.eu> 1.27-2
- Include postgreyreport script.

* Mon Nov  6 2006 Matthias Saou <matthias@saou.eu> 1.27-1
- Spec file cleanup.

* Wed Jan 18 2006 Levente Farkas <lfarkas@lfarkas.org> 1.24
- some minor changes thanks to Peter Bieringer <pb@bieringer.de>

* Mon Jan 16 2006 Levente Farkas <lfarkas@lfarkas.org> 1.24
- upgrade to 1.24

* Sun Nov 13 2005 Levente Farkas <lfarkas@lfarkas.org> 1.22
- upgrade to 1.22

* Mon Aug 22 2005 Levente Farkas <lfarkas@lfarkas.org> 1.21
- spec file update from Luigi Iotti <luigi@iotti.biz>

* Thu Apr 28 2005 Levente Farkas <lfarkas@lfarkas.org> 1.21
- update to 1.21

* Tue Mar  8 2005 Levente Farkas <lfarkas@lfarkas.org> 1.18
- update to 1.18

* Tue Dec 14 2004 Levente Farkas <lfarkas@lfarkas.org> 1.17
- update to 1.17

* Wed Jul 14 2004 Levente Farkas <lfarkas@lfarkas.org> 1.14
- guard the pre and post scripts

* Wed Jul  7 2004 Levente Farkas <lfarkas@lfarkas.org> 1.13
- initial release 1.13

