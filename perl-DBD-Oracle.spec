Summary: DBD-Oracle module for perl
Name: perl-DBD-Oracle
Version: 1.24a
Release: 3%{?dist}
License:  GPL+ or Artistic
Group: Development/Libraries
Source0: DBD-Oracle-%{version}.tar.gz
Source1: demo.mk
Patch2: update-blob-syn.patch
Url: http://www.cpan.org
BuildRoot: %{_tmppath}/perl-DBD-Oracle-buildroot/
BuildRequires: perl >= 0:5.6.1, perl(DBI)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: oracle-instantclient-devel
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# the version requires is not automatically picked up
Requires: perl(DBI) >= 1.51

%description
DBD-Oracle module for perl

%package explain
Summary: ora_explain script from DBD-Oracle module for perl
Group: Development/Libraries

%description explain
ora_explain script

%prep
%define modname %(echo %{name}| sed 's/perl-//')
%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

# Just for 1.24a - it is packed as 1.24
%define treeversion %(echo %{version} | sed 's/a$//')

%setup -q -n %{modname}-%{treeversion}
%patch2 -p1

cp %{SOURCE1} .

%build

MKFILE=$(find /usr/share/oracle/ -name demo.mk)
%ifarch ppc ppc64
# the included version in oracle-instantclient-devel is bad on ppc arches
# using the version from i386 rpm
MKFILE=demo.mk
%endif
%ifarch x86_64 s390x
ORACLE_HOME=$(find /usr/lib/oracle/ -name client64)
%else
ORACLE_HOME=$(find /usr/lib/oracle/ -name client)
%endif
export ORACLE_HOME
perl Makefile.PL -m $MKFILE INSTALLDIRS="vendor" PREFIX=%{_prefix}
make  %{?_smp_mflags} OPTIMIZE="%{optflags}"

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT%{_prefix} pure_install

rm -f `find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist`

%files
%defattr(-,root,root)
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/Oraperl.pm
%{perl_vendorarch}/oraperl.ph
%{_mandir}/man3/*

%files explain
%defattr(-,root,root)
%{_bindir}/ora_explain
%{_mandir}/man1/ora_explain.1.gz

%changelog
* Tue Jun 08 2010 Jan Pazdziora 1.24a-3
- rebuild to fix dist-cvs issue.

* Wed May 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.24a-2
- updated to upstream version 1.24a

* Thu Dec 17 2009 Justin Sherrill <jsherril@redhat.com> 1.23-5
- 548489 - adding patch to fix issue with updating/inserting a blob using a
  synonym (jsherril@redhat.com)

* Fri Jun 05 2009 Milan Zazrivec <mzazrivec@redhat.com> 1.23-4
- bug 504281: fix out of memory error

* Tue Jun 02 2009 Miroslav Suchý <msuchy@redhat.com> 1.23-3
- apply commit 12769 from Bug 46016 from upstream as patch

* Mon Jun 01 2009 Michael Mraka <michael.mraka@redhat.com> 1.23-2
- 470999 - fixed warnings on s390(x)

* Wed May 20 2009 Jan Pazdziora 1.23-1
- rebase to latest stable upstream 1.23
- fix typo in Summary of -explain subpackage

* Tue May 19 2009 Jan Pazdziora 1.22-15
- use plain find instead of rpm -ql for now

* Wed Apr 01 2009 Miroslav Suchý <msuchy@redhat.com> 1.22-13
- 493295 - requires perl-DBI >= 1.51

* Sat Feb 28 2009 Dennis Gilmore 1.22-12
- ppc oracle-instantclient-devel has a bade demo.mk file

* Fri Feb 27 2009 Dennis Gilmore <dgilmore@redhat.com> 1.22-11
- fix up sources and correct setup

* Fri Feb 27 2009 Dennis Gilmore <dgilmore@redhat.com> 1.22-10
- Rebuild for ppc ppc64 and ia64

* Wed Feb 25 2009 Devan Goodwin <dgoodwin@redhat.com> 1.22-9
- Rebuild for new rel-eng tools.

* Mon Jan 19 2009 Dennis Gilmore <dgilmore@redhat.com> 1.22-8
- bump and rebuild for git tag

* Thu Jan 15 2009 Dennis Gilmore <dgilmore@redhat.com> 1.22-6
- BR perl(ExtUtils::MakeMaker)

* Wed Dec 10 2008 Michael Mraka <michael.mraka@redhat.com> 1.22-5
- simplified %%build and %%instal stage
- resolved #470999

* Tue Nov 25 2008 Miroslav Suchy <msuchy@redhat.com> 1.22-2
- added buildrequires for oracle-lib-compat
- rebased to DBD::Oracle 1.22
- removed DBD-Oracle-1.14-blobsyn.patch

* Thu Oct 16 2008 Milan Zazrivec 1.21-4
- bumped release for minor release tagging
- added %%{?dist} to release

* Tue Aug 26 2008 Mike McCune 1.21-3
- Cleanup spec file to work in fedora and our new Makefile structure

* Wed Jul  2 2008 Michael Mraka <michael.mraka@redhat.com> 1.21-2
- rebased to DBD::Oracle 1.21, Oracle Instantclient 10.2.0.4
- ora_explain moved into subpackage

* Wed May 21 2008 Jan Pazdziora - 1.19-8
- rebuild on RHEL 4 as well.

* Fri Dec 05 2007 Michael Mraka <michael.mraka@redhat.com>
- update to DBD::Oracle 1.19 to support oracle-instantclient

* Fri Jun 20 2003 Mihai Ibanescu <misa@redhat.com>
- Linking against Oracle 9i Release 2 client libraries.

* Sun Nov 11 2001 Chip Turner <cturner@redhat.com>
- update to DBD::Oracle 1.12 to fix LOB bug

* Mon Jul 23 2001 Cristian Gafton <gafton@redhat.com>
- compile against oracle libraries using -rpath setting
- disable as many checks as we can from the default Makefile.PL

* Mon Apr 30 2001 Chip Turner <cturner@redhat.com>
- Spec file was autogenerated.
