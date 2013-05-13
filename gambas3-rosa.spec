%define debug_package	%{nil}
Name:		gambas3
Summary:	Complete IDE based on a BASIC interpreter with object extensions
Version:	3.3.3
Release:	2
License:	GPLv2+
Group:		Development/Other
URL:		http://gambas.sourceforge.net
Source0:	http://ovh.dl.sourceforge.net/sourceforge/gambas/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch1:		gambas3-3.3.1-iconv.patch
Patch2:		gambas3-3.3.1-intl.patch
BuildRequires:	bzip2-devel
BuildRequires:	autoconf automake libtool
BuildRequires:	unixODBC-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	imagemagick
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(QtWebKit)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	SDL_sound-devel
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(gdk-2.0)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(gdkglext-1.0)
BuildRequires:	libffi-devel
BuildRequires:	pkgconfig(imlib2)
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libexslt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:	xdg-utils
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(sqlite)
BuildRequires:  libstdc++-static-devel 
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(gsl)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(SDL_image)
# keep gmime-devel for portability
BuildRequires:  pkgconfig(gmime-2.6)
# no media.component for rosalts
%if %{mdvver} >= 201210
BuildRequires:  llvm-devel
BuildRequires:  pkgconfig(gstreamer-0.10) >= 0.10.36
BuildRequires:  pkgconfig(gstreamer-app-0.10) >= 0.10.36
%else
BuildRequires:	llvm
%endif

%description
Gambas is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic(tm) (but it is NOT a clone!). 
With Gambas, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, translate your program into many languages, 
create network applications easily, build RPMs of your apps 
automatically, and so on...

%prep
%setup -q 
chmod -x main/gbx/gbx_local.h
chmod -x main/gbx/gbx_subr_file.c
chmod -x gb.qt4/src/CContainer.cpp
chmod -x main/lib/option/getoptions.*
chmod -x main/lib/option/main.c

%patch1 -p1 
%patch2 -p1 

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
%makeinstall_std

find %{buildroot} -name '*.la' -delete

rm -f %{buildroot}%{_libdir}/%{name}/gb.so %{buildroot}%{_libdir}/%{name}/gb.so.*

install -D -m 755 app/src/%{name}/img/logo/logo-16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m 755 app/src/%{name}/img/logo/logo-32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m 755 app/src/%{name}/img/logo/logo-64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -D -m 755 app/src/%{name}/img/logo/logo-ide.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop



#-----------------------------------------------------------------------------

%package runtime
Summary: The Gambas runtime
Group: Development/Other

%description runtime
This package includes the Gambas interpreter needed to run Gambas applications.
#
%files runtime 

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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
Requires: %{name}-gb-form-stock = %{version}
Requires: %{name}-gb-qt4 = %{version}
Requires: %{name}-gb-qt4-ext = %{version}
Requires: %{name}-gb-qt4-webkit = %{version}
Requires: %{name}-gb-settings = %{version}
Requires: %{name}-examples = %{version}
Requires: %{name}-gb-eval-highlight = %{version}
Requires: %{name}-gb-image = %{version}
Requires: %{name}-gb-image-effect = %{version}
Requires: gettext
Requires: rpm-build

%description ide
This package includes the complete Gambas Development Environment, with the
database manager, the help files, and all components.

