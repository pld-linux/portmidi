#
# TODO: fix build doxygen documentaton
#
Summary:	Portable Real-Time MIDI library
Summary(pl.UTF-8):	Przenośna biblioteka MIDI czasu rzeczywistego
Name:		portmidi
Version:	217
Release:	5
License:	MIT-like
Group:		Libraries
Source0:	http://downloads.sourceforge.net/portmedia/%{version}/%{name}-src-%{version}.zip
# Source0-md5:	03f46fd3947e2ef4c8c465baaf832241
Source1:	pmdefaults.desktop
Patch0:		%{name}-cmake.patch
Patch1:		%{name}-format.patch
URL:		http://portmedia.sourceforge.net/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	cmake >= 2.6
#BuildRequires:	doxygen
BuildRequires:	jdk >= 1.5
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	sed >= 4.0
#BuildRequires:	texlive-format-pdflatex
#BuildRequires:	texlive-latex-extend
#BuildRequires:	texlive-xetex
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Portable Real-Time MIDI library.

%description -l pl.UTF-8
Przenośna biblioteka MIDI czasu rzeczywistego.

%package devel
Summary:	Header files for PortMidi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PortMidi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib-devel >= 0.9
Obsoletes:	portmidi-static

%description devel
Header files for PortMidi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PortMidi.

%package tools
Summary:	Tools to configure and use portmidi
Summary(pl.UTF-8):	Narzędzia do konfiguracji i używania portmidi
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	jre >= 1.5
Requires:	jpackage-utils

%description tools
Tools to configure and use portmidi.

%description tools -l pl.UTF-8
Narzędzia do konfiguracji i używania portmidi.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

# Add shebang, lib and class path
%{__sed} -i -e 's|^java|#!/bin/sh\njava \\\
	-Djava.library.path=%{_libdir}/%{name}/|' \
	-e 's|%{_javadir}/|%{_libdir}/%{name}/|' \
	pm_java/pmdefaults/pmdefaults

%build
export JAVA_HOME=%{java_home}
%cmake \
	-DCMAKE_CXX_COMPILER_WORKS=1 -DCMAKE_CXX_COMPILER="%{__cc}" \
	-DCMAKE_CACHEFILE_DIR=%{_builddir}/%{name}/build \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DVERSION=%{version}

%{__make} -j 1

# TODO: fix "undefined refernce" errors
%if 0
# Build the doxygen documentation
doxygen
%{__make} -C latex
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_datadir}/icons/hicolor/128x128/apps,%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Install the test applications
for app in latency midiclock midithread midithru mm qtest sysex test; do
	install build/PLD/$app $RPM_BUILD_ROOT%{_libdir}/%{name}
done

# PLD's jni library location is different
mv $RPM_BUILD_ROOT%{_libdir}/libpmjni.so $RPM_BUILD_ROOT%{_libdir}/%{name}
mv $RPM_BUILD_ROOT%{_javadir}/pmdefaults.jar $RPM_BUILD_ROOT%{_libdir}/%{name}

# pmdefaults icon
cp -a pm_java/pmdefaults/pmdefaults-icon.png \
	$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps

# desktop file
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

# remove duplicate library
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libportmidi_s.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt README.txt license.txt pm_linux/README_LINUX.txt
%attr(755,root,root) %{_libdir}/libportmidi.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libportmidi.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libportmidi.so
%{_includedir}/portmidi.h
%{_includedir}/porttime.h

%files tools
%defattr(644,root,root,755)
%doc pm_java/pmdefaults/README.txt pm_cl/*
%attr(755,root,root) %{_bindir}/pmdefaults
%dir %{_libdir}/portmidi
%attr(755,root,root) %{_libdir}/portmidi/latency
%attr(755,root,root) %{_libdir}/portmidi/libpmjni.so
%attr(755,root,root) %{_libdir}/portmidi/midiclock
%attr(755,root,root) %{_libdir}/portmidi/midithread
%attr(755,root,root) %{_libdir}/portmidi/midithru
%attr(755,root,root) %{_libdir}/portmidi/mm
%attr(755,root,root) %{_libdir}/portmidi/pmdefaults.jar
%attr(755,root,root) %{_libdir}/portmidi/qtest
%attr(755,root,root) %{_libdir}/portmidi/sysex
%attr(755,root,root) %{_libdir}/portmidi/test
%{_desktopdir}/pmdefaults.desktop
%{_iconsdir}/hicolor/128x128/apps/pmdefaults-icon.png
