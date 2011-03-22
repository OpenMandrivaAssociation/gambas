Name: gambas3
Summary: Complete IDE based on a BASIC interpreter with object extensions
Version: 2.99.0
Release: 1
License: GPLv2+
Group: Development/Other
URL: http://gambas.sourceforge.net/
Source0: http://ovh.dl.sourceforge.net/sourceforge/gambas/%{name}-%version.tar.bz2
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: bzip2-devel
BuildRequires: firebird-devel
BuildRequires: libunixODBC-devel
BuildRequires: libsqlite-devel
BuildRequires: libsqlite3-devel
BuildRequires: gtk+2-devel
BuildRequires: libmesagl-devel
BuildRequires: libmesaglu-devel
BuildRequires: libpcre-devel
BuildRequires: libSDL_gfx-devel
BuildRequires: libSDL_ttf-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: gettext-devel
BuildRequires: qt4-devel
BuildRequires: libcurl-devel
BuildRequires: libgettextmisc
BuildRequires: libSDL-devel
BuildRequires: libpoppler-devel
BuildRequires: mysql-devel
BuildRequires: postgresql-devel
BuildRequires: SDL_mixer-devel
BuildRequires: imagemagick
BuildRequires: libffi-devel
BuildRequires: libxtst-devel
BuildRequires: libv4l-devel
BuildRequires: glew-devel
BuildRequires: xdg-utils
BuildRequires: librsvg-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: imlib2-devel
BuildRequires: dbus-devel

%description
Gambas is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic(tm) (but it is NOT a clone!). 
With Gambas, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, control KDE applications with DCOP, translate
your program into many languages, create network applications easily,
build RPMs of your apps automatically, and so on...

%prep
%setup -q -n %{name}-%version

%build
%setup_compile_flags
./reconf-all
for i in `find -name configure`
do
	(
	  pushd `dirname $i`
	  %before_configure
	  popd
	)
done

%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -f %buildroot%_libdir/gambas3/gb.so* %buildroot%_libdir/gambas3/gb.la

#-----------------------------------------------------------------------------

%package runtime
Summary: The Gambas runtime
Group: Development/Other

%description runtime
This package includes the Gambas interpreter needed to run Gambas applications.

%if %mdkversion < 200900
%post runtime
%update_mime_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun runtime
%update_mime_database
%update_icon_cache hicolor
%endif

%files runtime
%defattr(-, root, root, 0755)
%doc README AUTHORS ChangeLog
%{_bindir}/gbx3
%{_bindir}/gbr3
%{_libdir}/%{name}/gb.component
%{_libdir}/%{name}/gb.debug.*
%{_libdir}/%{name}/gb.eval.*
%{_libdir}/%{name}/gb.draw.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.info
%{_datadir}/%{name}/info/gb.list
%{_datadir}/%{name}/info/gb.debug.*
%{_datadir}/%{name}/info/gb.eval.*
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/application-x-gambas.png

#-----------------------------------------------------------------------------

%package devel
Summary: The Gambas development package
Group: Development/Other

%description devel
This package includes all tools needed to compile Gambas projects
without having to install the complete development environment.

%files devel
%defattr(-, root, root, 0755)
%{_bindir}/gbc3
%{_bindir}/gba3
%{_bindir}/gbi3

#-----------------------------------------------------------------------------

%package script
Summary: The Gambas scripter package
Group: Development/Other
Requires: %{name}-runtime = %{version}
Requires: %{name}-devel = %{version}

%description script
This package includes the scripter program that allows to write script files
in Gambas.

%if %mdkversion < 200900
%post script
%update_mime_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun script
%clean_mime_database
%clean_icon_cache hicolor
%endif

%files script
%defattr(-, root, root, 0755)
%{_bindir}/gbs3
%{_bindir}/gbs3.gambas
%{_bindir}/gbw3
%{_datadir}/%{name}/icons/application-x-gambasserverpage.png
%{_datadir}/%{name}/icons/application-x-gambasscript.png

#-----------------------------------------------------------------------------

