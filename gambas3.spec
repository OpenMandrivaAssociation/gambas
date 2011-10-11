Name: gambas3
Summary: Complete IDE based on a BASIC interpreter with object extensions
Version: 2.99.5
Release: %mkrel 1
License: GPLv2+
Group: Development/Other
URL: http://gambas.sourceforge.net/
Source0: http://ovh.dl.sourceforge.net/sourceforge/gambas/%{name}-%{version}.tar.bz2
Source1: %{name}.desktop

BuildRequires: bzip2-devel
BuildRequires: autoconf automake libtool
BuildRequires: unixODBC-devel
BuildRequires: gettext-devel
BuildRequires: png-devel
BuildRequires: imagemagick
BuildRequires: jpeg-devel
BuildRequires: sqlite3-devel
BuildRequires: qt4-devel
BuildRequires: glew-devel
BuildRequires: SDL-devel
BuildRequires: libxcursor-devel
BuildRequires: SDL_ttf-devel
BuildRequires: mysql-devel
BuildRequires: cairo-devel
BuildRequires: libpoppler-devel
BuildRequires: SDL_sound-devel
BuildRequires: SDL_mixer-devel
BuildRequires: curl-devel
BuildRequires: libgtk+2.0-devel
BuildRequires: librsvg2-devel
BuildRequires: gtkglext-devel
BuildRequires: libffi-devel
BuildRequires: imlib2-devel
BuildRequires: postgresql-devel
BuildRequires: libv4l-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: libxtst-devel
BuildRequires: xdg-utils
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(sqlite)

%description
Gambas is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic(tm) (but it is NOT a clone!). 
With Gambas, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, translate your program into many languages, 
create network applications easily, build RPMs of your apps 
automatically, and so on...
This is %{name} RC5

%prep
%setup -q -n %{name}-%{version}

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
%__rm -rf %{buildroot}
%makeinstall_std

find %{buildroot} -name '*.la' | xargs rm

%__install -D -m 755 app/src/%{name}/img/logo/logo-16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/gambas3.png
%__install -D -m 755 app/src/%{name}/img/logo/logo-32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/gambas3.png
%__install -D -m 755 app/src/%{name}/img/logo/logo-64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/gambas3.png
%__install -D -m 755 app/src/%{name}/img/logo/logo-ide.png %{buildroot}%{_datadir}/pixmaps/gambas3.png

desktop-file-install --vendor="" \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE1}

#-----------------------------------------------------------------------------

%package runtime
Summary: The Gambas runtime
Group: Development/Other

%description runtime
This package includes the Gambas interpreter needed to run Gambas applications.

%files runtime
%defattr(-, root, root, 0755)
%doc README AUTHORS ChangeLog
%{_bindir}/gbx3
%{_bindir}/gbr3
%{_libdir}/%{name}/gb.component
%{_libdir}/%{name}/gb.debug.*
%{_libdir}/%{name}/gb.eval.component
%{_libdir}/%{name}/gb.eval.so*
%{_libdir}/%{name}/gb.draw.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.info
%{_datadir}/%{name}/info/gb.list
%{_datadir}/%{name}/info/gb.debug.*
%{_datadir}/%{name}/info/gb.eval.list
%{_datadir}/%{name}/info/gb.eval.info
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/application-x-%{name}.png

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
Requires: %{name}-gb-db = %{version}
Requires: %{name}-gb-db-form = %{version}
Requires: %{name}-gb-desktop = %{version}
Requires: %{name}-gb-form = %{version}
Requires: %{name}-gb-form-dialog = %{version}
Requires: %{name}-gb-form-mdi = %{version}
Requires: %{name}-gb-qt4 = %{version}
Requires: %{name}-gb-qt4-ext = %{version}
Requires: %{name}-gb-qt4-webkit = %{version}
Requires: %{name}-gb-settings = %{version}
Requires: gettext
Requires: rpm-build

%description ide
This package includes the complete Gambas Development Environment, with the
database manager, the help files, and all components.

