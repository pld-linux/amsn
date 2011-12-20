# TODO
# - Requires: /bin/bash /bin/sh /usr/bin/env /usr/bin/perl  ... etc in music plugin, subpackage it?
# - use mv for language codes fix, instead handling specially in find-lang.sh, send to upstream
Summary:	MSN Messenger clone for Linux
Summary(de.UTF-8):	MSN Messenger-Klon für Linux
Summary(fr.UTF-8):	Clône MSN Messenger pour Linux
Summary(pl.UTF-8):	Klon MSN Messengera dla Linuksa
Name:		amsn
Version:	0.98.4
Release:	3
License:	GPL
Group:		Applications/Communications
Source0:	http://downloads.sourceforge.net/project/amsn/amsn/%{version}/%{name}-%{version}-src.tar.gz
# Source0-md5:	3cf69c4a7773888cea854927c83b9cfb
Source1:	find-lang.sh
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-paths.patch
Patch2:		useV4L2.patch
Patch3:		%{name}-bwidget.patch
Patch4:		ca-certificates.patch
Patch6:		%{name}-disable-autoupdate.patch
URL:		http://www.amsn-project.net/
BuildRequires:	farsight2-devel
BuildRequires:	gupnp-igd-devel
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
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
# default skin is always needed, as it contains images if extra skin misses something
Requires:	%{name}-skin-default
# IM's convert is needed to display pictures (buddy icons).
Requires:	ImageMagick
Requires:	ca-certificates-update
Requires:	tcl >= 8.5.7
# MSN Protocol 9 won't let you in without SSL anymore.
Requires:	tcl-tls
Requires:	tcllib
Requires:	tk >= 8.4
Requires:	tk-BWidget >= 1.8.0-2
Requires:	xdg-utils
Obsoletes:	amsn-plugin-chameleon
%if 0
# new deps
Requires:	tcl-snack
Requires:	tclsoap
Requires:	tkdnd
%endif
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

%{__rm} -r utils/BWidget-1.9.0
%{__rm} -r plugins/music/MusicWin
%{__rm} plugins/music/*.scpt
%{__rm} plugins/amsnplus/snapshot

# skins in amsn-skins.spec
%{__rm} -r skins/*

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
%patch6 -p1

%build
# NOTE: enable debug allows us to keep debug symbols in -debuginfo package
%configure \
	--enable-debug \
	CFLAGS="%{rpmcflags}"
%{__make} \
	verbose=yes

# build with our flags
#%{__cc} plugins/amsnplus/snapshot.c -o plugins/amsnplus/snapshot %{rpmcflags} %{rpmldflags} `imlib-config --cflags` `imlib-config --libs`

%install
%{__rm} -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_iconsdir}/hicolor,%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/amsn $RPM_BUILD_ROOT%{_bindir}/amsn
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/amsn-remote $RPM_BUILD_ROOT%{_bindir}/amsn-remote
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/amsn-remote-CLI $RPM_BUILD_ROOT%{_bindir}/amsn-remote-CLI

#install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/amsnplus
#mv $RPM_BUILD_ROOT{%{_datadir},%{_libdir}}/%{name}/plugins/amsnplus/snapshot

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/base64
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/http
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/log
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/sha1
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/snit
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/uri
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/docs
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/{AGREEMENT,FAQ,GNUGPL,INSTALL,remote.help,TODO}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/{CREDITS,HELP,README}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/lang/{*.*,LANG-HOWTO,sortlang}

install -d $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/linux/* $RPM_BUILD_ROOT%{tcl_sitearch}
rmdir $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/linux
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/TkCximage $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/webcamsn $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/tcl_siren $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/tclISF $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/gupnp $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/farsight $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/asyncresolver $RPM_BUILD_ROOT%{tcl_sitearch}

mv $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_desktopdir}}/%{name}.desktop
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/desktop-icons/* $RPM_BUILD_ROOT%{_iconsdir}/hicolor
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/desktop-icons
%{__rm} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/amsnplus/{snapshot.c,Makefile}

#%{_datadir}/%{name}/plugins/growl/styles/aMSN.growlStyle/Contents/Resources/default.css
#%{_datadir}/%{name}/plugins/growl/styles/aMSNMac.growlStyle/Contents/Info.plist
#%{_datadir}/%{name}/plugins/address_book/utils/addressbook/pkgIndex.tcl

# docs in docs
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/*/test.tcl

%find_lang %{name}

