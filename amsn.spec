#
# Conditional build:
%bcond_without	imlib	# do not compile freedesktop notification plugin
#
Summary:	MSN Messenger clone for Linux
Summary(fr):	Clône MSN Messenger pour Linux
Summary(de):	MSN Messenger-Klon für Linux
Name:		amsn
Version:	0.94
Release:	0.5
Epoch:		0
License:	GPL
Group:		Applications/Communications
%define	_ver	%(echo %{version} | tr . _)
Source0:	http://dl.sourceforge.net/amsn/%{name}-%{_ver}.tar.gz
# Source0-md5:	7b7db9225342bb6c59b873ec90882e22
URL:		http://amsn.sourceforge.net/
%{?with_imlib:BuildRequires:	imlib-devel}
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	tcl-devel >= 8.3
BuildRequires:	tk-devel >= 8.3
BuildRequires:	sed >= 4.0
Requires:	tk >= 8.3
Requires:	tcl >= 8.3
# MSN Protocol 9 won't let you in without SSL anymore.
Requires:	tcl-tls
# IM's convert is needed to display pictures (buddy icons).
Requires:	ImageMagick
%{!?with_imlib:BuildArch:	noarch}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is Tcl/Tk clone that implements the Microsoft Messenger (MSN) for
Unix,Windows, or Macintosh platforms. It supports file transfers,
groups, and many more features. Visit http://amsn.sourceforge.net/ for
details. This is an ongoing project, and it is already going pretty
well.

%description -l fr
amsn est un client Microsoft Messenger (MSN) pour UNIX, Windows et
Macintosh écrit en Tcl/Tk.  Il supporte les tranferts de fichiers, les
groupes et beaucoup d'autres possibilités. 
Visitez http://amsn.sourceforge.net/ pour de plus amples détails.

%description -l de
amsn ist ein Microsoft Messenger (MSN) Client für UNIX, Windows und
Macintosh, der in Tcl/Tk geschrieben ist. Es unterstützt
Dateiübertragungen, Gruppen uvm.
Begeben Sie sich auf http://amsn.sourceforge.net/ um mehr über dieses
Projekt zu erfahren.

%prep
%setup -q -n %{name}-%{_ver}

%build
# add InstantMessaging category
sed -i -e '/Categories=/s/.*/Categories=Network;InstantMessaging;/' %{name}.desktop

%if %{with imlib}
cd plugins/traydock
%configure
%{__make} %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT

# create directories if necessary
install -d $RPM_BUILD_ROOT/usr/share/%{name}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix}

%if %{with imlib}
	# Installing the freedesktop notification plugin"
	install -d $RPM_BUILD_ROOT/usr/lib/amsn/plugins/traydock
	mv $RPM_BUILD_ROOT/usr/share/amsn/plugins/traydock/libtray.so $RPM_BUILD_ROOT/usr/lib/amsn/plugins/traydock/
	rm -rf $RPM_BUILD_ROOT/usr/share/amsn/plugins/traydock/
	ln -s ../../../lib/amsn/plugins/traydock/ $RPM_BUILD_ROOT/usr/share/amsn/plugins/
%else
	rm -rf $RPM_BUILD_ROOT/usr/share/amsn/plugins/traydock
%endif

# force relative path
# FIXME: FHS?
ln -sf ../share/amsn/amsn $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_desktopdir}
install %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# remove junk
rm -rf $RPM_BUILD_ROOT/usr/share/doc/amsn-0.91
rm -rf $RPM_BUILD_ROOT/usr/share/amsn/amsn.{desktop,spec,debianmenu}
# docs in docs
rm -rf $RPM_BUILD_ROOT/usr/share/amsn/docs
rm -rf $RPM_BUILD_ROOT/usr/share/amsn/{CREDITS,GNUGPL,README,HELP,FAQ,TODO,Makefile,cvs_date}
# random binary for PPC
rm -rf $RPM_BUILD_ROOT/usr/share/amsn/sndplay
# not for our arch
rm -rf $RPM_BUILD_ROOT/usr/share/amsn/plugins/{winflash,winutils,QuickTimeTcl3.1,applescript,tclCarbonNotification,tclAE2.0}
rm -rf $RPM_BUILD_ROOT/usr/share/amsn/plugins/winico*
rm -rf $RPM_BUILD_ROOT/usr/share/amsn/utils/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc FAQ GNUGPL HELP README TODO CREDITS
%attr(755,root,root) %{_bindir}/*

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/lang
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/skins
%{_datadir}/%{name}/*.tcl
%{_datadir}/%{name}/hotmlog.htm
%{_datadir}/%{name}/langlist
%{_datadir}/%{name}/remote.help

%attr(755,root,root) %{_datadir}/%{name}/%{name}*

%{_datadir}/pixmaps/*.png
%{_desktopdir}/%{name}.desktop
%{?with_imlib:/usr/lib/amsn}
