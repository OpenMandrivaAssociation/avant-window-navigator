%define name avant-window-navigator
%define version 0.2.1
%define rel 1
%define bzr 0

%define major 0
%define library_name awn
%define libname %mklibname %library_name %major
%define develname %mklibname %library_name -d

%if %bzr
%define srcname %{name}-%{bzr}
%define distname %{name}
%define release %mkrel 0.%{bzr}.%{rel}
%else
%define srcname %{name}-%{version}
%define distname %{name}-%{version}
%define release %mkrel %{rel}
%endif

#%define schemas switcher trash

Summary: Dock-style window selector for GNOME
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{srcname}.tar
License: GPLv2+
Group: Graphical desktop/GNOME
Url: https://launchpad.net/awn
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gnome-common
BuildRequires: libGConf2-devel
BuildRequires: intltool
BuildRequires: libgtk+2-devel
BuildRequires: libgnome2-devel
BuildRequires: libgnome-desktop-2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libwnck-devel
BuildRequires: libxcomposite-devel
BuildRequires: libxdamage-devel
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
BuildRequires: python-devel
BuildRequires: pygtk2.0-devel
BuildRequires: gnome-python
Requires: gnome-python

%description
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon.

%package -n %libname
Group: System/Libraries
Summary: Shared libraries for avant-window-navigator

%description -n %libname
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon.

%package -n %develname
Group: Development/C
Summary: Development libraries for avant-window-navigator
Requires: %libname = %version
Provides: %name-devel = %version-%release
Provides: %library_name-devel = %version-%release

%description -n %develname
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon.

%prep
%setup -q -n %{distname}

%build
%if %bzr
./autogen.sh -V
%endif
%configure --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %name

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-category="X-Fedora" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
$RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,16x16,scalable}/apps
install -m 644 %buildroot%_datadir/%{name}/%{name}.svg %buildroot%_iconsdir/hicolor/scalable/apps/%{name}.svg
install -m 644 data/%{name}-48.png %buildroot%_iconsdir/hicolor/48x48/apps/%{name}.png 
convert -scale 32 data/%{name}-48.png %buildroot%_iconsdir/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/%{name}-48.png %buildroot%_iconsdir/hicolor/16x16/apps/%{name}.png

perl -pi -e 's,/usr/share/%{name}/%{name}-48.png,%{name},g' %buildroot%{_datadir}/applications/%{name}.desktop
perl -pi -e 's,/usr/share/%{name}/%{name}-48.png,%{name},g' %buildroot%{_datadir}/applications/awn-manager.desktop

%post
%update_menus
%update_icon_cache hicolor
#post_install_gconf_schemas %{schemas}

#preun
#preun_uninstall_gconf_schemas %{schemas}

%postun
%update_menus
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog TODO
%_bindir/%{name}
%_bindir/awn-applet-activation
%_bindir/awn-manager
%_datadir/%{name}
%_datadir/applications/%{name}.desktop
%_datadir/applications/awn-manager.desktop
%_libdir/%{library_name}
#%_sysconfdir/gconf/schemas/*.schemas
%_iconsdir/hicolor/16x16/apps/%{name}.png
%_iconsdir/hicolor/32x32/apps/%{name}.png
%_iconsdir/hicolor/48x48/apps/%{name}.png
%_iconsdir/hicolor/scalable/apps/%{name}.svg
%py_platsitedir/%library_name

%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.%{major}*

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/lib%{library_name}
%{_libdir}/lib*.so
%{_libdir}/*.*a
%{_libdir}/pkgconfig/%library_name.pc
