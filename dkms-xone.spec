%global commit0 e9a7291cba1313355d31f514482898fea145586b
%global date 20240310
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global debug_package %{nil}
%global dkms_name xone

Name:       dkms-%{dkms_name}
Version:    0.3
Release:    9%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:    Linux kernel driver for Xbox One and Xbox Series X|S accessories
License:    GPLv2
URL:        https://github.com/medusalix/%{dkms_name}
BuildArch:  noarch

%if 0%{?tag:1}
Source0:    %{url}/archive/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
%else
Source0:    %{url}/archive/%{commit0}.tar.gz#/%{dkms_name}-%{shortcommit0}.tar.gz
%endif

Source1:    %{name}.conf
Source2:    dkms-no-weak-modules.conf

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
%autosetup -p1 -n %{dkms_name}-%{commit0}
%endif

cp %{SOURCE1} dkms.conf
sed -i -e 's/__VERSION_STRING/%{version}/g' dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr auth bus driver transport Kbuild dkms.conf %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%if 0%{?fedora}
# Do not enable weak modules support in Fedora (no kABI):
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
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
