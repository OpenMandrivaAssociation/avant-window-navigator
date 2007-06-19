%define name avant-window-navigator
%define version 0.1.1
%define svn 201
%if %svn
%define release %mkrel %svn.1
%else
%define release %mkrel 1
%endif
%define library_name awn
%define major 0
%define libname %mklibname %library_name %major
%define develname %mklibname %library_name -d

%define schemas switcher trash

Summary: Dock-style window selector for GNOME
Name: %{name}
Version: %{version}
Release: %{release}
%if %svn
Source0: %{name}-%{svn}.tar.bz2
%else
Source0: %{name}-%{version}.tar.bz2
%endif
License: GPL
Group: Graphical desktop/GNOME
Url: http://code.google.com/p/avant-window-navigator/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gnome-common
BuildRequires: libGConf2-devel
BuildRequires: intltool
BuildRequires: libgtk+2-devel
BuildRequires: libgnome2-devel
BuildRequires: libgnome-desktop-2-devel
BuildRequires: libwnck-devel
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
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

%description -n %develname
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon.

%prep
%if %svn
%setup -q -n %{name}
%else
%setup -q
%endif

%build
./autogen.sh -V
%configure --disable-schemas-install
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%find_lang %name

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-category="Utility" \
  --remove-category="X-Fedora" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
$RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %buildroot{%_liconsdir,%_miconsdir}
mkdir -p %buildroot%{_iconsdir}/hicolor
mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,24x24,22x22,16x16,scalable}
mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,24x24,22x22,16x16,scalable}/apps
install -m 644 data/%{name}-48.png %buildroot%_liconsdir/%{name}.png
install -m 644 data/%{name}-48.png %buildroot%_iconsdir/hicolor/48x48/apps/%{name}.png 
convert -scale 32 data/%{name}-48.png %buildroot%_iconsdir/%{name}.png
convert -scale 32 data/%{name}-48.png %buildroot%_iconsdir/hicolor/32x32/apps/%{name}.png
convert -scale 24 data/%{name}-48.png %buildroot%_iconsdir/hicolor/24x24/apps/%{name}.png
convert -scale 22 data/%{name}-48.png %buildroot%_iconsdir/hicolor/22x22/apps/%{name}.png
convert -scale 16 data/%{name}-48.png %buildroot%_miconsdir/%{name}.png
convert -scale 16 data/%{name}-48.png %buildroot%_iconsdir/hicolor/16x16/apps/%{name}.png
install -m 644 %buildroot%_datadir/%{name}/%{name}.svg %buildroot%_iconsdir/hicolor/scalable/apps/%{name}.svg

perl -pi -e 's,/usr/share/%{name}/%{name}-48.png,%{name},g' %buildroot%{_datadir}/applications/%{name}.desktop
perl -pi -e 's,/usr/share/%{name}/%{name}-48.png,%{name},g' %buildroot%{_datadir}/applications/avant-preferences.desktop

%post
%update_menus
%update_icon_cache hicolor
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%update_menus
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog TODO
%_bindir/%{name}
%_bindir/avant-launchers
%_bindir/avant-preferences
%_bindir/avant-applets
%_bindir/awn-applet-activation
%_datadir/%{name}
%_datadir/applications/%{name}.desktop
%_datadir/applications/avant-preferences.desktop
%_libdir/%{library_name}
%_sysconfdir/gconf/schemas/*.schemas
%_iconsdir/hicolor/16x16/apps/%{name}.png
%_iconsdir/hicolor/22x22/apps/%{name}.png
%_iconsdir/hicolor/24x24/apps/%{name}.png
%_iconsdir/hicolor/32x32/apps/%{name}.png
%_iconsdir/hicolor/48x48/apps/%{name}.png
%_iconsdir/hicolor/scalable/apps/%{name}.svg
%_liconsdir/%{name}.png
%_iconsdir/%{name}.png
%_miconsdir/%{name}.png

%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.*

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/lib%{library_name}
%{_libdir}/lib*.so
%{_libdir}/*.*a
%{_libdir}/pkgconfig/%library_name.pc