%{__grep} /plugins/ %{name}.lang > %{name}-plugins.lang
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
%dir %{_datadir}/%{name}/skins
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
%{_datadir}/%{name}/plugins/DBusStateChanger
%{_datadir}/%{name}/plugins/DualDisplayPicture
%{_datadir}/%{name}/plugins/LilyPondIM
%{_datadir}/%{name}/plugins/Restore
%{_datadir}/%{name}/plugins/SkinColor
%{_datadir}/%{name}/plugins/TeXIM
%{_datadir}/%{name}/plugins/Translate
%{_datadir}/%{name}/plugins/advancedconfigviewer
%{_datadir}/%{name}/plugins/camserv
%{_datadir}/%{name}/plugins/changeit
%{_datadir}/%{name}/plugins/dbusviewer
%{_datadir}/%{name}/plugins/desktop_integration
%{_datadir}/%{name}/plugins/devel
%{_datadir}/%{name}/plugins/emotes
%{_datadir}/%{name}/plugins/gename
%{_datadir}/%{name}/plugins/keepalive
%{_datadir}/%{name}/plugins/movewin
%{_datadir}/%{name}/plugins/notify
%{_datadir}/%{name}/plugins/organize_received
%{_datadir}/%{name}/plugins/sayit
%{_datadir}/%{name}/plugins/userstatus
%{_datadir}/%{name}/plugins/whatis
%{_datadir}/%{name}/plugins/ebuddykiller

