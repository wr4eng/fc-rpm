# Epson Inkjet Printer Driver 2 (ESC/P-R) for Fedora (COPR)
Name:           epson-inkjet-printer-escpr2
Version:        1.2.38
Release:        4%{?dist}
Summary:        Epson Inkjet Printer Driver 2 (ESC/P-R) for Linux
License:        LGPL-2.0-or-later
URL:            https://support.epson.net/linux/Printer/LSB_distribution_pages/en/escpr2.php

Source0:        https://download-center.epson.com/f/module/42a6470c-53bf-4993-abad-ba5b4a1d5d84/%{name}-%{version}-1.tar.gz
Patch0:         bug_x86_64.patch
Patch1:         enable_velvet_fine_art_paper.patch

ExclusiveArch:  x86_64 aarch64 %{ix86}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  cups-devel

Requires:       cups
Requires:       ghostscript

# CUPS keeps its own filter/backend tree outside the distro's libdir
# convention (always /usr/lib/cups/... even on lib64 systems). Ask
# cups-config for the real path instead of assuming %%{_libdir}.
%global cups_serverbin %(cups-config --serverbin 2>/dev/null || echo %{_exec_prefix}/lib/cups)

%description
Epson Inkjet Printer Driver 2 (ESC/P-R) for Linux. This is the
second-generation ESC/P-R driver that supports newer Epson inkjet and
EcoTank printers not covered by the original escpr driver. It provides
CUPS filter and PPD files with support for features such as duplex
printing, high-resolution output, and additional media types including
Velvet Fine Art Paper (via patch).

%prep
# Source tarball contains a nested tarball
tar xvf %{SOURCE0}
cd %{name}-%{version}
%patch -P0 -p1
%patch -P1 -p1
autoreconf -vif

%build
cd %{name}-%{version}

%configure \
    --with-cupsfilterdir=%{cups_serverbin}/filter \
    --with-cupsppddir=%{_datadir}/ppd

%make_build

%install
cd %{name}-%{version}
%make_install

%files
%license %{name}-%{version}/COPYING
%{cups_serverbin}/filter/epson-escpr2
%{cups_serverbin}/filter/epson-escpr-wrapper2
%{_datadir}/ppd/%{name}/
%{_libdir}/libescpr2.so.*
%exclude %{_libdir}/libescpr2.a
%exclude %{_libdir}/libescpr2.so

%changelog
* Sun Jul 26 2026 W. Hadi HSW <wra.eng@gmail.com> - 1.2.38-4
- Escape %% in spec comment to silence "Macro expanded in comment" rpmbuild warning.
- Fix CUPS filter install path: use cups-config --serverbin instead of
  %%{_libdir}, since CUPS always expects filters under /usr/lib/cups
  even on lib64 systems.
