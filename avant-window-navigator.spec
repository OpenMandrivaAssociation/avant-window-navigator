%define rel 1
%define bzr 0

%define major 1
%define library_name awn
%define libname %mklibname %library_name %major
%define develname %mklibname %library_name -d

%define oldlibname %mklibname %library_name 0

%if %bzr
%define srcname %{name}-%{bzr}
%define distname %{name}
%define release %mkrel 0.%{bzr}.%{rel}
%else
%define srcname %{name}-%{version}
%define distname %{name}-%{version}
%define release %mkrel 3
%endif

Summary:	AWN - a Dock-style window selector for GNOME
Name:		avant-window-navigator
Version:	0.4.0
Release:	%{release}
Source0:	http://launchpad.net/awn/0.4/%{version}/+download/%{srcname}.tar.gz
# add upstream patch to fix unintialized null pointer
Patch0:		avant-window-navigator-0.4.0-688_687.diff
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://launchpad.net/awn
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	intltool
BuildRequires:	libgtk+2-devel
BuildRequires:	libwnck-devel
BuildRequires:	libgtop2.0-devel
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	libdesktop-agnostic-devel
BuildRequires:	vala
BuildRequires:	dbus-glib-devel
BuildRequires:	pyxdg
Requires:	pyxdg
Requires:	pygtk2
Obsoletes:	%oldlibname

%description
Avant Window Navigator (AWN) is a dock-style window list for GNOME. It
provides a view of your running applications in a dock at the bottom
of the screen, identified by their icon.

%package -n %{libname}
Group: System/Libraries
Summary: Shared libraries for avant-window-navigator
Requires: %{name} >= %{version}-%{release}

%description -n %{libname}
Avant Window Navigator (AWN) is a dock-style window list for GNOME. It
provides a view of your running applications in a dock at the bottom
of the screen, identified by their icon. This package contains the
shared library for AWN.

%package -n %{develname}
Group: Development/C
Summary: Development libraries for avant-window-navigator
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Provides: %{library_name}-devel = %{version}-%{release}

%description -n %{develname}
Avant Window Navigator (AWN) is a dock-style window list for GNOME. It
provides a view of your running applications in a dock at the bottom
of the screen, identified by their icon. This package contains
development libraries and headers for AWN.

%prep
%setup -q -n %{distname}
%patch0 -p0

%build
%if %bzr
./autogen.sh -V
%endif
%configure2_5x --disable-static \
	--with-vala \
	--with-gnu-ld \
	--enable-shave \
	--with-gconf-schema-file-dir=%{_sysconfdir}/gconf/schemas/ 
%make

%install
rm -rf %{buildroot}

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std

%find_lang %{name} --with-html

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# don't ship .a and .la
find %{buildroot} -name "*.*a" -exec rm -f {} \;

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog TODO
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/%{name}
%{_bindir}/avant-window-navigator
%{_bindir}/awn-applet
%{_bindir}/awn-settings
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/awn-settings.desktop
%{_iconsdir}/hicolor/*/*/*
%{python_sitearch}/awn/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libawn.so.%{major}*
%{_libdir}/awn/applets/expander/expander.so
%{_libdir}/awn/applets/quick-prefs/quick-prefs.so
%{_libdir}/awn/applets/separator/separator.so
%{_libdir}/awn/applets/taskmanager/taskmanager.so

%files -n %{develname}
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/lib%{library_name}
%{_includedir}/lib%{library_name}
%{_libdir}/libawn.so
%{_libdir}/pkgconfig/%{library_name}.pc
%{_datadir}/vala/vapi/awn.*
%{_datadir}/pygtk/2.0/defs/awn.defs
