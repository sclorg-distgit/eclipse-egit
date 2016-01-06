%{?scl:%scl_package eclipse-egit}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

# EGit and Mylyn have circular dependencies
# EGit can build bootstrapped when Mylyn not present
%global bootstrap 0
%global version_suffix 201506240215-r

Name:             %{?scl_prefix}eclipse-egit
Version:          4.0.1
Release:          2.3.bs2%{?dist}
Summary:          Eclipse Git Integration

License:          EPL
URL:              http://www.eclipse.org/egit
Source0:          http://git.eclipse.org/c/egit/egit.git/snapshot/egit-%{version}.%{version_suffix}.tar.xz
%if %{bootstrap}
Patch0:           remove-mylyn-dep.patch
%endif

BuildRequires:    %{?scl_prefix}tycho
BuildRequires:    %{?scl_prefix}eclipse-jgit >= 4.0.0
BuildRequires:    %{?scl_prefix}eclipse-jdt
%if ! %{bootstrap}
BuildRequires:    %{?scl_prefix}eclipse-mylyn
BuildRequires:    %{?scl_prefix}eclipse-mylyn-docs-wikitext
%endif

BuildArch:        noarch

%description
The eclipse-egit package contains Eclipse plugins for
interacting with Git repositories.

%if ! %{bootstrap}
%package mylyn
Summary:     Git integration for mylyn.

%description mylyn
Git integration for mylyn.
%endif

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n egit-%{version}.%{version_suffix}
%if %{bootstrap}
%patch0
%endif

%pom_xpath_remove "pom:repositories"
%pom_xpath_remove "pom:dependencies"
%pom_xpath_remove "pom:profiles"
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin/pom:configuration/pom:target"
%pom_xpath_remove "*[local-name() ='plugin' and (child::*[text()='tycho-packaging-plugin'])]"
%pom_xpath_remove "pom:dependencies" org.eclipse.egit.doc/pom.xml
%pom_disable_module org.eclipse.egit.repository
%pom_disable_module org.eclipse.egit.source-feature
%pom_disable_module org.eclipse.egit.target
%pom_disable_module org.eclipse.egit.core.test
%pom_disable_module org.eclipse.egit.ui.test
%pom_disable_module org.eclipse.egit.ui.importer
%pom_disable_module org.eclipse.egit.gitflow.test
%pom_disable_module org.eclipse.egit.mylyn.ui.test

%if %{bootstrap}
#to avoid mylyn circular dependancy
%pom_disable_module org.eclipse.egit.mylyn.ui
%pom_disable_module org.eclipse.egit.mylyn-feature
%endif

%mvn_package org.eclipse.egit:egit-parent __noinstall
%if ! %{bootstrap}
%mvn_package :*mylyn* mylyn
%endif
%mvn_package :* egit
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -j -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}


%files -f .mfiles-egit
%doc LICENSE README.md

%if ! %{bootstrap}
%files mylyn -f .mfiles-mylyn
%doc LICENSE README.md
%endif

%changelog
* Thu Jul 16 2015 Mat Booth <mat.booth@redhat.com> - 4.0.1-2.3
- Fix unowned directories

* Wed Jul 08 2015 Mat Booth <mat.booth@redhat.com> - 4.0.1-2.2
- Non-bootstrap build to enable mylyn support

* Thu Jul 02 2015 Mat Booth <mat.booth@redhat.com> - 4.0.1-2.1
- Import latest from Fedora
- Enable bootstrap mode

* Thu Jul 02 2015 Mat Booth <mat.booth@redhat.com> - 4.0.1-2
- Drop incomplete SCL macros

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.1-1
- Update to 4.0.1.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-1
- Update to 4.0 final.

* Mon Jun 1 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-0.2.rc2
- Rebuild for jgit.

* Thu May 28 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-0.1.rc2
- Update to 4.0 rc2.

* Thu May 14 2015 Alexander Kurtakov <akurtako@redhat.com> 3.7.1-1
- Update to upstream 3.7.1 release.

* Mon Mar 02 2015 Roland Grunberg <rgrunber@redhat.com> - 3.7.0-1
- Update to upstream 3.7.0 release.