%package ide
Summary: The Gambas IDE
Group: Development/Other
Requires: %{name}-runtime = %{version}
Requires: %{name}-devel = %{version}
Requires: %{name}-gb-cairo = %{version}
Requires: %{name}-gb-chart = %{version}
Requires: %{name}-gb-compress = %{version}
Requires: %{name}-gb-crypt = %{version}
Requires: %{name}-gb-db = %{version}
Requires: %{name}-gb-db-form = %{version}
Requires: %{name}-gb-db-mysql = %{version}
Requires: %{name}-gb-db-odbc = %{version}
Requires: %{name}-gb-db-postgresql = %{version}
Requires: %{name}-gb-db-sqlite2 = %{version}
Requires: %{name}-gb-db-sqlite3 = %{version}
Requires: %{name}-gb-dbus = %{version}
Requires: %{name}-gb-dekstop-gnome = %{version}
Requires: %{name}-gb-desktop = %{version}
Requires: %{name}-gb-form = %{version}
Requires: %{name}-gb-gtk = %{version}
Requires: %{name}-gb-gui = %{version}
Requires: %{name}-gb-image = %{version}
Requires: %{name}-gb-mysql = %{version}
Requires: %{name}-gb-net = %{version}
Requires: %{name}-gb-net-curl = %{version}
Requires: %{name}-gb-net-smtp = %{version}
Requires: %{name}-gb-opengl = %{version}
Requires: %{name}-gb-option = %{version}
Requires: %{name}-gb-pcre = %{version}
Requires: %{name}-gb-pdf = %{version}
Requires: %{name}-gb-qt4 = %{version}
Requires: %{name}-gb-report = %{version}
Requires: %{name}-gb-sdl = %{version}
Requires: %{name}-gb-sdl-sound = %{version}
Requires: %{name}-gb-settings = %{version}
Requires: %{name}-gb-signal = %{version}
Requires: %{name}-gb-v4l = %{version}
Requires: %{name}-gb-vb = %{version}
Requires: %{name}-gb-web = %{version}
Requires: %{name}-gb-xml = %{version}
Requires: %{name}-gb-xml-rpc = %{version}
Requires: %{name}-gb-xml-xslt = %{version}

%description ide
This package includes the complete Gambas Development Environment, with the
database manager, the help files, and all components.

%if %mdkversion < 200900
%post ide
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun ide
%clean_menus
%clean_icon_cache hicolor
%endif

%files ide
%defattr(-, root, root, 0755)
%{_bindir}/%{name}
%{_bindir}/%{name}.gambas

#-----------------------------------------------------------------------------

%package examples
Summary: The Gambas examples
Group: Development/Other
Requires: %{name}-ide = %{version}
Conflicts: %{name}-ide < 2.6.0-2

%description examples
This package includes all the example projects provided with Gambas.

%files examples
%defattr(-,root,root)
%{_datadir}/%{name}/examples

#-----------------------------------------------------------------------------

%package gb-cairo
Summary: The Gambas Cairo component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-cairo
This package contains the Gambas Cario components.

%files gb-cairo
%defattr(-,root,root)
%{_libdir}/%{name}/gb.cairo.*
%{_datadir}/%{name}/info/gb.cairo.*

#-----------------------------------------------------------------------------

%package gb-chart
Summary: The Gambas chart component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-chart
This package contains the Gambas Chart components.

%files gb-chart
%defattr(-,root,root)
%{_libdir}/%{name}/gb.chart.*
%{_datadir}/%{name}/info/gb.chart.*

#-----------------------------------------------------------------------------

%package gb-compress
Summary: The Gambas compression component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-compress
This component allows you to compress/uncompress data or files with
the bzip2 and zip algorithms.

%files gb-compress
%defattr(-,root,root)
%{_libdir}/%{name}/gb.compress.*
%{_datadir}/%{name}/info/gb.compress.*

#-----------------------------------------------------------------------------

%package gb-crypt
Summary: The Gambas cryptography component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-crypt
This component allows you to use cryptography in your projects.

%files gb-crypt
%defattr(-,root,root)
%{_libdir}/%{name}/gb.crypt.*
%{_datadir}/%{name}/info/gb.crypt.*

