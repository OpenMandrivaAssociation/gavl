%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

Summary:	Gmerlin Audio Video Library
Name:		gavl
Version:	1.4.0
Release:	12
License:	GPLv2+
Group:		System/Libraries
Url:		https://gmerlin.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/gmerlin/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:		gavl-1.4.0-automake-1.13-fix.patch
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(samplerate)

%description
GAVL is short for Gmerlin Audio Video Library. It standardized types audio
and video formats, and defines generic container types for video frames and
blocks of audio samples.

In addition, it handles the sometimes ugly task to convert between all these
formats. The idea is to be able to convert from any format to any other with
the lowest possible CPU usage. 

%package -n	%{libname}
Summary:	Dynamic libraries from %name
Group:		System/Libraries

%description -n	%{libname}
Dynamic libraries from %name.

%package -n	%{devname}
Summary:	Header files and static libraries from %name
Group:		Development/C
Requires:	%{libname} >= %{version}
Provides:	%{name}-devel

%description -n	%{devname}
Libraries and includes files for developing programs based on %name.

%prep
%autosetup -p1
#Disable buildtime cpu detection
sed -i -i 's/LQT_TRY_CFLAGS/dnl LQT_TRY_CFLAGS/g' configure.ac
sed -i -i 's/LQT_OPT_CFLAGS/dnl LQT_OPT_CFLAGS/g' configure.ac
autoreconf -fi

%build
# Adding some upstream CFLAGS
export CFLAGS="%{optflags} -Ofast -funroll-all-loops -fomit-frame-pointer -fvisibility=hidden"
%configure \
	--disable-static \
	--disable-cpu-clip \

%make_build
										
%install
%make_install

%files -n %{libname}
%{_libdir}/libgavl.so.%{major}*

%files -n %{devname}
%doc AUTHORS TODO README
%doc %{_datadir}/doc/gavl/apiref
%{_libdir}/pkgconfig/gavl.pc
%{_includedir}/gavl
%{_libdir}/libgavl.so