* Fri Jan 23 2015 Alexander Kurtakov <akurtako@redhat.com> 3.6.2-1
- Update to upstream 3.6.2 release.

* Mon Jan 19 2015 Roland Grunberg <rgrunber@redhat.com> - 3.6.1-2
- Add bootstrapping capability.

* Mon Jan 5 2015 Alexander Kurtakov <akurtako@redhat.com> 3.6.1-1
- Update to upstream 3.6.1 release.

* Fri Dec 19 2014 Alexander Kurtakov <akurtako@redhat.com> 3.5.3-1
- Update to upstream 3.5.3 release.

* Thu Dec 18 2014 Alexander Kurtakov <akurtako@redhat.com> 3.5.2-1
- Update to upstream 3.5.2 release.

* Fri Nov 07 2014 Mat Booth <mat.booth@redhat.com> - 3.5.0-2
- Build/install with mvn_build/mvn_install

* Fri Oct 03 2014 Mat Booth <mat.booth@redhat.com> - 3.5.0-1
- Update to latest upstream release 3.5.0

* Thu Jun 26 2014 Mat Booth <mat.booth@redhat.com> - 3.4.1-1
- Update to latest upstream release 3.4.1

* Fri Jun 13 2014 Roland Grunberg <rgrunber@redhat.com> - 3.4.0-1
- Update to 3.4.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Sami Wagiaalla <swagiaal@redhat.com> - 3.3.2-2
- Fix build agains the lates o.e.jface.util.Policy.

* Mon Apr 28 2014 Mat Booth <mat.booth@redhat.com> - 3.3.2-1
- Update to 3.3.2.

* Fri Mar 28 2014 Alexander Kurtakov <akurtako@redhat.com> 3.3.1-1
- Update to 3.3.1.

* Tue Mar 11 2014 Alexander Kurtakov <akurtako@redhat.com> 3.3.0-1
- Update to 3.3.0.

* Sun Dec 29 2013 Alexander Kurtakov <akurtako@redhat.com> 3.2.0-1
- Update to 3.2.0.

* Mon Oct 21 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.1.0-3
- Fix feature installation.

* Wed Oct 16 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.1.0-2
- Package Egit integration for mylyn.
- Changed building process to reflect upstream one.

* Thu Oct 3 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.1.0-1
- Update to Kepler SR1.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 5 2013 Neil Brian Guzman <nguzman@redhat.com> 3.0.0-3
- Bump release

* Tue Jun 25 2013 Neil Brian Guzman <nguzman@redhat.com> 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jun 25 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.0.0-1
- Update to 3.0.0.

* Thu Feb 21 2013 Sami Wagiaalla <swagiaal@redhat.com> 2.3.1-1
- SCL-ized.

* Thu Feb 21 2013 Sami Wagiaalla <swagiaal@redhat.com> 2.3.1-1
- Update to 2.3.1.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 3 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.2.0-1
- Update to latest upstream.

* Mon Oct 1 2012 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-1
- Update to 2.1.0 release.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 2 2012 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-1
- Update to 2.0.0 upstream release.

* Fri Apr 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.3.0-3
- Use eclipse-pdebuild over pdebuild in lib.

* Thu Apr 26 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.3.0-2
- Fix 1.3.0 which was previously using wrong sources.
- Fix JGit BR/R since EGit depends on the same version of JGit.

* Fri Feb 17 2012 Andrew Robinson <arobinso@redhat.com> 1.3.0-1
- Update to 1.3.0 upstream release.

* Thu Jan 5 2012 Alexander Kurtakov <akurtako@redhat.com> 1.2.0-1
- Update to upstream 1.2.0.

* Fri Nov 18 2011 Alexander Kurtakov <akurtako@redhat.com> 1.1.0-2
- Add patch to fix New git repo wizard.

* Mon Jun 27 2011 Andrew Robinson <arobinso@redhat.com> 1.1.0-1
- Update to upstream release 1.1.0.

* Tue Jun 14 2011 Chris Aniszczyk <zx@redhat.com> 1.0.0-2
- Update to final upstream release v1.0.0.201106090707-r.

* Tue Jun 07 2011 Chris Aniszczyk <zx@redhat.com> 1.0.0-1
- Update to upstream release 1.0.0.