#-----------------------------------------------------------------------------

%package gb-db
Summary: The Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-db
This component allows you to access many databases management systems,
provided that you install the needed driver packages.

%files gb-db
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.la
%{_libdir}/%{name}/gb.db.so*
%{_libdir}/%{name}/gb.db.component
%{_libdir}/%{name}/gb.db.gambas
%{_datadir}/%{name}/info/gb.db.info
%{_datadir}/%{name}/info/gb.db.list

#-----------------------------------------------------------------------------

%package gb-db-form
Summary: The Gambas db-form component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-db-form
This package contains the Gambas Database form components.

%files gb-db-form
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.form.*
%{_datadir}/%{name}/info/gb.db.form.*
%{_datadir}/%{name}/control/gb.db.form

#-----------------------------------------------------------------------------

%package gb-db-mysql
Summary: The MySQL driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-mysql
This component allows you to access MySQL databases.

%files gb-db-mysql
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.mysql.*
%{_datadir}/%{name}/info/gb.db.mysql.*

#-----------------------------------------------------------------------------

%package gb-db-odbc
Summary: The ODBC driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-odbc
This component allows you to access ODBC databases.

%files gb-db-odbc
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.odbc.*
%{_datadir}/%{name}/info/gb.db.odbc.*

#-----------------------------------------------------------------------------

%package gb-db-postgresql
Summary: The PostgreSQL driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-postgresql
This component allows you to access PostgreSQL databases.

%files gb-db-postgresql
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.postgresql.*
%{_datadir}/%{name}/info/gb.db.postgresql.*

#-----------------------------------------------------------------------------

%package gb-db-sqlite2
Summary: The SQLite 2 driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-sqlite2
This component allows you to access SQLite 2 databases.

%files gb-db-sqlite2
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.sqlite2.*
%{_datadir}/%{name}/info/gb.db.sqlite2.*

#-----------------------------------------------------------------------------

%package gb-db-sqlite3
Summary: The SQLite 3 driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-sqlite3
This component allows you to access SQLite 3 databases.

%files gb-db-sqlite3
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.sqlite3.*
%{_datadir}/%{name}/info/gb.db.sqlite3.*

#-----------------------------------------------------------------------------

%package gb-dbus
Summary: The Gambas dbus component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-dbus
This package contains the Gambas D-bus components.

%files gb-dbus
%defattr(-,root,root)
%{_libdir}/%{name}/gb.dbus.*
%{_datadir}/%{name}/info/gb.dbus.*

#-----------------------------------------------------------------------------

%package gb-desktop
Summary: The Gambas XDG component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-desktop
This component allows you to use desktop-agnostic routines based on 
the xdg-utils scripts of the Portland project.

%files gb-desktop
%defattr(-,root,root)
%{_libdir}/%{name}/gb.desktop.la
%{_libdir}/%{name}/gb.desktop.so*
%{_libdir}/%{name}/gb.desktop.component
%{_libdir}/%{name}/gb.desktop.gambas
%{_datadir}/%{name}/info/gb.desktop.info
%{_datadir}/%{name}/info/gb.desktop.list
%{_datadir}/%{name}/control/gb.desktop

#-----------------------------------------------------------------------------

%package gb-dekstop-gnome
Summary: The Gambas GNOME desktop component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-dekstop-gnome
This package contains the Gambas GNOME desktop components.

%files gb-dekstop-gnome
%defattr(-,root,root)
%{_libdir}/%{name}/gb.desktop.gnome.*

#-----------------------------------------------------------------------------

%package gb-form
Summary: The Gambas dialog form component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}

%description gb-form
This component implements the form control.

%files gb-form
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.*
%{_datadir}/%{name}/info/gb.form.*
%{_datadir}/%{name}/control/gb.form*

#-----------------------------------------------------------------------------

%package gb-gtk
Summary: The Gambas GTK+ GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-gtk
This package contains the Gambas GTK+ GUI components.

%files gb-gtk
%defattr(-,root,root)
%{_libdir}/%{name}/gb.gtk.*
%{_datadir}/%{name}/info/gb.gtk.*

