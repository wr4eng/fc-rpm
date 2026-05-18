Name:           vtzero
Version:        1.2.0
Release:        1%{?dist}
Summary:        Tiny and fast vector tile decoder and encoder in C++

License:        BSD-2-Clause
URL:            https://github.com/mapbox/vtzero
Source0:        https://github.com/mapbox/vtzero/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.18
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  protozero-devel >= 1.7.0

BuildArch:      noarch


%description
vtzero is a header-only C++ library for reading and writing Mapbox Vector
Tiles (VT spec 2.x). It is tiny, fast, and depends only on protozero.


# ── devel subpackage ──────────────────────────────────────────────────────────
# Header-only libraries ship everything under -devel.
# The base package is an empty metapackage that pulls in -devel.
%package        devel
Summary:        Development files for %{name}
# No %%{name} base dep — nothing compiled to link against.
Requires:       protozero-devel >= 1.7.0

%description    devel
Header files and CMake find-package config for the vtzero vector tile
C++ library.


# ── prep ──────────────────────────────────────────────────────────────────────
%prep
%autosetup -p1 -n %{name}-%{version}


# ── build ─────────────────────────────────────────────────────────────────────
# Header-only: cmake configure + build is essentially a no-op but required
# so that cmake --install produces the correct directory layout.
%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DBUILD_TESTING=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_DOCS=OFF

%cmake_build


# ── install ───────────────────────────────────────────────────────────────────
%install
%cmake_install

# Install license file
install -m 0755 -d %{buildroot}%{_licensedir}/%{name}/
find %{_builddir}/%{name}-%{version} -maxdepth 1 -type f \
    \( -iname 'license*' -o -iname 'copying*' \) \
    -exec install -m 0644 -t %{buildroot}%{_licensedir}/%{name}/ {} +


# ── file lists ────────────────────────────────────────────────────────────────

# Base package: empty, just carries the license
%files
%license %{_licensedir}/%{name}/


# devel: headers + cmake config
%files devel
%{_includedir}/vtzero/
%{_datadir}/cmake/vtzero/
%license %{_licensedir}/%{name}/


# ── changelog ─────────────────────────────────────────────────────────────────
%changelog
* Mon May 19 2026 W. Hadi HSW <wra.eng@gmail.com> - 1.2.0-1
- Initial Fedora package for vtzero 1.2.0
- Header-only library: BuildArch noarch, single -devel subpackage
- iwyu/cppcheck/doxygen removed from BuildRequires (optional dev tools,
  not needed to produce installable headers)
- boost removed from Requires (not a runtime dependency of header-only lib)
