%define name	gavl
%define version	1.1.1
%define release %mkrel 1

%define major	1
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Name: 	 	%{name}
Summary: 	Gmerlin Audio Video Library
Version: 	%{version}
Release: 	%{release}
Source:		http://downloads.sourceforge.net/project/gmerlin/%{name}/%{version}/%{name}-%{version}.tar.gz
URL:		http://gmerlin.sourceforge.net/
License:	GPLv2+
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig 
BuildRequires:  libsamplerate-devel
BuildRequires:  png-devel
BuildRequires:	doxygen

%description
GAVL is short for Gmerlin Audio Video Library. It standardized types audio
and video formats, and defines generic container types for video frames and
blocks of audio samples.

In addition, it handles the sometimes ugly task to convert between all these
formats. The idea is to be able to convert from any format to any other with
the lowest possible CPU usage. 

%package -n     %{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %name.

%package -n     %{develname}
Summary:        Header files and static libraries from %name
Group:          Development/C
Requires:       %{libname} >= %{version}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{name}-devel < %{version}-%{release}
Obsoletes:	%mklibname gavl 0 -d

%description -n %{develname}
Libraries and includes files for developing programs based on %name.

%prep
%setup -q
#Disable buildtime cpu detection
sed -i -i 's/LQT_TRY_CFLAGS/dnl LQT_TRY_CFLAGS/g' configure.ac
sed -i -i 's/LQT_OPT_CFLAGS/dnl LQT_OPT_CFLAGS/g' configure.ac


%build
autoconf
# Adding some upstream CFLAGS
export CFLAGS=$(echo %optflags | sed -e "s/-O2/-O3 -funroll-all-loops -fomit-frame-pointer -ffast-math -fvisibility=hidden/")
%configure2_5x	--disable-static \
		--disable-cpu-clip \

%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc AUTHORS TODO README
%doc %_datadir/doc/gavl/apiref
%{_libdir}/pkgconfig/*
%{_includedir}/gavl
%{_libdir}/*.so
%{_libdir}/*.la