#-----------------------------------------------------------------------------

%package gb-gui
Summary: The Gambas GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-gui
This is a component that just loads gb.qt if you are running KDE or
gb.gtk in the other cases.

%files gb-gui
%defattr(-,root,root)
%{_libdir}/%{name}/gb.gui.*
%{_datadir}/%{name}/info/gb.gui.*

#-----------------------------------------------------------------------------

%package gb-image
Summary: The Gambas image manipulation component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-image
This component allows you to apply various effects to images.

%files gb-image
%defattr(-,root,root)
%{_libdir}/%{name}/gb.image.*
%{_datadir}/%{name}/info/gb.image.*

#-----------------------------------------------------------------------------

%package gb-mysql
Summary: The Gambas mysql component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-mysql
This package contains the Gambas MySQL components.

%files gb-mysql
%defattr(-,root,root)
%{_libdir}/%{name}/gb.mysql.*
%{_datadir}/%{name}/info/gb.mysql.*

#-----------------------------------------------------------------------------

%package gb-net
Summary: The Gambas networking component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-net
This component allows you to use TCP/IP and UDP sockets, and to access
any serial ports.

%files gb-net
%defattr(-,root,root)
%{_libdir}/%{name}/gb.net.la
%{_libdir}/%{name}/gb.net.so*
%{_libdir}/%{name}/gb.net.component
%{_datadir}/%{name}/info/gb.net.info
%{_datadir}/%{name}/info/gb.net.list

#-----------------------------------------------------------------------------

%package gb-net-curl
Summary: The Gambas advanced networking component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-net = %{version}

%description gb-net-curl
This component allows your programs to easily become FTP or HTTP clients.

%files gb-net-curl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.net.curl.la
%{_libdir}/%{name}/gb.net.curl.so*
%{_libdir}/%{name}/gb.net.curl.component
%{_datadir}/%{name}/info/gb.net.curl.info
%{_datadir}/%{name}/info/gb.net.curl.list

#-----------------------------------------------------------------------------

%package gb-net-smtp
Summary: The Gambas SMTP component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-net = %{version}

%description gb-net-smtp
This component allows you to send emails using the SMTP protocol.

%files gb-net-smtp
%defattr(-,root,root)
%{_libdir}/%{name}/gb.net.smtp.*
%{_datadir}/%{name}/info/gb.net.smtp.*

#-----------------------------------------------------------------------------

%package gb-opengl
Summary: The Gambas OpenGL component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-opengl
This component allows you to use the Mesa libraries to do 3D operations.

%files gb-opengl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.opengl.*
%{_datadir}/%{name}/info/gb.opengl.*

#-----------------------------------------------------------------------------

%package gb-option
Summary: The Gambas command-line option component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-option
This component allows you to interpret command-line options.

%files gb-option
%defattr(-,root,root)
%{_libdir}/%{name}/gb.option.*
%{_datadir}/%{name}/info/gb.option.*

#-----------------------------------------------------------------------------

%package gb-pcre
Summary: The Gambas PCRE component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-pcre
This component allows you to use Perl compatible regular expresions
within Gambas code.

%files gb-pcre
%defattr(-,root,root)
%{_libdir}/%{name}/gb.pcre.*
%{_datadir}/%{name}/info/gb.pcre.*

#-----------------------------------------------------------------------------

%package gb-pdf
Summary: The Gambas PDF component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-pdf
This component allows you to manipulate pdf files with Gambas code.

%files gb-pdf
%defattr(-,root,root)
%{_libdir}/%{name}/gb.pdf.*
%{_datadir}/%{name}/info/gb.pdf.*

#-----------------------------------------------------------------------------

%package gb-qt4
Summary: The Gambas Qt GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-qt4
This package includes the Gambas QT GUI component.

%files gb-qt4
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt4.*
%{_datadir}/%{name}/info/gb.qt4.*

#-----------------------------------------------------------------------------

%package gb-report
Summary: The Gambas report component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-report
This package contains the Gambas Report components.

%files gb-report
%defattr(-,root,root)
%{_libdir}/%{name}/gb.report.*
%{_datadir}/%{name}/info/gb.report.*
%{_datadir}/%{name}/control/gb.report

