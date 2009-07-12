Summary:	MSN Messenger clone for Linux
Summary(de.UTF-8):	MSN Messenger-Klon für Linux
Summary(fr.UTF-8):	Clône MSN Messenger pour Linux
Summary(pl.UTF-8):	Klon MSN Messengera dla Linuksa
Name:		amsn
Version:	0.97.2
Release:	3
Epoch:		0
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/amsn/%{name}-%{version}.tar.gz
# Source0-md5:	c6c2e9c016c39dfbae80028a3c745419
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-tkcximage.patch
Patch2:		%{name}-paths.patch
URL:		http://www.amsn-project.net/
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	rpmbuild(macros) >= 1.517
BuildRequires:	sed >= 4.0
BuildRequires:	tcl-devel >= 8.4
BuildRequires:	tk-devel >= 8.4
Requires(post,postun):	hicolor-icon-theme
# IM's convert is needed to display pictures (buddy icons).
Requires:	ImageMagick
Requires:	tcl >= 8.5.7
Requires:	tcl-bwidget
Requires:	tcllib
# MSN Protocol 9 won't let you in without SSL anymore.
Requires:	tcl-tls
Requires:	tk >= 8.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

rm -r utils/bwidget1.8.0
rm -r skins/default/winicons

# for webcam to work these paths need to be added because we move libs around
%{__sed} -i 's#\.\./libng/plugins#%{tcl_sitearch}/capture/libng/plugins#' utils/linux/capture/libng/grab-ng.c
%{__sed} -i 's#\.\./libng/contrib-plugins#%{tcl_sitearch}/capture/libng/contrib-plugins#' utils/linux/capture/libng/grab-ng.c

%{__sed} -i 's#mozilla#firefox#' config.tcl
%{__sed} -i 's#my_filemanager open#xdg-open#' config.tcl
%{__sed} -i 's#env(HOME) amsn_received#env(HOME) Desktop#' config.tcl
%{__sed} -i 's# utils/bwidget1.8.0##' Makefile.in

%{__sed} -i 's#set program_dir \[file dirname \[info script\]\]#set program_dir "%{_datadir}/amsn/"#' amsn amsn-remote amsn-remote-CLI

%patch0 -p1
%patch1 -p2
%patch2 -p1

# MS-DOS executable PE for MS Windows (GUI) Intel 80386 32-bit
rm -f utils/*/*/*.exe

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
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/http2.4
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
mv $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_desktopdir}}/%{name}.desktop
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/desktop-icons/* $RPM_BUILD_ROOT%{_iconsdir}/hicolor
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/desktop-icons
ln -sf %{_iconsdir}/hicolor/48x48/apps/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}

# docs in docs
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/utils/*/test.tcl

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
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
%dir %{_datadir}/%{name}/lang
%{_datadir}/%{name}/lang/langen
%lang(sq) %{_datadir}/%{name}/lang/langal
%lang(ca) %{_datadir}/%{name}/lang/langca
%lang(ca) %{_datadir}/%{name}/lang/langca_VC
%lang(cs) %{_datadir}/%{name}/lang/langcs
%lang(cy) %{_datadir}/%{name}/lang/langcy
%lang(da) %{_datadir}/%{name}/lang/langda
%lang(de) %{_datadir}/%{name}/lang/langde
%lang(et) %{_datadir}/%{name}/lang/langee
%lang(el) %{_datadir}/%{name}/lang/langel
%lang(es) %{_datadir}/%{name}/lang/langes
%lang(eu) %{_datadir}/%{name}/lang/langeu
%lang(fi) %{_datadir}/%{name}/lang/langfi
%lang(fr) %{_datadir}/%{name}/lang/langfr
%lang(fr_CA) %{_datadir}/%{name}/lang/langfr_CA
%lang(fy) %{_datadir}/%{name}/lang/langfri
%lang(gl) %{_datadir}/%{name}/lang/langglg
%lang(el) %{_datadir}/%{name}/lang/langgr2
%lang(hu) %{_datadir}/%{name}/lang/langhu
%lang(id) %{_datadir}/%{name}/lang/langid
%lang(is) %{_datadir}/%{name}/lang/langis
%lang(it) %{_datadir}/%{name}/lang/langit
%lang(ko) %{_datadir}/%{name}/lang/langko
%lang(lt) %{_datadir}/%{name}/lang/langlt
%lang(mk) %{_datadir}/%{name}/lang/langmk
%lang(mt) %{_datadir}/%{name}/lang/langmt
%lang(nl) %{_datadir}/%{name}/lang/langnl
%lang(nb) %{_datadir}/%{name}/lang/langno
%lang(oc) %{_datadir}/%{name}/lang/langoc
%lang(pl) %{_datadir}/%{name}/lang/langpl
%lang(pt) %{_datadir}/%{name}/lang/langpt
%lang(pt_BR) %{_datadir}/%{name}/lang/langpt_BR
%lang(ro) %{_datadir}/%{name}/lang/langro
%lang(ru) %{_datadir}/%{name}/lang/langru
%lang(sk) %{_datadir}/%{name}/lang/langsk
%lang(sl) %{_datadir}/%{name}/lang/langsl
%lang(sr) %{_datadir}/%{name}/lang/langsr
%lang(sv) %{_datadir}/%{name}/lang/langsv
%lang(tr) %{_datadir}/%{name}/lang/langtr
%lang(zh_CN) %{_datadir}/%{name}/lang/langzh-CN
%lang(zh_TW) %{_datadir}/%{name}/lang/langzh-TW

# no ISO 639-1 code present
%lang(NONE) %{_datadir}/%{name}/lang/langast

%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/skins
%{_datadir}/%{name}/utils

%{_iconsdir}/hicolor/*/apps/*.png
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png

%dir %{tcl_sitearch}/*
%{tcl_sitearch}/*/*.tcl
%attr(755,root,root) %{tcl_sitearch}/*/*.so
%dir %{tcl_sitearch}/capture/libng
%dir %{tcl_sitearch}/capture/libng/plugins
%attr(755,root,root) %{tcl_sitearch}/capture/libng/plugins/*.so

%files plugins
%defattr(644,root,root,755)
%{_datadir}/%{name}/plugins/*
