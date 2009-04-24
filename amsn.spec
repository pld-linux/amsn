# TODO
# - %lang tags: /usr/lib/amsn/lang/langfr_CA ..
Summary:	MSN Messenger clone for Linux
Summary(de.UTF-8):	MSN Messenger-Klon für Linux
Summary(fr.UTF-8):	Clône MSN Messenger pour Linux
Summary(pl.UTF-8):	Klon MSN Messengera dla Linuksa
Name:		amsn
Version:	0.97
Release:	1
Epoch:		0
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/amsn/%{name}-%{version}.tar.gz
# Source0-md5:	0ae903f6cac24c042f4ef74b5015ea88
Patch0:		%{name}-desktop.patch
URL:		http://www.amsn-project.net/
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	sed >= 4.0
BuildRequires:	tcl-devel >= 8.4
BuildRequires:	tk-devel >= 8.4
Requires(post,postun):	hicolor-icon-theme
# IM's convert is needed to display pictures (buddy icons).
Requires:	ImageMagick
Requires:	tcl >= 8.4
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

%prep
%setup -q

# undos some source files
find -name '*.tcl' -print0 | xargs -0 sed -i -e 's,\r$,,'

%patch0 -p1

# MS-DOS executable PE for MS Windows (GUI) Intel 80386 32-bit
rm -f utils/*/*/*.exe

%build
%configure \
	CFLAGS="%{rpmcflags}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_iconsdir}/hicolor/,%{_pixmapsdir},%{_desktopdir}}

# FIXME: FHS?
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT%{_bindir} \
	dstdir=$RPM_BUILD_ROOT%{_libdir} \
	slnkdir=$RPM_BUILD_ROOT%{_bindir}

install %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
rm $RPM_BUILD_ROOT%{_libdir}/applications/amsn.desktop
rm -r $RPM_BUILD_ROOT%{_libdir}/pixmaps
mv $RPM_BUILD_ROOT%{_libdir}/amsn/desktop-icons/* $RPM_BUILD_ROOT%{_iconsdir}/hicolor
rm -r $RPM_BUILD_ROOT%{_libdir}/amsn/desktop-icons
ln -s %{_iconsdir}/hicolor/48x48/apps/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}

for f in amsn{,-remote{,-CLI}}; do
	rm $RPM_BUILD_ROOT%{_bindir}/$f
	ln -s ../%{_lib}/%{name}/$f $RPM_BUILD_ROOT%{_bindir}
done

# remove junk
rm $RPM_BUILD_ROOT%{_libdir}/amsn/amsn.desktop
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/lang/LANG-HOWTO
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/lang/convert.tcl

# docs in docs
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/docs
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/{AGREEMENT,CREDITS,GNUGPL,INSTALL,README,HELP,FAQ,TODO}
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/utils/*/test.tcl

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc FAQ GNUGPL HELP README TODO CREDITS
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/amsn
%attr(755,root,root) %{_libdir}/%{name}/amsn-remote*

%{_libdir}/%{name}/*.tcl
%{_libdir}/%{name}/remote.help
%{_libdir}/%{name}/hotmlog.htm
# TODO: %lang
%{_libdir}/%{name}/lang
%{_libdir}/%{name}/langlist

%dir %{_libdir}/%{name}/plugins

%{_libdir}/%{name}/plugins/Nudge
%{_libdir}/%{name}/plugins/PowerTool
%{_libdir}/%{name}/plugins/WebcamShooter
%{_libdir}/%{name}/plugins/inkdraw
%{_libdir}/%{name}/plugins/remind
%{_libdir}/%{name}/plugins/winks

%{_libdir}/%{name}/skins

%dir %{_libdir}/%{name}/utils
%{_libdir}/%{name}/utils/base64
%{_libdir}/%{name}/utils/bwidget1.8.0
%{_libdir}/%{name}/utils/combobox
%{_libdir}/%{name}/utils/contentmanager
%{_libdir}/%{name}/utils/dpbrowser
%{_libdir}/%{name}/utils/drawboard
%{_libdir}/%{name}/utils/framec
%{_libdir}/%{name}/utils/http2.4
%{_libdir}/%{name}/utils/log
%{_libdir}/%{name}/utils/pixmapmenu
%{_libdir}/%{name}/utils/pixmapscroll
%{_libdir}/%{name}/utils/scalable-bg
%{_libdir}/%{name}/utils/sexytile
%{_libdir}/%{name}/utils/sha1
%{_libdir}/%{name}/utils/snit
%{_libdir}/%{name}/utils/uri

%dir %{_libdir}/%{name}/utils/TkCximage
%attr(755,root,root) %{_libdir}/%{name}/utils/TkCximage/*.so
%{_libdir}/%{name}/utils/TkCximage/pkgIndex.tcl

%dir %{_libdir}/%{name}/utils/linux
%dir %{_libdir}/%{name}/utils/linux/capture
%{_libdir}/%{name}/utils/linux/capture/pkgIndex.tcl
%attr(755,root,root) %{_libdir}/%{name}/utils/linux/capture/*.so

%dir %{_libdir}/%{name}/utils/linux/capture/libng
%dir %{_libdir}/%{name}/utils/linux/capture/libng/plugins
%attr(755,root,root) %{_libdir}/%{name}/utils/linux/capture/libng/plugins/*.so

%dir %{_libdir}/%{name}/utils/linux/linflash
%attr(755,root,root) %{_libdir}/%{name}/utils/linux/linflash/*.so
%{_libdir}/%{name}/utils/linux/linflash/pkgIndex.tcl

%dir %{_libdir}/%{name}/utils/linux/traydock
%attr(755,root,root) %{_libdir}/%{name}/utils/linux/traydock/libtray.so
%{_libdir}/%{name}/utils/linux/traydock/pkgIndex.tcl

%dir %{_libdir}/%{name}/utils/tcl_siren
%{_libdir}/%{name}/utils/tcl_siren/pkgIndex.tcl
%attr(755,root,root) %{_libdir}/%{name}/utils/tcl_siren/*.so

%dir %{_libdir}/%{name}/utils/webcamsn
%{_libdir}/%{name}/utils/webcamsn/pkgIndex.tcl
%attr(755,root,root) %{_libdir}/%{name}/utils/webcamsn/*.so

%{_iconsdir}/hicolor/*/apps/*.png
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
