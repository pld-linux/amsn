Summary:	MSN Messenger clone for Linux
Summary(de):	MSN Messenger-Klon f�r Linux
Summary(fr):	Cl�ne MSN Messenger pour Linux
Summary(pl):	Klon MSN Messengera dla Linuksa
Name:		amsn
Version:	0.95
Release:	1
Epoch:		0
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/amsn/%{name}-%{version}.tar.gz
# Source0-md5:	f57e3c2c78a3c7d64c93a78be88846aa
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-libng_plugin_init.patch
URL:		http://amsn.sourceforge.net/
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	sed >= 4.0
BuildRequires:	tcl-devel >= 8.3
BuildRequires:	tk-devel >= 8.3
# IM's convert is needed to display pictures (buddy icons).
Requires:	ImageMagick
Requires:	tcl >= 8.3
# MSN Protocol 9 won't let you in without SSL anymore.
Requires:	tcl-tls
Requires:	tk >= 8.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is Tcl/Tk clone that implements the Microsoft Messenger (MSN) for
Unix, Windows, or Macintosh platforms. It supports file transfers,
groups, and many more features. Visit http://amsn.sourceforge.net/ for
details. This is an ongoing project, and it is already going pretty
well.

%description -l de
amsn ist ein Microsoft Messenger (MSN) Client f�r UNIX, Windows und
Macintosh, der in Tcl/Tk geschrieben ist. Es unterst�tzt
Datei�bertragungen, Gruppen uvm. Begeben Sie sich auf
http://amsn.sourceforge.net/ um mehr �ber dieses Projekt zu erfahren.

%description -l fr
amsn est un client Microsoft Messenger (MSN) pour UNIX, Windows et
Macintosh �crit en Tcl/Tk. Il supporte les tranferts de fichiers, les
groupes et beaucoup d'autres possibilit�s. Visitez
http://amsn.sourceforge.net/ pour de plus amples d�tails.

%description -l pl
amsn to klient Microsoft Messengera (MSN) dla Uniks�w, Windows i
Macintosha napisany w Tcl/Tk. Obs�uguje przesy�anie plik�w, grupy i
wiele wi�cej mo�liwo�ci - szczeg�y pod adresem
<http://amsn.sourceforge.net/>. Projekt jest nadal rozwijany i ju�
dzia�a ca�kiem dobrze.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	CFLAGS="%{rpmcflags}"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}

# FIXME: FHS?
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT%{_bindir} \
	dstdir=$RPM_BUILD_ROOT%{_libdir} \
	slnkdir=$RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_desktopdir}
install %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
rm -f $RPM_BUILD_ROOT%{_libdir}/applications/amsn.desktop

for f in amsn{,-remote{,-CLI}}; do
	rm $RPM_BUILD_ROOT%{_bindir}/$f
	ln -s ../%{_lib}/%{name}/$f $RPM_BUILD_ROOT%{_bindir}
done

# remove junk
rm -rf $RPM_BUILD_ROOT%{_libdir}/doc/amsn-0.91
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/amsn.{desktop,spec,debianmenu}
# docs in docs
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/docs
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/{AGREEMENT,CREDITS,GNUGPL,INSTALL,README,HELP,FAQ,TODO,Makefile,cvs_date}
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/utils/*/test.tcl
# random binary for PPC
rm -rf $RPM_BUILD_ROOT%{_libdir}/amsn/sndplay

mv $RPM_BUILD_ROOT%{_libdir}/icons $RPM_BUILD_ROOT%{_iconsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc FAQ GNUGPL HELP README TODO CREDITS
%attr(755,root,root) %{_bindir}/*
%{_libdir}/%{name}/a[!m]*
%{_libdir}/%{name}/[!a]*
%attr(755,root,root) %{_libdir}/%{name}/amsn*

%{_iconsdir}/hicolor/*/*.png
%{_desktopdir}/%{name}.desktop
