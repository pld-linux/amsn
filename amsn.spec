Summary:	MSN Messenger clone for Linux
Summary(de.UTF-8):	MSN Messenger-Klon für Linux
Summary(fr.UTF-8):	Clône MSN Messenger pour Linux
Summary(pl.UTF-8):	Klon MSN Messengera dla Linuksa
Name:		amsn
Version:	0.97
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/amsn/%{name}-%{version}.tar.gz
# Source0-md5:	0ae903f6cac24c042f4ef74b5015ea88
Patch0:		%{name}-desktop.patch
URL:		http://amsn.sourceforge.net/
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
groups, and many more features. Visit http://amsn.sourceforge.net/ for
details. This is an ongoing project, and it is already going pretty
well.

%description -l de.UTF-8
amsn ist ein Microsoft Messenger (MSN) Client für UNIX, Windows und
Macintosh, der in Tcl/Tk geschrieben ist. Es unterstützt
Dateiübertragungen, Gruppen uvm. Begeben Sie sich auf
http://amsn.sourceforge.net/ um mehr über dieses Projekt zu erfahren.

%description -l fr.UTF-8
amsn est un client Microsoft Messenger (MSN) pour UNIX, Windows et
Macintosh écrit en Tcl/Tk. Il supporte les tranferts de fichiers, les
groupes et beaucoup d'autres possibilités. Visitez
http://amsn.sourceforge.net/ pour de plus amples détails.

%description -l pl.UTF-8
amsn to klient Microsoft Messengera (MSN) dla Uniksów, Windows i
Macintosha napisany w Tcl/Tk. Obsługuje przesyłanie plików, grupy i
wiele więcej możliwości - szczegóły pod adresem
<http://amsn.sourceforge.net/>. Projekt jest nadal rozwijany i już
działa całkiem dobrze.

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
rm -f $RPM_BUILD_ROOT%{_libdir}/applications/amsn.desktop

rm -rf $RPM_BUILD_ROOT%{_libdir}/pixmaps
ln -s %{_iconsdir}/hicolor/48x48/apps/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}

for f in amsn{,-remote{,-CLI}}; do
	rm $RPM_BUILD_ROOT%{_bindir}/$f
	ln -s ../%{_lib}/%{name}/$f $RPM_BUILD_ROOT%{_bindir}
done

# remove junk
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/amsn.desktop
# docs in docs
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/docs
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/{AGREEMENT,CREDITS,GNUGPL,INSTALL,README,HELP,FAQ,TODO}
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/utils/*/test.tcl

mv $RPM_BUILD_ROOT%{_libdir}/amsn/desktop-icons/* $RPM_BUILD_ROOT%{_iconsdir}/hicolor/
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/desktop-icons

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
%{_libdir}/%{name}/a[!m]*
%{_libdir}/%{name}/amsn[!-]*
%{_libdir}/%{name}/[!a]*
%attr(755,root,root) %{_libdir}/%{name}/amsn
%attr(755,root,root) %{_libdir}/%{name}/amsn-remote*

%{_iconsdir}/hicolor/*/apps/*.png
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