%files ide
%defattr(-, root, root, 0755)
%{_bindir}/%{name}
%{_bindir}/%{name}.gambas
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/*/%{name}.png
%{_datadir}/pixmaps/%{name}.png

#-----------------------------------------------------------------------------

%package examples
Summary: The Gambas examples
Group: Development/Other
Requires: %{name}-ide = %{version}

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
%{_libdir}/%{name}/gb.desktop.*
%{_datadir}/%{name}/info/gb.desktop.*
%{_datadir}/%{name}/control/gb.desktop

#-----------------------------------------------------------------------------

%package gb-eval-highlight
Summary: The Gambas eval-highlight component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-eval-highlight
This component implements the eval-highlight componet.

%files gb-eval-highlight
%defattr(-,root,root)
%{_libdir}/%{name}/gb.eval.highlight.*
%{_datadir}/%{name}/info/gb.eval.highlight.*

#-----------------------------------------------------------------------------

%package gb-form
Summary: The Gambas dialog form component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-form
This component implements the form control.

%files gb-form
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.component
%{_libdir}/%{name}/gb.form.gambas
%{_datadir}/%{name}/control/gb.form
%{_datadir}/%{name}/info/gb.form.info
%{_datadir}/%{name}/info/gb.form.list

#-----------------------------------------------------------------------------

%package gb-form-dialog
Summary: The Gambas dialog form component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-form-dialog
This component implements the form-dialog control.

%files gb-form-dialog
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.dialog.component
%{_libdir}/%{name}/gb.form.dialog.gambas
%{_datadir}/%{name}/info/gb.form.dialog.info
%{_datadir}/%{name}/info/gb.form.dialog.list

#-----------------------------------------------------------------------------

%package gb-form-mdi
Summary: The Gambas mdi form component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-form-mdi
This component implements the form-mdi control.

%files gb-form-mdi
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.mdi.component
%{_libdir}/%{name}/gb.form.mdi.gambas
%{_datadir}/%{name}/control/gb.form.mdi
%{_datadir}/%{name}/info/gb.form.mdi.info
%{_datadir}/%{name}/info/gb.form.mdi.list

#-----------------------------------------------------------------------------

%package gb-form-stock
Summary: The Gambas stock form component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-form-stock
This component implements the form-stock control.

%files gb-form-stock
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.stock.component
%{_libdir}/%{name}/gb.form.stock.gambas
%{_datadir}/%{name}/info/gb.form.stock.info
%{_datadir}/%{name}/info/gb.form.stock.list

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
%{_libdir}/%{name}/gb.image.component
%{_libdir}/%{name}/gb.image.so*
%{_datadir}/%{name}/info/gb.image.info
%{_datadir}/%{name}/info/gb.image.list

#-----------------------------------------------------------------------------

%package gb-image-effect
Summary: The Gambas image effect component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-image-effect
This component allows you to apply various effects to images.

%files gb-image-effect
%defattr(-,root,root)
%{_libdir}/%{name}/gb.image.effect.*
%{_datadir}/%{name}/info/gb.image.effect.*

#-----------------------------------------------------------------------------

%package gb-image-imlib
Summary: The Gambas image imlib component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-image-imlib
This component allows you to manipulate images with imlibs.

%files gb-image-imlib
%defattr(-,root,root)
%{_libdir}/%{name}/gb.image.imlib.*
%{_datadir}/%{name}/info/gb.image.imlib.*

#-----------------------------------------------------------------------------

%package gb-image-io
Summary: The Gambas image io component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-image-io
This component allows you to perform images input output operations.

%files gb-image-io
%defattr(-,root,root)
%{_libdir}/%{name}/gb.image.io.*
%{_datadir}/%{name}/info/gb.image.io.*

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
%{_libdir}/%{name}/gb.opengl.component
%{_libdir}/%{name}/gb.opengl.so*
%{_datadir}/%{name}/info/gb.opengl.info
%{_datadir}/%{name}/info/gb.opengl.list

#-----------------------------------------------------------------------------

%package gb-opengl-glsl
Summary: The Gambas opengl-glsl component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-opengl-glsl
This component allows you to use the Mesa libraries to do 3D operations.

%files gb-opengl-glsl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.opengl.glsl.*
%{_datadir}/%{name}/info/gb.opengl.glsl.*

#-----------------------------------------------------------------------------

%package gb-opengl-glu
Summary: The Gambas opengl-glu component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-opengl-glu
This component allows you to use the Mesa libraries to do 3D operations.

%files gb-opengl-glu
%defattr(-,root,root)
%{_libdir}/%{name}/gb.opengl.glu.*
%{_datadir}/%{name}/info/gb.opengl.glu.*

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
%{_libdir}/%{name}/gb.qt4.component
%{_libdir}/%{name}/gb.qt4.gambas
%{_libdir}/%{name}/gb.qt4.so*
%{_datadir}/%{name}/info/gb.qt4.info
%{_datadir}/%{name}/info/gb.qt4.list

#-----------------------------------------------------------------------------

%package gb-qt4-ext
Summary: The Gambas qt-ext component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-qt4-ext
This package contains the Gambas qt-ext components.

%files gb-qt4-ext
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt4.ext.*
%{_datadir}/%{name}/info/gb.qt4.ext.*

#-----------------------------------------------------------------------------

%package gb-qt4-opengl
Summary: The Gambas qt-opengl component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-qt4-opengl
This package contains the Gambas qt-opengl components.

%files gb-qt4-opengl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt4.opengl.*
%{_datadir}/%{name}/info/gb.qt4.opengl.*

#-----------------------------------------------------------------------------

%package gb-qt4-webkit
Summary: The Gambas qt-webkit component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-qt4-webkit
This package contains the Gambas qt-webkit components.

%files gb-qt4-webkit
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt4.webkit.*
%{_datadir}/%{name}/info/gb.qt4.webkit.*

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

