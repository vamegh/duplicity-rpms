%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:        Encrypted bandwidth-efficient backup using rsync algorithm
Name:           duplicity
Version:        0.6.26
Release:        4vh%{?dist}
License:        GPLv2+
Group:          Applications/Archiving
URL:            http://www.nongnu.org/duplicity/
Source:         http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.gz
Patch0:         duplicity-0.6.22-documentation.patch
Requires:       python-GnuPGInterface >= 0.3.2, gnupg >= 1.0.6
Requires:       openssh-clients, ncftp >= 3.1.9, rsync, python-boto >= 0.9d
Requires:       python-paramiko python-lockfile

%if 0%{?rhel}  != 5
Requires:      ca-certificates
%endif

BuildRequires:  python-devel librsync-devel >= 0.9.6
BuildRequires:  python-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Duplicity incrementally backs up files and directory by encrypting
tar-format volumes with GnuPG and uploading them to a remote (or
local) file server. In theory many protocols for connecting to a
file server could be supported; so far ssh/scp, local file access,
rsync, ftp, HSI, WebDAV and Amazon S3 have been written.

Because duplicity uses librsync, the incremental archives are space
efficient and only record the parts of files that have changed since
the last backup. Currently duplicity supports deleted files, full
unix permissions, directories, symbolic links, fifos, device files,
but not hard links.

%prep
%setup -q
%patch0 -p1 -b .documentation

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
ln -sf %{_sysconfdir}/pki/tls/cert.pem \
       %{buildroot}/%{_sysconfdir}/%{name}/cacert.pem

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc CHANGELOG COPYING README
%{_bindir}/rdiffdir
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%{_mandir}/man1/rdiffdir*
%{python_sitearch}/%{name}*
%{_sysconfdir}/%{name}/cacert.pem

%changelog
* Thu Jul 26 2018 Vamegh Hedayati <vhedayati@ev9.io> - 0.6.26-2vh1
- Added kms_key support to s3 bucket put operation