* Tue May 03 2011 Chris Aniszczyk <zx@redhat.com> 0.12.1-1
- Update to upstream release 0.12.1.

* Tue Feb 22 2011 Chris Aniszczyk <zx@redhat.com> 0.11.3-2
- Update to fix issue with GitCloneWizard file.

* Tue Feb 22 2011 Chris Aniszczyk <zx@redhat.com> 0.11.3-1
- Update to upstream release 0.11.3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Chris Aniszczyk <zx@redhat.com> 0.10.1-1
- Update to upstream release 0.10.1.

* Thu Oct 7 2010 Chris Aniszczyk <zx@redhat.com> 0.9.3-1
- Update to upstream release 0.9.3.

* Wed Sep 15 2010 Severin Gehwolf <sgehwolf@redhat.com> 0.9.1-1
- Update to upstream release 0.9.1.
- Remove git-core dependency.

* Thu Aug 26 2010 Severin Gehwolf <sgehwolf at, redhat.com> 0.9.0-0.1.20100825git
- Make release tag more readable (separate "0.1" and pre-release tag by ".").

* Wed Aug 25 2010 Severin Gehwolf <sgehwolf at, redhat.com> 0.9.0-0.120100825git
- Pre-release of EGit 0.9.0

* Thu Jun 24 2010 Severin Gehwolf <sgehwolf at, redhat.com> 0.8.4-1
- Rebase to 0.8.4 release.

* Tue Apr 13 2010 Jeff Johnston <jjohnstn@redhat.com> 0.7.1-2
- Bump up release.

* Tue Apr 13 2010 Jeff Johnston <jjohnstn@redhat.com> 0.7.1-1
- Rebase to 0.7.1.

* Fri Mar 19 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.0-1
- Update to 0.7.0.
- License is only EPL now.

* Tue Feb 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0.6.0-0.1.git20100208
- New git snapshot.

* Tue Nov 10 2009 Alexander Kurtakov <akurtako@redhat.com> 0.6.0-0.1.git20091029
- Update to 0.6 git.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Alexander Kurtakov <akurtako@redhat.com> 0.5.0-1
- Update to 0.5.0.

* Mon Mar 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0.4.0-3.20090323
- Update to latest snapshot.

* Mon Mar 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0.4.0-3.20090217
- Rebuild to not ship p2 context.xml.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2.20090217
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Alexander Kurtakov <akurtako@redhat.com> 0.4.0-1.20090217
- New snapshot.

* Wed Dec 10 2008 Alexander Kurtakov <akurtako@redhat.com> 0.4.0-1
- Update to 0.4.0.

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> 0.3.1.20081022-3
- New git version.

* Wed Jul 30 2008 Andrew Overholt <overholt@redhat.com> 0.3.1-2
- Move files and update build for Eclipse SDK 3.4
- Use pdebuild

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.1-1
- fix license tag

* Tue Apr 08 2008 Jesse Keating <jkeating@redhat.com> - 0.3.1-0
- New upstream release 0.3.1, makes committing / diffing actually work

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.0-3
- Autorebuild for GCC 4.3

* Thu Oct 04 2007 Ben Konrath <bkonrath@redhat.com> 0.3.0-2.fc8
- Require git-core instead of git.
- Resolves: #319321

* Mon Sep 24 2007 Ben Konrath <bkonrath@redhat.com> 0.3.0-1.fc8
- 0.3.0

* Wed Sep 19 2007 Ben Konrath <bkonrath@redhat.com> 0.2.99-0.git20070919.fc8
- 0.2.99 git20070919

* Mon Sep 17 2007 Ben Konrath <bkonrath@redhat.com> 0.2.2-2.git20070911.fc8
- Update add feature and plugin patch.

* Mon Sep 17 2007 Ben Konrath <bkonrath@redhat.com> 0.2.2-1.git20070911.fc8
- Require eclipse-platform >= 3.2.1 

* Fri Sep 14 2007 Ben Konrath <bkonrath@redhat.com> 0.2.2-0.git20070911.fc8
- Update to git20070911.
- Update feature and accosicated branding plugin.

* Wed Aug 29 2007 Ben Konrath <bkonrath@redhat.com> 0.2.2-0.git20070826.fc8
- Initial version
