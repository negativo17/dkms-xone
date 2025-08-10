%global commit 197b160f7806d7d27117b12198cacb7656a07f1f
%global date 20250502
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global tag %{version}

%global debug_package %{nil}
%global dkms_name xone

Name:       dkms-%{dkms_name}
Version:    0.4.2%{!?tag:^%{date}git%{shortcommit}}
Release:    1%{?dist}
Summary:    Linux kernel driver for Xbox One and Xbox Series X|S accessories
License:    GPLv2
URL:        https://github.com/dlundqvist/xone
BuildArch:  noarch

%if 0%{?tag:1}
Source0:    %{url}/archive/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
%else
Source0:    %{url}/archive/%{commit}.tar.gz#/%{dkms_name}-%{shortcommit}.tar.gz
%endif

BuildRequires:  sed

Provides:   %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:   %{dkms_name}-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:   dkms

%description
Linux kernel driver for Xbox One and Xbox Series X|S accessories.

%prep
%if 0%{?tag:1}
%autosetup -p1 -n %{dkms_name}-%{version}
%else
%autosetup -p1 -n %{dkms_name}-%{commit}
%endif

sed -i \
    -e 's|#VERSION#|%{version}|g' \
    -e 's|kernel/drivers/input/joystick|extra|g' \
    dkms.conf

find . -type f -name '*.c' -exec sed -i "s/#VERSION#/%{version}/" {} \;

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr auth bus driver transport Kbuild dkms.conf %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
* Sun Aug 10 2025 Simone Caronni <negativo17@gmail.com> - 0.4.2-1
- Update to 0.4.2.

* Sun Aug 03 2025 Simone Caronni <negativo17@gmail.com> - 0.4.1-1
- Update to 0.4.1.

* Fri Aug 01 2025 Simone Caronni <negativo17@gmail.com> - 0.3.5-1
- Update to 0.3.5.

* Tue May 20 2025 Simone Caronni <negativo17@gmail.com> - 0.3^20250502git197b160-18
- Drop weak modules configuration, it's already disabled in Fedora.

* Sat May 10 2025 Simone Caronni <negativo17@gmail.com> - 0.3^20250502git197b160-17
- Update to latest snapshot.

* Wed Dec 25 2024 Simone Caronni <negativo17@gmail.com> - 0.3^20241223git6b9d59a-16
- Switch to https://github.com/dlundqvist/xone fork.

* Wed Oct 16 2024 Simone Caronni <negativo17@gmail.com> - 0.3^20240425git29ec357-15
- Fix build on 6.11/6.12 kernels.
- Do not uninstall in preun scriptlet in case of an upgrade.

* Tue Sep 24 2024 Simone Caronni <negativo17@gmail.com> - 0.3^20240425git29ec357-14
- Use new packaging guidelines for snapshots.

* Tue Jun 25 2024 Simone Caronni <negativo17@gmail.com> - 0.3-13.20240425git29ec357
- Set appropriate version into modules.

* Mon Jun 24 2024 Simone Caronni <negativo17@gmail.com> - 0.3-12.20240425git29ec357
- Adjust path in DKMS configuration file.

* Mon Jun 24 2024 Simone Caronni <negativo17@gmail.com> - 0.3-11.20240425git29ec357
- Use bundled DKMS configuration file.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 0.3-10.20240425git29ec357
- Update to latest snapshot.

* Wed Mar 13 2024 Simone Caronni <negativo17@gmail.com> - 0.3-9.20240310gite9a7291
- Update to the latest snapshot.

* Thu Feb 22 2024 Simone Caronni <negativo17@gmail.com> - 0.3-8.20240214gitab688dd
- Fix build.

* Sat Feb 17 2024 Simone Caronni <negativo17@gmail.com> - 0.3-7.20240214gitab688dd
- Update to latest snapshot.

* Mon Feb 12 2024 Simone Caronni <negativo17@gmail.com> - 0.3-6.20240211git2388401
- Update to latest snapshot.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 0.3-5.20240127gitd93b4d5
- Update to latest snapshot.

* Tue Jan 23 2024 Simone Caronni <negativo17@gmail.com> - 0.3-4.20240118giteaa55d0
- Update to latest snapshot.

* Wed Jan 17 2024 Simone Caronni <negativo17@gmail.com> - 0.3-3.20240116gitaf5e344
- Update to latest snapshot.

* Sun Jun 04 2023 Simone Caronni <negativo17@gmail.com> - 0.3-2.20230517gitbbf0dcc
- Update to latest snapshot.

* Tue Aug 9 2022 Simone Caronni <negativo17@gmail.com> - 0.3-1
- First build.
