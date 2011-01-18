#
# TODO: fix build doxygen documentaton
#
Summary:	Portable Real-Time MIDI library
Summary(pl.UTF-8):	Przenośna biblioteka MIDI czasu rzeczywistego
Name:		portmidi
Version:	217
Release:	0.1
License:	MIT-like
Group:		Libraries
Source0:	http://downloads.sourceforge.net/portmedia/%{version}/%{name}-src-%{version}.zip
# Source0-md5:	03f46fd3947e2ef4c8c465baaf832241
Patch0:		%{name}-cmake.patch
URL:		http://portmedia.sourceforge.net/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	cmake
#BuildRequires:	doxygen
BuildRequires:	jdk >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.600
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

%description devel
Header files for PortMidi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PortMidi.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
export JAVA_HOME=%{java_home}
%cmake \
	-DCMAKE_CACHEFILE_DIR=%{_builddir}/%{name}/build

%{__make} -j 1

# TODO: fix "undefined refernce" errors
%if 0
# Build the doxygen documentation:
doxygen
cd latex
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt README.txt license.txt pm_linux/README_LINUX.txt
%attr(755,root,root) %{_bindir}/pmdefaults
%attr(755,root,root) %ghost %{_libdir}/libportmidi.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpmjni.so
%attr(755,root,root) %{_libdir}/libportmidi.so
%attr(755,root,root) %{_libdir}/libportmidi_s.so
%{_includedir}/portmidi.h
%{_includedir}/porttime.h
