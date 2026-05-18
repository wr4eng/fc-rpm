Name:           vtzero
Version:        1.2.0
Release:        1%{?dist}
Summary:        Tiny and fast vector tile decoder and encoder in C++

License:        BSD-2-Clause
URL:            https://github.com/mapbox/vtzero
Source0:        https://github.com/mapbox/vtzero/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# vtzero is a header-only C++ library.
# protozero headers needed at configure time for FindProtozero.cmake check.
# No iwyu/cppcheck/doxygen/boost needed — those are optional upstream dev tools.
BuildRequires:  cmake >= 3.18
BuildRequires:  gcc-c++
BuildRequires:  protozero-devel >= 1.7.0

BuildArch:      noarch


%description
vtzero is a header-only C++ library for reading and writing Mapbox Vector
Tiles (VT spec 2.x). It is tiny and fast with minimal dependencies.


# ── devel subpackage ──────────────────────────────────────────────────────────
# For header-only libraries everything ships in -devel.
%package        devel
Summary:        Development files for %{name}
Requires:       protozero-devel >= 1.7.0

%description    devel
Header files for the vtzero vector tile C++ library.


# ── prep ──────────────────────────────────────────────────────────────────────
%prep
%autosetup -p1 -n %{name}-%{version}


# ── build ─────────────────────────────────────────────────────────────────────
# vtzero 1.2.0 cmake installs ONLY headers — no cmake config, no .so, no pkgconfig.
# Confirmed from install_manifest: only include/vtzero/*.hpp is installed.
# We disable examples, tests, and docs to avoid pulling in extra dependencies.
%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DBUILD_TESTING=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_DOCS=OFF \
    -DWITH_DOCS=OFF

%cmake_build


# ── install ───────────────────────────────────────────────────────────────────
%install
%cmake_install

# cmake_install only puts headers in buildroot.
# License is in the source tree — install manually.
install -D -m 0644 LICENSE \
    %{buildroot}%{_licensedir}/%{name}/LICENSE


# ── file lists ────────────────────────────────────────────────────────────────

# Base package: empty metapackage, carries the license
%files
%license %{_licensedir}/%{name}/LICENSE


# devel: the only actual content — 16 header files
# vtzero 1.2.0 does NOT install cmake find_package config or pkgconfig.
# Consumers must add the include path manually or use the bundled source.
%files devel
%{_includedir}/vtzero/
%license %{_licensedir}/%{name}/LICENSE


# ── changelog ─────────────────────────────────────────────────────────────────
%changelog
* Mon May 18 2026 W. Hadi HSW <wra.eng@gmail.com> - 1.2.0-1
- Initial Fedora package for vtzero 1.2.0
- Header-only library: BuildArch noarch, single -devel subpackage
- cmake install only produces include/vtzero/*.hpp (confirmed from
  install_manifest); no cmake config or pkgconfig is generated upstream
- Disabled examples, tests, and docs in cmake to avoid extra dependencies
