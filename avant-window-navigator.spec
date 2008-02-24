%define rel 2
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

%define schemas awn

Summary:	Dock-style window selector for GNOME
Name:		avant-window-navigator
Version:	0.2.6
Release:	%{release}
Source0:	%{srcname}.tar.gz
# From upstream dev malept: install Python stuff to platsitedir not
# puresitedir - AdamW 2008/02
Patch0:		avant-window-navigator-0.2.6-platsitedir.patch
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://launchpad.net/awn
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gnome-common
BuildRequires:	libGConf2-devel
BuildRequires:	intltool
BuildRequires:	libgtk+2-devel
BuildRequires:	libgnome2-devel
BuildRequires:	libgnome-desktop-2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	libwnck-devel
BuildRequires:	libxcomposite-devel
BuildRequires:	libxdamage-devel
BuildRequires:	ImageMagick
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	gnome-python
BuildRequires:	gtk-doc
BuildRequires:	pyxdg
BuildRequires:	vala
Requires:	gnome-python
Requires:	gnome-python-gconf
Requires:	gnome-desktop
Requires:	gnome-python-gnomevfs
Requires:	gnome-python-applet
Requires:	pygtk2.0-libglade
Requires:	pyxdg

%description
Avant Window Navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon.

%package -n %{libname}
Group: System/Libraries
Summary: Shared libraries for avant-window-navigator

%description -n %{libname}
Avant Window Navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon. This package contains the shared library for
AWN.

%package -n %{develname}
Group: Development/C
Summary: Development libraries for avant-window-navigator
Requires: %{libname} = %{version}
Provides: %{name}-devel = %{version}-%{release}
Provides: %{library_name}-devel = %{version}-%{release}

%description -n %{develname}
Avant-window-navigator is a dock-style window list for GNOME. It provides
a view of your running applications in a dock at the bottom of the screen,
identified by their icon. This package contains development libraries and
headers for AWN.

%prep
%setup -q -n %{distname}
%patch0 -p1 -b .platsitedir

%build
%if %bzr
./autogen.sh -V
%endif
# Needed for the platsitedir patch - AdamW 2008/02
autoreconf
%configure2_5x --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-category="X-Fedora" \
  --dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/*

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16,scalable}/apps
install -m 644 %{buildroot}%{_datadir}/%{name}/%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -m 644 data/%{name}-48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png 
convert -scale 32 data/%{name}-48.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/%{name}-48.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

sed -i -e 's,/usr/share/%{name}/%{name}-48.png,%{name},g' %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i -e 's,/usr/share/%{name}/%{name}-48.png,%{name},g' %{buildroot}%{_datadir}/applications/awn-manager.desktop

%post
%update_menus
%update_icon_cache hicolor
%post_install_gconf_schemas %{schemas}

#preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%update_menus
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog TODO
%{_bindir}/%{name}
%{_bindir}/awn-applet-activation
%{_bindir}/awn-launcher-editor
%{_bindir}/awn-manager
%{_bindir}/awn-schema-to-gconf
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/awn-manager.desktop
%{_libdir}/%{library_name}
%{_sysconfdir}/gconf/schemas/*.schemas
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_iconsdir}/hicolor/*/apps/awn-manager.*
%{py_platsitedir}/%{library_name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/lib%{library_name}
%{_includedir}/lib%{library_name}
%{_libdir}/lib*.so
%{_libdir}/*.*a
%{_libdir}/pkgconfig/%{library_name}.pc
%{_datadir}/vala/vapi/awn.*

