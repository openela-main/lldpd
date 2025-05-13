Name:     lldpd
Version:  1.0.18
Release:  6%{?dist}
Summary:  ISC-licensed implementation of LLDP

License:  ISC
URL:      https://github.com/lldpd/
Source0:  lldpd-%{version}-free.tar.gz
Source1:  %{name}.service
Source2:  %{name}-tmpfiles
Source3:  %{name}.sysconfig
Source4:  %{name}-systemd-sysusers.conf

Source100: lldpd-cleanup.sh

Patch1: 0001-client-tx-hold-range.patch
Patch2: 0002-lldpd-limit-tx-ttl-to-65535.patch
Patch3: 0003-lldpd-fix-ttl-range.patch
Patch4: 0004-client-fix-tx-hold.patch

BuildRequires: check-devel
BuildRequires: gcc
BuildRequires: libxml2-devel
BuildRequires: libevent-devel
BuildRequires: make
BuildRequires: net-snmp-devel
BuildRequires: readline-devel
BuildRequires: systemd-rpm-macros
%{?systemd_requires}
%{?sysusers_requires_compat}

Requires(pre): shadow-utils

%description
LLDP is an industry standard protocol designed to supplant proprietary
Link-Layer protocols such as EDP or CDP. The goal of LLDP is to provide
an inter-vendor compatible mechanism to deliver Link-Layer notifications
to adjacent network devices.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: %{summary}

%description devel
%{name} development libraries and headers

%prep
%autosetup -p1

%build
%configure --disable-static --with-snmp --disable-silent-rules \
  --with-privsep-user=%{name} --with-privsep-group=%{name} \
  --with-privsep-chroot=%{_rundir}/%{name}/chroot \
  --with-lldpd-ctl-socket=%{_rundir}/%{name}/%{name}.socket \
  --with-systemdsystemunitdir=%{_unitdir} --with-sysusersdir=no

%make_build

%install
%make_install

install -p -D -m644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -D -m644 %{SOURCE3} %{buildroot}/etc/sysconfig/%{name}
install -p -D -m644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf

install -d -D -m 0755 %{buildroot}%{_rundir}/%{name}/chroot
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}
# remove the docs from buildroot
rm -rf %{buildroot}/usr/share/doc/%{name}

# don't include completion conf yet
rm -f %{buildroot}/usr/share/bash-completion/completions/lldpcli
rm -f %{buildroot}/usr/share/zsh/vendor-completions/_lldpcli
rm -f %{buildroot}/usr/share/zsh/site-functions/_lldpcli

# remove static libtool archive
find %{buildroot} -type f -name "*.la" -delete

%ldconfig_scriptlets

%pre
%sysusers_create_compat %{SOURCE4}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc NEWS README.md
%config %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/lldpcli
%{_sbindir}/lldpctl
%{_sbindir}/%{name}
%{_mandir}/man8/lldpcli.8*
%{_mandir}/man8/lldpctl.8*
%{_mandir}/man8/%{name}.8*
%{_libdir}/liblldpctl.so.4*
%dir %{_rundir}/%{name}
%dir %{_rundir}/%{name}/chroot
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%dir %attr(-,lldpd,lldpd) %{_sharedstatedir}/%{name}

%files devel
%{_includedir}/lldp-const.h
%{_includedir}/lldpctl.h
%{_libdir}/liblldpctl.so
%{_libdir}/pkgconfig/lldpctl.pc

%changelog
* Mon Dec 9 2024 Hangbin Liu <haliu@redhat.com> - 1.0.18-6
- Add range checking for tx-interval and tx-hold [RHEL-40245]

* Wed Oct 16 2024 Hangbin Liu <haliu@redhat.com> - 1.0.18-5
- Add range checking for tx-interval and tx-hold [RHEL-40245]

* Tue Mar 26 2024 Hangbin Liu <haliu@redhat.com> - 1.0.18-4
- lldpd use systemd-sysusers [RHEL-5787]

* Mon May 20 2024 Hangbin Liu <haliu@redhat.com> - 1.0.18-3
- Add lldpd-devel package [RHEL-22127]

* Sun Feb 18 2024 Hangbin Liu <haliu@redhat.com> - 1.0.18-2
- Remove networkd gating test [RHEL-25990]

* Wed Jan 31 2024 Hangbin Liu <haliu@redhat.com> - 1.0.18-1
- Rebased to 1.0.18 [RHEL-2211]

* Mon Nov 06 2023 Hangbin Liu <haliu@redhat.com> - 1.0.17-1
- Rebased to 1.0.17 [RHEL-2211, RHEL-5791, RHEL-5796]

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.0.4-10
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon Jul 12 2021 Aaron Conole <aconole@redhat.com> - 1.0.4-9
- Strip ASL components (#1982259)

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 1.0.4-8
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.0.4-7
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 29 20:35:23 CEST 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.4-5
- Rebuilt for libevent 2.1.12

* Wed Sep 02 2020 Josef Ridky <jridky@redhat.com> - 1.0.4-4
- Rebuilt for new net-snmp release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 James Hogarth <james.hogarth@gmail.com> - 1.0.4-1
- Updated to new upstream release 1.0.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-5
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 1.0.1-3
- Rebuild for new net-snmp

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018 James Hogarth <james.hogarth@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 21 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.8-1
- Update to 0.9.8

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.7-10
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.7-9
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.7-8
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 06 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-5
- Older fedora needs the older syntax matching EPEL7

* Wed Apr 05 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-4
- EPEL7 systemd needs an older syntax

* Wed Apr 05 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-3
- Use the official release tarball rather than the github snapshot
- Add EPEL6 conditionals

* Wed Apr 05 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-2
- Tweaks to spec requested in review

* Tue Apr 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.9.7-1
- Initial package
