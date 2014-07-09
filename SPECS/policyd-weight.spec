%define version 0.1.15_beta2

Name: policyd-weight
Version: %{version}
Release: 1
License: GPL
URL: http://www.policyd-weight.org
Group: Applications/System
Summary: Weighted Postfix SMTPD policy daemon written entirely in perl.
Source0:  %{name}-%{version}.tar.gz
Requires:  postfix, perl, perl-Net-DNS, perl-Unix-Syslog 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
policyd-weight is a Perl policy daemon for the Postfix MTA (2.1 and later) intended to eliminate forged envelope senders and HELOs (i.e. in bogus mails). It allows you to score DNSBLs (RBL/RHSBL), HELO, MAIL FROM and client IP addresses before any queuing is done. It allows you to REJECT messages which have a score higher than allowed, providing improved blocking of spam and virus mails. policyd-weight caches the most frequent client/sender combinations (SPAM as well as HAM) to reduce the number of DNS queries.

%prep
%setup -q
%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}
cp -a ${RPM_BUILD_DIR}/%{name}-%{version}/usr ${RPM_BUILD_ROOT}
cp -a ${RPM_BUILD_DIR}/%{name}-%{version}/etc ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root)
%config(noreplace) /etc/policyd-weight.conf
%attr(755,root,root) /usr/sbin/policyd-weight
%attr(755,root,root) /etc/init.d/policyd-weight
%doc documentation.txt
%doc COPYING
%doc LICENSE
%doc todo.txt
%doc changes.txt
%doc policyd-weight.conf.sample
%{_mandir}/man5/policyd-weight.conf.5.gz
%{_mandir}/man8/policyd-weight.8.gz

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre
if [ $1 = 1 ]; then
/usr/sbin/groupadd polw
/usr/sbin/useradd -r -s /sbin/nologin -g polw -c "policyd-weight daemon" polw || { echo "Could not create user 'polw'... exiting"; exit 0; }
fi

%post
if [ $1 = 1 ]; then
if [ -f /sbin/chkconfig ]; then
/sbin/chkconfig --add policyd-weight
elif [ -f %{_libdir}/lsb/install_initd ]; then
%{_libdir}/lsb/install_initd /etc/init.d/policyd-weight
fi
fi

cat << EOF

Please read the man page for suggested configuration: policyd-weight(8)
EOF

%preun
if [ $1 = 0 ]; then
if [ -f /sbin/chkconfig ]; then
/etc/init.d/policyd-weight stopall
/sbin/chkconfig --del policyd-weight
elif [ -f %{_libdir}/lsb/remove_initd ]; then
%{_libdir}/lsb/remove_initd /etc/init.d/policyd-weight
fi
fi

if [ $1 = 1 ]; then
/etc/init.d/policyd-weight stopall
fi

%postun
if [ $1 = 0 ]; then
/usr/sbin/userdel polw || { echo "Could not delete user 'polw'... please clean up manually"; exit 0; }
/usr/sbin/groupdel polw
fi

if [ $1 = 1 ]; then
/etc/init.d/policyd-weight start
fi

%changelog
* Wed Apr 03 2013 Marc Ponschab <marc@ponschab.de>
- (0.1.15_beta2)	Upgrade to latest upstream release. 
* Sat Jul 18 2009 Morgan Weetman <morganweetman@users.sourceforge.net>
- (0.1.15dev3-1)	Packaging of dev build, see changes.txt
			spec file cleanup due to rpmlint checks
			init script updates

* Tue Jun 03 2008 Morgan Weetman <morganweetman@users.sourceforge.net>
- (0.1.14b17-1)		First attempt at distro neutral init script
			tested on RHEL4, OpenSuSE 10.3

* Mon Mar 31 2008 Morgan Weetman <morganweetman@users.sourceforge.net>
- (0.1.14b17-1rh)	Security update - prior update unsuccessful

* Fri Mar 20 2008 Morgan Weetman <morganweetman@users.sourceforge.net>
- (0.1.14b15-1rh)	Security update

* Fri Mar 20 2008 Morgan Weetman <morganweetman@users.sourceforge.net>
- (0.1.14b14-1rh)	Initial redhat/fedora rpm release.