* Wed Apr 6 2016 Andy Grover <agrover@redhat.com> - 0.6.26-2
- Upgrade to 0.6.26 for corruption issue (#1324641)
- Update patch0
- Drop now-merged patch for librsync API changes
- Add BuildRequires on python-setuptools
- Add dep on python-lockfile

* Sat Mar 07 2015 Robert Scheck <robert@fedoraproject.org> - 0.6.22-4
- Rebuild for librsync 1.0.0 (#1126712)

* Fri Dec 27 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.22-3
- Fix ssl cert enforcement (rhbz#960860)
- Fix bogus date in changelog

* Thu Dec 26 2013 Robert Scheck <robert@fedoraproject.org> 0.6.22-2
- Added runtime requirement to python-paramiko (#819272, #918933)

* Wed Dec 25 2013 Robert Scheck <robert@fedoraproject.org> 0.6.22-1
- Upgrade to 0.6.22 (#903584, #992158)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.21-1
- Upgrade to 0.6.21
- Fixes data corruption issues (#922576)
- Fix bogus dates in spec changelog

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.20-1
- Upgrade to 0.6.20 (#827960)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Robert Scheck <robert@fedoraproject.org> 0.6.18-1
- Upgrade to 0.6.18 (#798951)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011 Robert Scheck <robert@fedoraproject.org> 0.6.17-1
- Upgrade to 0.6.17 (#736715)

* Sun Jul 17 2011 Robert Scheck <robert@fedoraproject.org> 0.6.14-1
- Upgrade to 0.6.14 (#720589, #697222)
- Backported optparse 1.5a2 from RHEL 5 for RHEL 4 (#717133)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Robert Scheck <robert@fedoraproject.org> 0.6.11-1
- Upgrade to 0.6.11 (#655870)

* Sun Oct 31 2010 Robert Scheck <robert@fedoraproject.org> 0.6.10-1
- Upgrade to 0.6.10
- Added a patch to avoid ternary conditional operators (#639863)

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> 0.6.09-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Robert Scheck <robert@fedoraproject.org> 0.6.09-1
- Upgrade to 0.6.09 (#596018)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.08b-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Mar 28 2010 Robert Scheck <robert@fedoraproject.org> 0.6.08b-1
- Upgrade to 0.6.08b

* Sat Dec 26 2009 Robert Scheck <robert@fedoraproject.org> 0.6.06-1
- Upgrade to 0.6.06 (#550663)

* Sun Sep 27 2009 Robert Scheck <robert@fedoraproject.org> 0.6.05-1
- Upgrade to 0.6.05 (#525940)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Robert Scheck <robert@fedoraproject.org> 0.5.18-1
- Upgrade to 0.5.18

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.5.16-1
- Upgrade to 0.5.16

* Thu Apr 16 2009 Robert Scheck <robert@fedoraproject.org> 0.5.15-1
- Upgrade to 0.5.15

* Sat Mar 21 2009 Robert Scheck <robert@fedoraproject.org> 0.5.12-1
- Upgrade to 0.5.12 (#490289)

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.5.06-2
- Rebuild for gcc 4.4 and rpm 4.6

* Sun Jan 25 2009 Robert Scheck <robert@fedoraproject.org> 0.5.06-1
- Upgrade to 0.5.06 (#481489)

* Sun Dec 07 2008 Robert Scheck <robert@fedoraproject.org> 0.5.03-1
- Upgrade to 0.5.03

* Fri Dec 05 2008 Jeremy Katz <katzj@redhat.com> 0.4.12-3
- Rebuild for python 2.6

* Fri Aug 08 2008 Robert Scheck <robert@fedoraproject.org> 0.4.12-2
- Added patch to get scp without username working (#457680)

* Sun Jul 27 2008 Robert Scheck <robert@fedoraproject.org> 0.4.12-1
- Upgrade to 0.4.12

* Sat Jun 28 2008 Robert Scheck <robert@fedoraproject.org> 0.4.11-2
- Added patch for incremental backups using python 2.3 (#453069)

* Mon May 05 2008 Robert Scheck <robert@fedoraproject.org> 0.4.11-1
- Upgrade to 0.4.11 (#440346)

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 0.4.9-1
- Upgrade to 0.4.9 (#293081, #431467)

* Sat Dec 08 2007 Robert Scheck <robert@fedoraproject.org> 0.4.7-1
- Upgrade to 0.4.7

* Sat Sep 15 2007 Robert Scheck <robert@fedoraproject.org> 0.4.3-1
- Upgrade to 0.4.3 (#265701)
- Updated the license tag according to the guidelines

* Mon May 07 2007 Robert Scheck <robert@fedoraproject.org> 0.4.2-7
- Rebuild

* Wed Dec 20 2006 Robert Scheck <robert@fedoraproject.org> 0.4.2-6
- fix broken sftp support by adding --sftp-command (#220316)

* Sun Dec 17 2006 Robert Scheck <robert@fedoraproject.org> 0.4.2-5
- own %%{python_sitearch}/%%{name} and not only %%{python_sitearch}

* Sat Dec 16 2006 Robert Scheck <robert@fedoraproject.org> 0.4.2-4
- added two small fixing patches (upstream items #4486, #5183)
- many spec file cleanups and try to silence rpmlint a bit more

* Fri Sep 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-3
- don't ghost pyo files

* Sun Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-2
- Rebuild for FC6

* Tue May 16 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.4.2-1
- version bump

* Thu Apr 7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Oct 05 2003 Ben Escoto <bescoto@stanford.edu> - 0:0.4.1-0.fdr.3
- More hints from Fedora QA (ville.skytta@iki.fi)

* Sat Aug 09 2003 Ben Escoto <bescoto@stanford.edu> - 0:0.4.1-0.fdr.2
- Repackaging for Fedora

* Fri Aug 30 2002 Ben Escoto <bescoto@stanford.edu>
- Initial RPM