# need to list resources manually due autogenerated lang resources
%dir %{_datadir}/%{name}/plugins/ColoredNicks
%{_datadir}/%{name}/plugins/ColoredNicks/*.tcl
%{_datadir}/%{name}/plugins/ColoredNicks/*.xml

%dir %{_datadir}/%{name}/plugins/MSNGameTTT
%{_datadir}/%{name}/plugins/MSNGameTTT/pixmaps
%{_datadir}/%{name}/plugins/MSNGameTTT/*.tcl
%{_datadir}/%{name}/plugins/MSNGameTTT/*.xml

%dir %{_datadir}/%{name}/plugins/SearchContact
%{_datadir}/%{name}/plugins/SearchContact/pixmaps
%{_datadir}/%{name}/plugins/SearchContact/*.tcl
%{_datadir}/%{name}/plugins/SearchContact/*.xml

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
%{_datadir}/%{name}/plugins/inkdraw/pixmaps
%{_datadir}/%{name}/plugins/inkdraw/*.tcl
%{_datadir}/%{name}/plugins/inkdraw/*.xml
%{_datadir}/%{name}/plugins/inkdraw/pencils

%dir %{_datadir}/%{name}/plugins/music
%{_datadir}/%{name}/plugins/music/pixmaps
%{_datadir}/%{name}/plugins/music/*.tcl
%{_datadir}/%{name}/plugins/music/*.xml
%{_datadir}/%{name}/plugins/music/*.txt
%{_datadir}/%{name}/plugins/music/info*

%dir %{_datadir}/%{name}/plugins/remind
%{_datadir}/%{name}/plugins/remind/*.tcl
%{_datadir}/%{name}/plugins/remind/*.xml

%dir %{_datadir}/%{name}/plugins/winks
%{_datadir}/%{name}/plugins/winks/pixmaps
%{_datadir}/%{name}/plugins/winks/*.tcl
%{_datadir}/%{name}/plugins/winks/*.xml
%{_datadir}/%{name}/plugins/winks/*.txt

%dir %{_datadir}/%{name}/plugins/FPSstats
%{_datadir}/%{name}/plugins/FPSstats/README
%{_datadir}/%{name}/plugins/FPSstats/pixmaps
%{_datadir}/%{name}/plugins/FPSstats/*.tcl
%{_datadir}/%{name}/plugins/FPSstats/*.xml

%dir %{_datadir}/%{name}/plugins/Invisibility
%{_datadir}/%{name}/plugins/Invisibility/Changelog
%{_datadir}/%{name}/plugins/Invisibility/*.tcl
%{_datadir}/%{name}/plugins/Invisibility/*.xml

%dir %{_datadir}/%{name}/plugins/Kryptonite
%{_datadir}/%{name}/plugins/Kryptonite/pixmaps
%{_datadir}/%{name}/plugins/Kryptonite/*.tcl
%{_datadir}/%{name}/plugins/Kryptonite/*.xml

%dir %{_datadir}/%{name}/plugins/SendRecents
%{_datadir}/%{name}/plugins/SendRecents/*.tcl
%{_datadir}/%{name}/plugins/SendRecents/*.xml

%dir %{_datadir}/%{name}/plugins/SpellCheck
%{_datadir}/%{name}/plugins/SpellCheck/Changelog.txt
%{_datadir}/%{name}/plugins/SpellCheck/ReadMe.txt
%{_datadir}/%{name}/plugins/SpellCheck/pixmaps
%{_datadir}/%{name}/plugins/SpellCheck/*.tcl
%{_datadir}/%{name}/plugins/SpellCheck/*.xml

%dir %{_datadir}/%{name}/plugins/actionsmenu
%{_datadir}/%{name}/plugins/actionsmenu/pixmaps
%{_datadir}/%{name}/plugins/actionsmenu/*.tcl
%{_datadir}/%{name}/plugins/actionsmenu/*.xml

%dir %{_datadir}/%{name}/plugins/address_book
%{_datadir}/%{name}/plugins/address_book/utils
%{_datadir}/%{name}/plugins/address_book/*.tcl
%{_datadir}/%{name}/plugins/address_book/*.xml

%dir %{_datadir}/%{name}/plugins/amsnplus
%{_datadir}/%{name}/plugins/amsnplus/readme
%{_datadir}/%{name}/plugins/amsnplus/pixmaps
%{_datadir}/%{name}/plugins/amsnplus/*.tcl
%{_datadir}/%{name}/plugins/amsnplus/*.xml

%dir %{_datadir}/%{name}/plugins/bugbuddy
%{_datadir}/%{name}/plugins/bugbuddy/CREDITS
%{_datadir}/%{name}/plugins/bugbuddy/*.tcl
%{_datadir}/%{name}/plugins/bugbuddy/*.xml

%dir %{_datadir}/%{name}/plugins/chameleon
%{_datadir}/%{name}/plugins/chameleon/*.tcl
%{_datadir}/%{name}/plugins/chameleon/*.xml

%dir %{_datadir}/%{name}/plugins/colorize
%{_datadir}/%{name}/plugins/colorize/*.tcl
%{_datadir}/%{name}/plugins/colorize/*.xml

%dir %{_datadir}/%{name}/plugins/countdown
%{_datadir}/%{name}/plugins/countdown/*.tcl
%{_datadir}/%{name}/plugins/countdown/*.xml

%dir %{_datadir}/%{name}/plugins/emoticons_importer
%{_datadir}/%{name}/plugins/emoticons_importer/*.tcl
%{_datadir}/%{name}/plugins/emoticons_importer/*.xml

%dir %{_datadir}/%{name}/plugins/games
%{_datadir}/%{name}/plugins/games/images
%{_datadir}/%{name}/plugins/games/*.tcl
%{_datadir}/%{name}/plugins/games/*.xml
%{_datadir}/%{name}/plugins/games/changelog
%{_datadir}/%{name}/plugins/games/developers.readme
%{_datadir}/%{name}/plugins/games/readme

%dir %{_datadir}/%{name}/plugins/glogs
%{_datadir}/%{name}/plugins/glogs/*.tcl
%{_datadir}/%{name}/plugins/glogs/*.xml

%dir %{_datadir}/%{name}/plugins/gnotify
%{_datadir}/%{name}/plugins/gnotify/pixmaps
%{_datadir}/%{name}/plugins/gnotify/*.tcl
%{_datadir}/%{name}/plugins/gnotify/*.xml

%dir %{_datadir}/%{name}/plugins/growl
%{_datadir}/%{name}/plugins/growl/styles
%{_datadir}/%{name}/plugins/growl/*.tcl
%{_datadir}/%{name}/plugins/growl/*.xml
%{_datadir}/%{name}/plugins/growl/*.png

%dir %{_datadir}/%{name}/plugins/jake
%{_datadir}/%{name}/plugins/jake/README
%{_datadir}/%{name}/plugins/jake/*.tcl
%{_datadir}/%{name}/plugins/jake/*.xml

%dir %{_datadir}/%{name}/plugins/openwith
%{_datadir}/%{name}/plugins/openwith/*.tcl
%{_datadir}/%{name}/plugins/openwith/*.xml

%dir %{_datadir}/%{name}/plugins/pop3
%{_datadir}/%{name}/plugins/pop3/pixmaps
%{_datadir}/%{name}/plugins/pop3/*.tcl
%{_datadir}/%{name}/plugins/pop3/*.xml

%dir %{_datadir}/%{name}/plugins/transparent
%{_datadir}/%{name}/plugins/transparent/*.tcl
%{_datadir}/%{name}/plugins/transparent/*.xml
