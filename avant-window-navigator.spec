%define name avant-window-navigator
%define version 0.1.1
%define svn 173
%if %svn
%define release %mkrel %svn.1
%else
%define release %mkrel 1
%endif


Summary: Dock-style window selector for GNOME
Name: %{name}
Version: %{version}
Release: %{release}
%if %svn
Source0: %{name}-%{version}-%{svn}.tar.bz2
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
BuildRequires: sed
BuildRequires: desktop-file-utils
Requires: gnome-python

%description
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon.

%prep
%setup -q

%build
./autogen.sh -V
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%find_lang %name

desktop-file-install --vendor="" \
  --add-category="X-MandrivaLinux-System-Session-Windowmanagers" \
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

sed -e 's/\/usr\/share\/%{name}\/%{name}-48.png/%{name}/' %buildroot%{_datadir}/applications/%{name}.desktop > %buildroot%{_datadir}/applications/%{name}.new && \
mv -f %buildroot%{_datadir}/applications/%{name}.new %buildroot%{_datadir}/applications/%{name}.desktop
sed -e 's/\/usr\/share\/%{name}\/%{name}-48.png/%{name}/' %buildroot%{_datadir}/applications/avant-preferences.desktop > %buildroot%{_datadir}/applications/avant-preferences.new && \
mv -f %buildroot%{_datadir}/applications/avant-preferences.new %buildroot%{_datadir}/applications/avant-preferences.desktop

%post
%update_menus
%update_icon_cache hicolor
%postun
%update_menus
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog TODO
%_bindir/%{name}
%_bindir/avant-preferences
%dir %_datadir/%{name}
%_datadir/%{name}/active/*.png
%_datadir/applications/%{name}.desktop
%_datadir/applications/avant-preferences.desktop
%_datadir/%{name}/*.png
%_datadir/%{name}/%{name}.svg
%_iconsdir/hicolor/16x16/apps/%{name}.png
%_iconsdir/hicolor/22x22/apps/%{name}.png
%_iconsdir/hicolor/24x24/apps/%{name}.png
%_iconsdir/hicolor/32x32/apps/%{name}.png
%_iconsdir/hicolor/48x48/apps/%{name}.png
%_iconsdir/hicolor/scalable/apps/%{name}.svg
%_liconsdir/%{name}.png
%_iconsdir/%{name}.png
%_miconsdir/%{name}.png
%_datadir/%{name}/window.glade


