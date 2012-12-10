%define major 1
%define library_name awn
%define libname %mklibname %{library_name} %{major}
%define develname %mklibname %{library_name} -d

Summary:	AWN - a Dock-style window selector for GNOME
Name:		avant-window-navigator
Version:	0.4.0
Release:	8
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://launchpad.net/awn
Source0:	http://launchpad.net/awn/0.4/%{version}/+download/%{name}-%{version}.tar.gz
# add upstream patch to fix unintialized null pointer
Patch0:		avant-window-navigator-0.4.0-688_687.diff
Patch1:		avant-window-navigator-0.4.0-linkage.patch
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	python-devel
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(pycairo)
BuildRequires:	libdesktop-agnostic-devel
BuildRequires:	vala
BuildRequires:	pyxdg
BuildRequires:	GConf2
Requires:	pyxdg
Requires:	pygtk2
Requires:	python-dbus
Requires:	bzr
Conflicts:	%{_lib}awn1 < 0.4.0-8

%description
Avant Window Navigator (AWN) is a dock-style window list for GNOME. It
provides a view of your running applications in a dock at the bottom
of the screen, identified by their icon.

%package -n %{libname}
Group:		System/Libraries
Summary:	Shared libraries for avant-window-navigator
Requires:	%{name} >= %{version}-%{release}

%description -n %{libname}
Avant Window Navigator (AWN) is a dock-style window list for GNOME. It
provides a view of your running applications in a dock at the bottom
of the screen, identified by their icon. This package contains the
shared library for AWN.

%package -n %{develname}
Group:		Development/C
Summary:	Development libraries for avant-window-navigator
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{library_name}-devel = %{version}-%{release}

%description -n %{develname}
Avant Window Navigator (AWN) is a dock-style window list for GNOME. It
provides a view of your running applications in a dock at the bottom
of the screen, identified by their icon. This package contains
development libraries and headers for AWN.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
%configure2_5x --disable-static \
	--with-vala \
	--with-gnu-ld \
	--enable-shave \
	--with-gconf-schema-file-dir=%{_sysconfdir}/gconf/schemas/ 
%make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std

%find_lang %{name} --with-html

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# don't ship .a and .la
find %{buildroot} -name "*.*a" -exec rm -f {} \;

%files -f %{name}.lang
%doc README AUTHORS ChangeLog TODO
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/avant-window-navigator
%{_bindir}/awn-applet
%{_bindir}/awn-settings
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/awn-settings.desktop
%{_iconsdir}/hicolor/*/*/*
%{python_sitearch}/awn/*
%{_libdir}/awn/applets/expander/expander.so
%{_libdir}/awn/applets/quick-prefs/quick-prefs.so
%{_libdir}/awn/applets/separator/separator.so
%{_libdir}/awn/applets/taskmanager/taskmanager.so

%files -n %{libname}
%{_libdir}/libawn.so.%{major}*

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/lib%{library_name}
%{_includedir}/lib%{library_name}
%{_libdir}/libawn.so
%{_libdir}/pkgconfig/%{library_name}.pc
%{_datadir}/vala/vapi/awn.*
%{_datadir}/pygtk/2.0/defs/awn.defs

