# TODO: fix build doxygen documentaton
#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_without	jni	# Java Native Interface library

Summary:	Portable Real-Time MIDI library
Summary(pl.UTF-8):	Przenośna biblioteka MIDI czasu rzeczywistego
Name:		portmidi
Version:	2.0.4
Release:	1
Epoch:		1
License:	MIT-like
Group:		Libraries
#Source0Download: https://github.com/PortMidi/portmidi/releases
Source0:	https://github.com/PortMidi/portmidi/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cda6c7714fe2ea8d8184226f3a85c923
Source1:	pmdefaults.desktop
URL:		https://portmedia.sourceforge.net/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	cmake >= 3.21
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_jni:BuildRequires:	jdk >= 1.5}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Portable Real-Time MIDI library.

%description -l pl.UTF-8
Przenośna biblioteka MIDI czasu rzeczywistego.

%package devel
Summary:	Header files for PortMidi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PortMidi
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	alsa-lib-devel >= 0.9
Obsoletes:	portmidi-static < 131

%description devel
Header files for PortMidi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PortMidi.

%package apidocs
Summary:	API documentation for PortMidi library
Summary(pl.UTF-8):	Dokumentacja API biblioteki PortMidi
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for PortMidi library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PortMidi.

%package tools
Summary:	Tools to configure and use portmidi
Summary(pl.UTF-8):	Narzędzia do konfiguracji i używania portmidi
Group:		Applications/Multimedia
Requires:	%{name} = %{epoch}:%{version}-%{release}
%if %{with jni}
Requires:	jre >= 1.5
Requires:	jpackage-utils
%endif

%description tools
Tools to configure and use portmidi.

%description tools -l pl.UTF-8
Narzędzia do konfiguracji i używania portmidi.

%prep
%setup -q

# Add shebang, lib and class path
%{__sed} -i -e 's|\.\./\.\./Release:\.\./\.\./Debug:\.\./\.\.|%{_libdir}/%{name}|' \
	pm_java/pmdefaults/pmdefaults

%{__sed} -i -e 's/^OUTPUT_DIRECTORY .*/OUTPUT_DIRECTORY = html/' Doxyfile

%build
export JAVA_HOME=%{java_home}
%cmake -B build \
	-DCMAKE_CXX_COMPILER="%{__cc}" \
	-DCMAKE_CXX_COMPILER_WORKS=1 \
	%{?with_jni:-DBUILD_JAVA_NATIVE_INTERFACE=ON} \
	%{?with_jni:-DBUILD_PMDEFAULTS=ON} \
	-DBUILD_PORTMIDI_TESTS=ON

%{__make} -C build

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_datadir}/icons/hicolor/128x128/apps,%{_desktopdir}}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Install the test applications
for app in latency midiclock midithread midithru mm pmlist ; do
	install build/pm_test/$app $RPM_BUILD_ROOT%{_libdir}/%{name}
done

%if %{with jni}
# PLD's jni library location is different
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libpmjni.so* $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -p pm_java/pmdefaults/pmdefaults.jar $RPM_BUILD_ROOT%{_libdir}/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}
install pm_java/pmdefaults/pmdefaults $RPM_BUILD_ROOT%{_bindir}

# pmdefaults icon
cp -p pm_java/pmdefaults/pmdefaults-icon.png \
	$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps

# desktop file
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt README.txt license.txt pm_linux/README_LINUX.txt
%attr(755,root,root) %{_libdir}/libportmidi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libportmidi.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libportmidi.so
%{_includedir}/pmutil.h
%{_includedir}/portmidi.h
%{_includedir}/porttime.h
%{_pkgconfigdir}/portmidi.pc
%{_libdir}/cmake/PortMidi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc html/docs/*
%endif

%files tools
%defattr(644,root,root,755)
%doc pm_java/pmdefaults/README.txt
%dir %{_libdir}/portmidi
%attr(755,root,root) %{_libdir}/portmidi/latency
%attr(755,root,root) %{_libdir}/portmidi/midiclock
%attr(755,root,root) %{_libdir}/portmidi/midithread
%attr(755,root,root) %{_libdir}/portmidi/midithru
%attr(755,root,root) %{_libdir}/portmidi/mm
%attr(755,root,root) %{_libdir}/portmidi/pmlist
%if %{with jni}
%attr(755,root,root) %{_bindir}/pmdefaults
%attr(755,root,root) %{_libdir}/portmidi/libpmjni.so.*.*.*
%attr(755,root,root) %{_libdir}/portmidi/libpmjni.so.2
%attr(755,root,root) %{_libdir}/portmidi/libpmjni.so
%attr(755,root,root) %{_libdir}/portmidi/pmdefaults.jar
%{_desktopdir}/pmdefaults.desktop
%{_iconsdir}/hicolor/128x128/apps/pmdefaults-icon.png
%endif
