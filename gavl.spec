%define name	gavl
%define version	0.2.5
%define release %mkrel 2

%define major	0
%define libname %mklibname %name %major

Name: 	 	%{name}
Summary: 	Gmerlin Audio Video Library
Version: 	%{version}
Release: 	%{release}

Source:		http://prdownloads.sourceforge.net/gmerlin/%{name}-%{version}.tar.bz2
URL:		http://gmerlin.sourceforge.net/
License:	GPL
Group:		System/Libraries
BuildRequires:	pkgconfig 
BuildRequires:  libsamplerate-devel
BuildRequires:  png-devel

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
#Provides:      %name
#Obsoletes:     %name = %version-%release

%description -n %{libname}
Dynamic libraries from %name.

%package -n     %{libname}-devel
Summary:        Header files and static libraries from %name
Group:          Development/C
Requires:       %{libname} >= %{version}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep
%setup -q

%build
%configure2_5x
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc AUTHORS TODO README
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la


