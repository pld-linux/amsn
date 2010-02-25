# TODO
# - Requires: /bin/bash /bin/sh /usr/bin/env /usr/bin/perl
# - mv languages instead handling specially in find-lang.sh, send to upstream
Summary:	MSN Messenger clone for Linux
Summary(de.UTF-8):	MSN Messenger-Klon für Linux
Summary(fr.UTF-8):	Clône MSN Messenger pour Linux
Summary(pl.UTF-8):	Klon MSN Messengera dla Linuksa
Name:		amsn
Version:	0.98.1
Release:	2.4
License:	GPL
Group:		Applications/Communications
Source0:	http://downloads.sourceforge.net/amsn/%{name}-%{version}.tar.gz
# Source0-md5:	8c608673a4e920b83cc9f41c2cb837dc
Source1:	find-lang.sh
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-libpng.patch
Patch3:		%{name}-bwidget.patch
Patch4:		%{name}-no-exact-http.patch
Patch5:		%{name}-songbird-exception.patch
URL:		http://www.amsn-project.net/
BuildRequires:	farsight2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.4
BuildRequires:	libstdc++-devel
BuildRequires:	libv4l-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.517
BuildRequires:	sed >= 4.0
BuildRequires:	tcl-devel >= 8.4
BuildRequires:	tk-devel >= 8.4
BuildRequires:	which
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	hicolor-icon-theme
# IM's convert is needed to display pictures (buddy icons).
Requires:	ImageMagick
Requires:	tcl >= 8.5.7
# MSN Protocol 9 won't let you in without SSL anymore.
Requires:	tcl-tls
Requires:	tcllib
Requires:	tk >= 8.4
Requires:	tk-BWidget >= 1.8.0-2
Requires:	xdg-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		find_lang 	%{SOURCE1} %{buildroot}

%description
This is Tcl/Tk clone that implements the Microsoft Messenger (MSN) for
Unix, Windows, or Macintosh platforms. It supports file transfers,
groups, and many more features.

%description -l de.UTF-8
amsn ist ein Microsoft Messenger (MSN) Client für UNIX, Windows und
Macintosh, der in Tcl/Tk geschrieben ist. Es unterstützt
Dateiübertragungen, Gruppen uvm.

%description -l fr.UTF-8
amsn est un client Microsoft Messenger (MSN) pour UNIX, Windows et
Macintosh écrit en Tcl/Tk. Il supporte les tranferts de fichiers, les
groupes et beaucoup d'autres possibilités.

%description -l pl.UTF-8
amsn to klient Microsoft Messengera (MSN) dla Uniksów, Windows i
Macintosha napisany w Tcl/Tk. Obsługuje przesyłanie plików, grupy i
wiele więcej możliwości.

%package plugins
Summary:	Plugins for aMSN
Group:		Applications/Networking
URL:		http://amsn.sourceforge.net/plugins.php
Requires:	%{name} = %{version}-%{release}

%description plugins
Extra plugins for amsn to enable drawing Ink, send and receive Nudges,
view the last lines of a recent chat when opening a new one and create
snapshots with your webcam to use as your display picture.

%prep
%setup -q

# undos some source files
find -name '*.tcl' -print0 | xargs -0 sed -i -e 's,\r$,,'

rm -r utils/BWidget-1.9.0
rm -r skins/default/winicons
rm -r skins/"Dark Matter 4.0"/winicons
rm -r plugins/music/MusicWin

# for webcam to work these paths need to be added because we move libs around
%{__sed} -i 's#\.\./libng/plugins#%{tcl_sitearch}/capture/libng/plugins#' utils/linux/capture/libng/grab-ng.c
%{__sed} -i 's#\.\./libng/contrib-plugins#%{tcl_sitearch}/capture/libng/contrib-plugins#' utils/linux/capture/libng/grab-ng.c

%{__sed} -i 's#mozilla#firefox#' config.tcl
%{__sed} -i 's#my_filemanager open#xdg-open#' config.tcl
%{__sed} -i 's#env(HOME) amsn_received#env(HOME) Desktop#' config.tcl
%{__sed} -i 's# utils/bwidget1.8.0##' Makefile.in

%{__sed} -i 's#set program_dir \[file dirname \[info script\]\]#set program_dir "%{_datadir}/%{name}/"#' amsn amsn-remote amsn-remote-CLI

%{__sed} -i 's#`locate .*`##' configure

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
# NOTE: enable debug allows us to keep debug symbols in -debuginfo package
%configure \
	--enable-debug \
	CFLAGS="%{rpmcflags}"
%{__make} \
	verbose=yes

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_iconsdir}/hicolor,%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/amsn $RPM_BUILD_ROOT%{_bindir}/amsn
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/amsn-remote $RPM_BUILD_ROOT%{_bindir}/amsn-remote
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/amsn-remote-CLI $RPM_BUILD_ROOT%{_bindir}/amsn-remote-CLI

rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/base64
#rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/http
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/log
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/sha1
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/snit
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/uri
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/docs
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/{AGREEMENT,FAQ,GNUGPL,INSTALL,remote.help,TODO}
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/{CREDITS,HELP,README}
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/lang/{*.*,LANG-HOWTO,sortlang}

install -d $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/linux/* $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/TkCximage $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/webcamsn $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/tcl_siren $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/tclISF $RPM_BUILD_ROOT%{tcl_sitearch}
#mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/gupnp $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/farsight $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/asyncresolver $RPM_BUILD_ROOT%{tcl_sitearch}

mv $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_desktopdir}}/%{name}.desktop
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/desktop-icons/* $RPM_BUILD_ROOT%{_iconsdir}/hicolor
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/desktop-icons
rm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

# docs in docs
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/*/test.tcl

%find_lang %{name}

grep /plugins/ %{name}.lang > %{name}-plugins.lang
sed -i -e '/plugins/d' %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc FAQ HELP README TODO CREDITS
%attr(755,root,root) %{_bindir}/amsn
%attr(755,root,root) %{_bindir}/amsn-remote
%attr(755,root,root) %{_bindir}/amsn-remote-CLI

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.tcl
%{_datadir}/%{name}/hotmlog.htm

# langlist explains the language codes used
%{_datadir}/%{name}/langlist

%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/skins
%{_datadir}/%{name}/utils

%{_iconsdir}/hicolor/*/apps/*.png
%{_desktopdir}/%{name}.desktop

%dir %{tcl_sitearch}/*
%{tcl_sitearch}/*/*.tcl
%attr(755,root,root) %{tcl_sitearch}/*/*.so
%dir %{tcl_sitearch}/capture/libng
%dir %{tcl_sitearch}/capture/libng/plugins
%attr(755,root,root) %{tcl_sitearch}/capture/libng/plugins/*.so

%files plugins -f %{name}-plugins.lang
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/plugins/ColoredNicks
%{_datadir}/%{name}/plugins/ColoredNicks/*.tcl
%{_datadir}/%{name}/plugins/ColoredNicks/*.xml

%dir %{_datadir}/%{name}/plugins/MSNGameTTT
%{_datadir}/%{name}/plugins/MSNGameTTT/*.tcl
%{_datadir}/%{name}/plugins/MSNGameTTT/*.xml
%{_datadir}/%{name}/plugins/MSNGameTTT/pixmaps

%dir %{_datadir}/%{name}/plugins/SearchContact
%{_datadir}/%{name}/plugins/SearchContact/*.tcl
%{_datadir}/%{name}/plugins/SearchContact/*.xml
%{_datadir}/%{name}/plugins/SearchContact/pixmaps

%dir %{_datadir}/%{name}/plugins/WebcamShooter
%{_datadir}/%{name}/plugins/WebcamShooter/*.tcl
%{_datadir}/%{name}/plugins/WebcamShooter/*.xml

%dir %{_datadir}/%{name}/plugins/Notes
%{_datadir}/%{name}/plugins/Notes/*.tcl
%{_datadir}/%{name}/plugins/Notes/*.xml

%dir %{_datadir}/%{name}/plugins/Nudge
%{_datadir}/%{name}/plugins/Nudge/*.tcl
%{_datadir}/%{name}/plugins/Nudge/*.xml
%{_datadir}/%{name}/plugins/Nudge/*.wav

%dir %{_datadir}/%{name}/plugins/inkdraw
%{_datadir}/%{name}/plugins/inkdraw/*.tcl
%{_datadir}/%{name}/plugins/inkdraw/*.xml
%{_datadir}/%{name}/plugins/inkdraw/pixmaps
%{_datadir}/%{name}/plugins/inkdraw/pencils

%dir %{_datadir}/%{name}/plugins/music
%{_datadir}/%{name}/plugins/music/*.tcl
%{_datadir}/%{name}/plugins/music/*.xml
%{_datadir}/%{name}/plugins/music/*.txt
%{_datadir}/%{name}/plugins/music/info*
%{_datadir}/%{name}/plugins/music/display_and_send.scpt
%{_datadir}/%{name}/plugins/music/pixmaps

%dir %{_datadir}/%{name}/plugins/remind
%{_datadir}/%{name}/plugins/remind/*.tcl
%{_datadir}/%{name}/plugins/remind/*.xml

%dir %{_datadir}/%{name}/plugins/winks
%{_datadir}/%{name}/plugins/winks/*.tcl
%{_datadir}/%{name}/plugins/winks/*.xml
%{_datadir}/%{name}/plugins/winks/*.txt
%{_datadir}/%{name}/plugins/winks/pixmaps