%files ide 
%doc README AUTHORS ChangeLog
%{_bindir}/%{name}
%{_bindir}/%{name}.gambas
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/*/%{name}.png
%{_datadir}/pixmaps/%{name}.png

#-----------------------------------------------------------------------------

%package examples
Summary: The Gambas examples
Group: Development/Other
BuildArch: noarch
Requires: %{name}-ide = %{version}

%description examples
This package includes all the example projects provided with Gambas.

%files examples
%doc README AUTHORS ChangeLog
%{_datadir}/%{name}/examples

#-----------------------------------------------------------------------------

%package gb-cairo
Summary: The Gambas Cairo component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-cairo
This package contains the Gambas Cario components.

%files gb-cairo
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.gtk.*
%{_datadir}/%{name}/info/gb.gtk.*

#-----------------------------------------------------------------------------
%package gb-gsl
Summary: The Gambas interface to the GNU Scientific Library 
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-gsl
This component provides an interface to the GNU Scientific Library.

%files gb-gsl
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.gsl.*
%{_datadir}/%{name}/info/gb.gsl.*

#-----------------------------------------------------------------------------
%package gb-gui
Summary: The Gambas GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-gui
This is a component that just loads gb.qt if you are running KDE or
gb.gtk in the other cases.

%files gb-gui
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.gui.*
%{_datadir}/%{name}/info/gb.gui.*

#-----------------------------------------------------------------------------
%if %{mdvver} >= 201210
%package gb-jit
Summary: The Gambas JIT component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-jit
This component provides the jit compiler for gambas.

%files gb-jit
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.jit.*
%{_datadir}/%{name}/info/gb.jit.*
%endif
#-----------------------------------------------------------------------------
%package gb-image
Summary: The Gambas image manipulation component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-image
This component allows you to apply various effects to images.

%files gb-image
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.image.io.*
%{_datadir}/%{name}/info/gb.image.io.*

#-----------------------------------------------------------------------------
%if %{mdvver} >= 201210
%package gb-media
Summary: The Gambas media component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-media
This package contains the Gambas media component.

%files gb-media
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.media.*
%{_datadir}/%{name}/info/gb.media.*
%endif
#-----------------------------------------------------------------------------
%package gb-mysql
Summary: The Gambas mysql component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-mysql
This package contains the Gambas MySQL components.

%files gb-mysql
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.mysql.*
%{_datadir}/%{name}/info/gb.mysql.*

#-----------------------------------------------------------------------------
%package gb-ncurses
Summary: The Gambas ncurses component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-ncurses
This component allows you to use ncurses with gambas.

%files gb-ncurses
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.ncurses.so*
%{_libdir}/%{name}/gb.ncurses.component
%{_datadir}/%{name}/info/gb.ncurses.info
%{_datadir}/%{name}/info/gb.ncurses.list

#---------------------------------------------------------------------------
%package gb-net
Summary: The Gambas networking component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-net
This component allows you to use TCP/IP and UDP sockets, and to access
any serial ports.

%files gb-net
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
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
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.web.*
%{_datadir}/%{name}/info/gb.web.*

#-----------------------------------------------------------------------------
%package gb-libxml
Summary: The Gambas libxml component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-libxml
This component allows you to use xml.

%files gb-libxml
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.libxml.so*
%{_libdir}/%{name}/gb.libxml.component
%{_datadir}/%{name}/info/gb.libxml.info
%{_datadir}/%{name}/info/gb.libxml.list

#------------------------------------------------------------------------------
%package gb-xml
Summary: The Gambas xml component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-xml
This component allows you to use xml.

%files gb-xml
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.xml.gambas
%{_libdir}/%{name}/gb.xml.so*
%{_libdir}/%{name}/gb.xml.component
%{_datadir}/%{name}/info/gb.xml.info
%{_datadir}/%{name}/info/gb.xml.list

#-----------------------------------------------------------------------------
%package gb-xml-html
Summary: The Gambas xml html component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Requires: %{name}-gb-xml

%description gb-xml-html
This component allows you to use xml html.

%files gb-xml-html
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.xml.html.so*
%{_libdir}/%{name}/gb.xml.html.component
%{_datadir}/%{name}/info/gb.xml.html.info
%{_datadir}/%{name}/info/gb.xml.html.list

#-----------------------------------------------------------------------------
%package gb-xml-rpc
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Requires: %{name}-gb-xml

%description gb-xml-rpc
This component allows you to use xml-rpc.

%files gb-xml-rpc
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.xml.rpc*
# added info, list
%{_datadir}/%{name}/info/gb.xml.rpc.info
%{_datadir}/%{name}/info/gb.xml.rpc.list


#-----------------------------------------------------------------------------

%package gb-xml-xslt
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-xml-xslt
This component allows you to use xml-xslt.

%files gb-xml-xslt
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.xml.xslt*
%{_datadir}/%{name}/info/gb.xml.xslt*

#-----------------------------------------------------------------------------
%package gb-complex
Summary: The Gambas complex component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-complex
New component that implements a rudimentary management of complex numbers. 
This component is automatically loaded if a complex 
number constant is encountered and no loaded component 
can already handle complex numbers.

%files gb-complex
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.complex*
%{_datadir}/%{name}/info/gb.complex*
#-----------------------------------------------------------------------------

%package gb-data
Summary: The Gambas data component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-data
New component that adds new container datatypes to Gambas.

%files gb-data
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.data*
%{_datadir}/%{name}/info/gb.data*
#-----------------------------------------------------------------------------
%package gb-mime
Summary: The Gambas mime component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-mime
New component that allows to encode and decode MIME messages.

%files gb-mime
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.mime.* 
%{_datadir}/%{name}/info/gb.mime.*         
#----------------------------------------------------------------------------
%package gb-net-pop3
Summary:	Gambas3 component package for net-pop3
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-net-pop3
New component that implements a POP3 client.

%files gb-net-pop3
%doc README AUTHORS ChangeLog
%{_libdir}/%{name}/gb.net.pop3.*
%{_datadir}/%{name}/info/gb.net.pop3.*
#---------------------------------------------------------------------------


%post runtime
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun runtime
update-mime-database %{_datadir}/mime &> /dev/null || :

%post script
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun script
update-mime-database %{_datadir}/mime &> /dev/null || :