#-----------------------------------------------------------------------------

%package gb-sdl
Summary: The Gambas SDL component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-sdl
This component use the sound, image and TTF fonts parts of the SDL
library. It allows you to simultaneously play many sounds and music
stored in a file. If OpenGL drivers are installed it uses them to 
accelerate 2D and 3D drawing.

%files gb-sdl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.sdl.la
%{_libdir}/%{name}/gb.sdl.so
%{_libdir}/%{name}/gb.sdl.so.*
%{_libdir}/%{name}/gb.sdl.component
%{_datadir}/%{name}/info/gb.sdl.info
%{_datadir}/%{name}/info/gb.sdl.list
%{_datadir}/%{name}/gb.sdl

#-----------------------------------------------------------------------------

%package gb-sdl-sound
Summary: The Gambas SDL sound component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-sdl-sound
This component allows you to play sounds in Gambas. This component 
manages up to 32 sound tracks that can play sounds from memory, and
one music track that can play music from a file. Everything is mixed
in real time. 

%files gb-sdl-sound
%defattr(-,root,root)
%{_libdir}/%{name}/gb.sdl.sound.*
%{_datadir}/%{name}/info/gb.sdl.sound.*

#-----------------------------------------------------------------------------

%package gb-settings
Summary: The Gambas settings component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-settings
This components allows you to deal with configuration files.

%files gb-settings
%defattr(-,root,root)
%{_libdir}/%{name}/gb.settings.*
%{_datadir}/%{name}/info/gb.settings.*

#-----------------------------------------------------------------------------

%package gb-signal
Summary: The Gambas signal component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-signal
This package contains the Gambas Signal components.

%files gb-signal
%defattr(-,root,root)
%{_libdir}/%{name}/gb.signal.*
%{_datadir}/%{name}/info/gb.signal.*

#-----------------------------------------------------------------------------

%package gb-v4l
Summary: The Gambas Video4Linux component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-v4l
This components allows you to use the Video4Linux interface with
Gambas.

%files gb-v4l
%defattr(-,root,root)
%{_libdir}/%{name}/gb.v4l.*
%{_datadir}/%{name}/info/gb.v4l.*

#-----------------------------------------------------------------------------

%package gb-vb
Summary: The Gambas Visual Basic(tm) compatibility component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-vb
This component aims at including some functions that imitate the 
behaviour of Visual Basic(TM) functions. Use it only if you want to 
port some VB projects.

%files gb-vb
%defattr(-,root,root)
%{_libdir}/%{name}/gb.vb.*
%{_datadir}/%{name}/info/gb.vb.*

#-----------------------------------------------------------------------------

%package gb-web
Summary: The Gambas CGI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-web
This components allows you to make CGI web applications using Gambas, 
with an ASP-like interface.

%files gb-web
%defattr(-,root,root)
%{_libdir}/%{name}/gb.web.*
%{_datadir}/%{name}/info/gb.web.*

#-----------------------------------------------------------------------------

%package gb-xml
Summary: The Gambas xml component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-xml
This component allows you to use xml.

%files gb-xml
%defattr(-,root,root)
%{_libdir}/%{name}/gb.xml.la
%{_libdir}/%{name}/gb.xml.so*
%{_libdir}/%{name}/gb.xml.component
%{_datadir}/%{name}/info/gb.xml.info
%{_datadir}/%{name}/info/gb.xml.list

#-----------------------------------------------------------------------------

%package gb-xml-rpc
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-xml-rpc
This component allows you to use xml-rpc.

%files gb-xml-rpc
%defattr(-,root,root)
%{_libdir}/%{name}/gb.xml.rpc*
%{_datadir}/%{name}/info/gb.xml.rpc*

#-----------------------------------------------------------------------------

%package gb-xml-xslt
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-xml-xslt
This component allows you to use xml-xslt.

%files gb-xml-xslt
%defattr(-,root,root)
%{_libdir}/%{name}/gb.xml.xslt*
%{_datadir}/%{name}/info/gb.xml.xslt*

#-----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT


