Summary:	Portable Real-Time MIDI library
Summary(pl.UTF-8):	Przenośna biblioteka MIDI czasu rzeczywistego
Name:		portmidi
Version:	20070117
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	http://www.cs.cmu.edu/~music/portmusic/portmidi/portmidi17Jan07.zip
# Source0-md5:	2b21759b2ce05fde9d50842252ce6418
Patch0:		%{name}-make.patch
URL:		http://www.cs.cmu.edu/~music/portmusic/portmidi/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	libtool
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

%package static
Summary:	Static PortMidi library
Summary(pl.UTF-8):	Statyczna biblioteka PortMidi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PortMidi library.

%description static -l pl.UTF-8
Statyczna biblioteka PortMidi.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} -f pm_linux/Makefile \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}" \
	PMFLAGS="-DNEWBUFFER%{?debug: -DPM_CHECK_ERRORS}" \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -f pm_linux/Makefile install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt README.txt license.txt pm_linux/README_LINUX.txt
%attr(755,root,root) %{_libdir}/libportmidi.so.*.*.*
%attr(755,root,root) %{_libdir}/libporttime.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libportmidi.so
%attr(755,root,root) %{_libdir}/libporttime.so
%{_libdir}/libportmidi.la
%{_libdir}/libporttime.la
%{_includedir}/pmutil.h
%{_includedir}/portmidi.h
%{_includedir}/porttime.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libportmidi.a
%{_libdir}/libporttime.a
