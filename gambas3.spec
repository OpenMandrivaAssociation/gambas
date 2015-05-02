Name:		gambas3
Summary:	Complete IDE based on a BASIC interpreter with object extensions
Version:	3.7.1
Release:	1
License:	GPLv2+
Group:		Development/Other
URL:		http://gambas.sourceforge.net
Source0:    http://garr.dl.sourceforge.net/project/gambas/gambas3/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source100:	%{name}.rpmlintrc

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
#
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	SDL_sound-devel
BuildRequires:  pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	SDL_sound-devel
#
#sdl2 has to be ported to 2014.0
BuildRequires:	pkgconfig(sdl2) >= 2.0.2
BuildRequires:	pkgconfig(SDL2_mixer) >= 2.0.0
BuildRequires:  pkgconfig(SDL2_image) >= 2.0.0
BuildRequires:	pkgconfig(SDL2_ttf) >= 2.0.12
#
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(gdk-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(gdkglext-1.0)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(imlib2)
BuildRequires:	pkgconfig(libecpg)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libexslt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:  freetype-devel
BuildRequires:	xdg-utils
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(sqlite)
BuildRequires:  libstdc++-static-devel 
BuildRequires:  libstdc++-devel
BuildRequires:  freetype-devel
BuildRequires:  pkgconfig(gsl)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(dbus-1)

# no pkgconfig for gmime for portability
BuildRequires:  gmime-devel
BuildRequires:  pkgconfig(libv4lconvert)
BuildRequires:  llvm-devel >= 3.4
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  gmp-devel
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(alure)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(libmpg123)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  dumb-devel

%description
Gambas is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic(tm) (but it is NOT a clone!). 
With Gambas, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, translate your program into many languages, 
create network applications easily, build RPMs of your apps 
automatically, and so on...

%prep
%setup -q

for i in `find . -name "acinclude.m4"`;
do
	sed -i -e 's|AM_CONFIG_HEADER|AC_CONFIG_HEADERS|g' ${i}
	sed -i 's|$AM_CFLAGS -O3|$AM_CFLAGS|g' ${i}
	sed -i 's|$AM_CXXFLAGS -Os -fno-omit-frame-pointer|$AM_CXXFLAGS|g' ${i}
	sed -i 's|$AM_CFLAGS -Os|$AM_CFLAGS|g' ${i}
	sed -i 's|$AM_CFLAGS -O0|$AM_CFLAGS|g' ${i}
	sed -i 's|$AM_CXXFLAGS -O0|$AM_CXXFLAGS|g' ${i}
done



# debug linting fix
chmod -x main/gbx/gbx_local.h
chmod -x gb.xml/src/xslt/CXSLT.h
chmod -x main/lib/option/main.h
chmod -x main/lib/option/main.c
chmod -x main/lib/option/getoptions.c
chmod -x main/lib/option/getoptions.h
chmod -x main/gbx/gbx_subr_file.c
chmod -x gb.xml/src/xslt/main.cpp
chmod -x gb.qt4/src/CContainer.cpp
chmod -x gb.xml/src/xslt/CXSLT.cpp



%build
# add math's functions to the linker
export LDFLAGS="$LDFLAGS -lm"
# export pow, ceil a.s.o math's functions
# in both compilers , gb.image component is in C
export CXXFLAGS="%{optflags} -lm"
export CFLAGS="%{optflags} -lm"


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

# Get the SVN noise out of the main tree
find %{buildroot}%{_datadir}/%{name}/ -type d -name .svn -exec rm -rf {} 2>/dev/null ';' || :

# Mime types.
mkdir -p %{buildroot}%{_datadir}/mime/packages/
install -m 0644 -p app/mime/application-x-gambasscript.xml %{buildroot}%{_datadir}/mime/packages/
install -m 0644 -p main/mime/application-x-gambas3.xml %{buildroot}%{_datadir}/mime/packages/

# clean, should be done upstream
find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_libdir}/%{name}/gb.so %{buildroot}%{_libdir}/%{name}/gb.so.*

# menu entry && icons
install -D -m 755 app/src/%{name}/img/logo/logo-16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m 755 app/src/%{name}/img/logo/logo-32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m 755 app/src/%{name}/img/logo/logo-64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -D -m 755 app/src/%{name}/img/logo/logo-ide.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
chmod -x %{buildroot}%{_datadir}/applications/%{name}.desktop 
chmod -x %{buildroot}%{_datadir}/appdata/gambas3.appdata.xml

mkdir -p %{buildroot}%{_docdir}


#------------------------------------------------------------------------
%package runtime
Summary: The Gambas runtime
Group: Development/Other

%description runtime
This package includes the Gambas interpreter needed to run Gambas applications.

%files runtime 
%doc README ChangeLog AUTHORS
%{_bindir}/gbx3
%{_bindir}/gbr3
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.component
%{_libdir}/%{name}/gb.debug.*
%{_libdir}/%{name}/gb.eval.component
%{_libdir}/%{name}/gb.eval.so*
%{_libdir}/%{name}/gb.draw.*
%{_libdir}/%{name}/gb.geom.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.info
%{_datadir}/%{name}/info/gb.list
%{_datadir}/%{name}/info/gb.debug.*
%{_datadir}/%{name}/info/gb.eval.list
%{_datadir}/%{name}/info/gb.eval.info
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/application-x-%{name}.png
%{_datadir}/appdata/gambas3.appdata.xml

#-----------------------------------------------------------------------------

%package devel
Summary: The Gambas development package
Group: Development/Other

%description devel
This package includes all tools needed to compile Gambas projects
without having to install the complete development environment.

%files devel
%doc README  ChangeLog 
%{_bindir}/gbc3
%{_bindir}/gba3
%{_bindir}/gbi3
# help will not compile reported upstream.
%ifarch %{ix86}
%{_bindir}/gbh3
%{_bindir}/gbh3.gambas
%endif

#-----------------------------------------------------------------------------

%package script
Summary: The Gambas scripter package
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}


%description script
This package includes the scripter program that allows to write script files
in Gambas.

%files script
%doc README  ChangeLog 
%{_bindir}/gbs3
%{_bindir}/gbs3.gambas
%{_bindir}/gbw3
%{_datadir}/%{name}/icons/application-x-gambasserverpage.png
%{_datadir}/%{name}/icons/application-x-gambasscript.png

#-----------------------------------------------------------------------------

%package ide
Summary: The Gambas IDE
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-devel = %{EVRD}
Requires: %{name}-gb-db = %{EVRD}
Requires: %{name}-gb-db-form = %{EVRD}
Requires: %{name}-gb-desktop = %{EVRD}
Requires: %{name}-gb-eval-highlight = %{EVRD}
Requires: %{name}-gb-form = %{EVRD}
Requires: %{name}-gb-form-dialog = %{EVRD}
Requires: %{name}-gb-form-mdi = %{EVRD}
Requires: %{name}-gb-form-stock = %{EVRD}
Requires: %{name}-gb-gui = %{EVRD}
Requires: %{name}-gb-image = %{EVRD}
Requires: %{name}-gb-image-effect = %{EVRD}
Requires: %{name}-gb-qt4 = %{EVRD}
Requires: %{name}-gb-qt4-ext = %{EVRD}
Requires: %{name}-gb-qt4-webkit = %{EVRD}
Requires: %{name}-gb-settings = %{EVRD}
Requires: %{name}-gb-clipper
Requires: %{name}-gb-markdown
Requires: gettext
Requires: rpm-build

%description ide
This package includes the complete Gambas Development Environment, with the
database manager, the help files, and all components.

%files ide 
%doc README ChangeLog 
%{_bindir}/%{name}
%{_bindir}/%{name}.gambas
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/*/%{name}.png
%{_datadir}/pixmaps/%{name}.png


#-----------------------------------------------------------------------------

%package gb-cairo
Summary: The Gambas Cairo component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-cairo
This package contains the Gambas Cario components.

%files gb-cairo
%doc README  ChangeLog
%{_libdir}/%{name}/gb.cairo.*
%{_datadir}/%{name}/info/gb.cairo.*

#-----------------------------------------------------------------------------

%package gb-chart
Summary: The Gambas chart component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-chart
This package contains the Gambas Chart components.

%files gb-chart
%doc README  ChangeLog
%{_libdir}/%{name}/gb.chart.*
%{_datadir}/%{name}/info/gb.chart.*

#-----------------------------------------------------------------------------

%package gb-compress
Summary: The Gambas compression component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-compress
This component allows you to compress/uncompress data or files with
the bzip2 and zip algorithms.

%files gb-compress
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.compress.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.compress.*

#-----------------------------------------------------------------------------

%package gb-crypt
Summary: The Gambas cryptography component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-crypt
This component allows you to use cryptography in your projects.

%files gb-crypt
%doc README  ChangeLog
%{_libdir}/%{name}/gb.crypt.*
%{_datadir}/%{name}/info/gb.crypt.*

#-----------------------------------------------------------------------------

%package gb-db
Summary: The Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-db
This component allows you to access many databases management systems,
provided that you install the needed driver packages.

%files gb-db
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.db.so*
%{_libdir}/%{name}/gb.db.component
%{_libdir}/%{name}/gb.db.gambas
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.db.info
%{_datadir}/%{name}/info/gb.db.list

#-----------------------------------------------------------------------------

%package gb-db-form
Summary: The Gambas db-form component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-db-form
This package contains the Gambas Database form components.

%files gb-db-form
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.db.form.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.db.form.*
%dir %{_datadir}/%{name}/control
%{_datadir}/%{name}/control/gb.db.form

#-----------------------------------------------------------------------------
%package gb-db-mysql
Summary: The MySQL driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-db = %{EVRD}

%description gb-db-mysql
This component allows you to access MySQL databases.

%files gb-db-mysql
%doc README  ChangeLog
%{_libdir}/%{name}/gb.db.mysql.*
%{_datadir}/%{name}/info/gb.db.mysql.info
%{_datadir}/%{name}/info/gb.db.mysql.list

#-----------------------------------------------------------------------------
%package gb-db-odbc
Summary: The ODBC driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-db = %{EVRD}

%description gb-db-odbc
This component allows you to access ODBC databases.

%files gb-db-odbc
%doc README  ChangeLog
%{_libdir}/%{name}/gb.db.odbc.*
%{_datadir}/%{name}/info/gb.db.odbc.info
%{_datadir}/%{name}/info/gb.db.odbc.list

#-----------------------------------------------------------------------------
%package gb-db-postgresql
Summary: The PostgreSQL driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-db = %{EVRD}

%description gb-db-postgresql
This component allows you to access PostgreSQL databases.

%files gb-db-postgresql
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.db.postgresql.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.db.postgresql.info
%{_datadir}/%{name}/info/gb.db.postgresql.list

#-----------------------------------------------------------------------------
%package gb-db-sqlite2
Summary: The SQLite 2 driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-db = %{EVRD}

%description gb-db-sqlite2
This component allows you to access SQLite 2 databases.

%files gb-db-sqlite2
%doc README  ChangeLog
%{_libdir}/%{name}/gb.db.sqlite2.*
%{_datadir}/%{name}/info/gb.db.sqlite2.info
%{_datadir}/%{name}/info/gb.db.sqlite2.list

#-----------------------------------------------------------------------------

%package gb-db-sqlite3
Summary: The SQLite 3 driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-db = %{EVRD}

%description gb-db-sqlite3
This component allows you to access SQLite 3 databases.

%files gb-db-sqlite3
%doc README  ChangeLog
%{_libdir}/%{name}/gb.db.sqlite3.*
%{_datadir}/%{name}/info/gb.db.sqlite3.info
%{_datadir}/%{name}/info/gb.db.sqlite3.list

#-----------------------------------------------------------------------------

%package gb-dbus
Summary: The Gambas dbus component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-dbus
This package contains the Gambas D-bus components.

%files gb-dbus
%doc README  ChangeLog
%{_libdir}/%{name}/gb.dbus.*
%{_datadir}/%{name}/info/gb.dbus.*

#-----------------------------------------------------------------------------

%package gb-desktop
Summary: The Gambas XDG component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-desktop
This component allows you to use desktop-agnostic routines based on 
the xdg-utils scripts of the Portland project.

%files gb-desktop
%doc README  ChangeLog
%{_libdir}/%{name}/gb.desktop.*
%{_datadir}/%{name}/info/gb.desktop.*
%{_datadir}/%{name}/control/gb.desktop

#-----------------------------------------------------------------------------

%package gb-eval-highlight
Summary: The Gambas eval-highlight component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-eval-highlight
This component implements the eval-highlight component.

%files gb-eval-highlight
%doc README  ChangeLog
%{_libdir}/%{name}/gb.eval.highlight.*
%{_datadir}/%{name}/info/gb.eval.highlight.*

#-----------------------------------------------------------------------------

%package gb-form
Summary: The Gambas dialog form component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-form
This component implements the form control.

%files gb-form
%doc README  ChangeLog
%{_libdir}/%{name}/gb.form.component
%{_libdir}/%{name}/gb.form.gambas
%{_datadir}/%{name}/control/gb.form
%{_datadir}/%{name}/info/gb.form.info
%{_datadir}/%{name}/info/gb.form.list

#-----------------------------------------------------------------------------

%package gb-form-dialog
Summary: The Gambas dialog form component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-form-dialog
This component implements the form-dialog control.

%files gb-form-dialog
%doc README  ChangeLog
%{_libdir}/%{name}/gb.form.dialog.component
%{_libdir}/%{name}/gb.form.dialog.gambas
%{_datadir}/%{name}/info/gb.form.dialog.info
%{_datadir}/%{name}/info/gb.form.dialog.list

#-----------------------------------------------------------------------------

%package gb-form-mdi
Summary: The Gambas mdi form component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-form-mdi
This component implements the form-mdi control.

%files gb-form-mdi
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.form.mdi.component
%{_libdir}/%{name}/gb.form.mdi.gambas
%dir %{_datadir}/%{name}/control
%{_datadir}/%{name}/control/gb.form.mdi
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.form.mdi.info
%{_datadir}/%{name}/info/gb.form.mdi.list

#-----------------------------------------------------------------------------

%package gb-form-stock
Summary: The Gambas stock form component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-form-stock
This component implements the form-stock control.

%files gb-form-stock
%doc README  ChangeLog
%{_libdir}/%{name}/gb.form.stock.component
%{_libdir}/%{name}/gb.form.stock.gambas
%{_datadir}/%{name}/info/gb.form.stock.info
%{_datadir}/%{name}/info/gb.form.stock.list

#-----------------------------------------------------------------------------

%package gb-gtk
Summary: The Gambas GTK+ GUI component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-gtk
This package contains the Gambas GTK+ GUI components.

%files gb-gtk
%doc README  ChangeLog
%dir %{_datadir}/%{name}/info
%{_libdir}/%{name}/gb.gtk.*
%{_datadir}/%{name}/info/gb.gtk.*

#-----------------------------------------------------------------------------
%package gb-gsl
Summary: The Gambas interface to the GNU Scientific Library 
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-gsl
This component provides an interface to the GNU Scientific Library.

%files gb-gsl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.gsl.*
%{_datadir}/%{name}/info/gb.gsl.*

#-----------------------------------------------------------------------------
%package gb-gui
Summary: The Gambas GUI component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-gui
This is a component that just loads gb.qt if you are running KDE or
gb.gtk in the other cases.

%files gb-gui
%doc README  ChangeLog
%{_libdir}/%{name}/gb.gui.*
%{_datadir}/%{name}/info/gb.gui.*

#-----------------------------------------------------------------------------
#%if %{mdvver} < 201410
%package gb-jit
Summary: The Gambas JIT component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-jit
This component provides the jit compiler for gambas.

%files gb-jit
%doc README  ChangeLog
%{_libdir}/%{name}/gb.jit.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.jit.info
%{_datadir}/%{name}/info/gb.jit.list
#%endif
#-----------------------------------------------------------------------------
%package gb-image
Summary: The Gambas image manipulation component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-image
This component allows you to apply various effects to images.

%files gb-image
%doc README  ChangeLog
%{_libdir}/%{name}/gb.image.component
%{_libdir}/%{name}/gb.image.so*
%{_datadir}/%{name}/info/gb.image.info
%{_datadir}/%{name}/info/gb.image.list

#-----------------------------------------------------------------------------

%package gb-image-effect
Summary: The Gambas image effect component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-image-effect
This component allows you to apply various effects to images.

%files gb-image-effect
%doc README  ChangeLog
%{_libdir}/%{name}/gb.image.effect.*
%{_datadir}/%{name}/info/gb.image.effect.*

#-----------------------------------------------------------------------------

%package gb-image-imlib
Summary: The Gambas image imlib component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-image-imlib
This component allows you to manipulate images with imlibs.

%files gb-image-imlib
%doc README  ChangeLog
%{_libdir}/%{name}/gb.image.imlib.*
%{_datadir}/%{name}/info/gb.image.imlib.*

#-----------------------------------------------------------------------------

%package gb-image-io
Summary: The Gambas image io component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-image-io
This component allows you to perform images input output operations.

%files gb-image-io
%doc README  ChangeLog
%{_libdir}/%{name}/gb.image.io.*
%{_datadir}/%{name}/info/gb.image.io.*

#-----------------------------------------------------------------------------
# we don't have gst-1 in lts
%if %{mdvver} >= 201210
%package gb-media
Summary: The Gambas media component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-media
This package contains the Gambas media component.

%files gb-media
%doc README  ChangeLog
%{_libdir}/%{name}/gb.media.*
%{_datadir}/%{name}/info/gb.media.*
%{_datadir}/%{name}/control/gb.media.form/mediaview.png
%endif

#-----------------------------------------------------------------------------
%package gb-mysql
Summary: The Gambas mysql component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-mysql
This package contains the Gambas MySQL components.

%files gb-mysql
%doc README  ChangeLog
%{_libdir}/%{name}/gb.mysql.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.mysql.*

#-----------------------------------------------------------------------------
%package gb-ncurses
Summary: The Gambas ncurses component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-ncurses
This component allows you to use ncurses with gambas.

%files gb-ncurses
%doc README  ChangeLog
%{_libdir}/%{name}/gb.ncurses.so*
%{_libdir}/%{name}/gb.ncurses.component
%{_datadir}/%{name}/info/gb.ncurses.info
%{_datadir}/%{name}/info/gb.ncurses.list

#---------------------------------------------------------------------------
%package gb-net
Summary: The Gambas networking component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-net
This component allows you to use TCP/IP and UDP sockets, and to access
any serial ports.

%files gb-net
%doc README  ChangeLog
%{_libdir}/%{name}/gb.net.so*
%{_libdir}/%{name}/gb.net.component
%{_datadir}/%{name}/info/gb.net.info
%{_datadir}/%{name}/info/gb.net.list

#-----------------------------------------------------------------------------

%package gb-net-curl
Summary: The Gambas advanced networking component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-net = %{EVRD}

%description gb-net-curl
This component allows your programs to easily become FTP or HTTP clients.

%files gb-net-curl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.net.curl.so*
%{_libdir}/%{name}/gb.net.curl.component
%{_libdir}/%{name}/gb.net.curl.gambas
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.net.curl.info
%{_datadir}/%{name}/info/gb.net.curl.list

#-----------------------------------------------------------------------------

%package gb-net-smtp
Summary: The Gambas SMTP component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-net = %{EVRD}

%description gb-net-smtp
This component allows you to send emails using the SMTP protocol.

%files gb-net-smtp
%doc README  ChangeLog
%{_libdir}/%{name}/gb.net.smtp.*
%{_datadir}/%{name}/info/gb.net.smtp.*
%{_datadir}/%{name}/control/gb.net.smtp/smtpclient.png

#-----------------------------------------------------------------------------

%package gb-opengl
Summary: The Gambas OpenGL component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-opengl
This component allows you to use the Mesa libraries to do 3D operations.

%files gb-opengl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.opengl.component
%{_libdir}/%{name}/gb.opengl.so*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.opengl.info
%{_datadir}/%{name}/info/gb.opengl.list

#-----------------------------------------------------------------------------

%package gb-opengl-glsl
Summary: The Gambas opengl-glsl component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-opengl-glsl
This component allows you to use the Mesa libraries to do 3D operations.

%files gb-opengl-glsl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.opengl.glsl.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.opengl.glsl.*

#-----------------------------------------------------------------------------

%package gb-opengl-glu
Summary: The Gambas opengl-glu component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-opengl-glu
This component allows you to use the Mesa libraries to do 3D operations.

%files gb-opengl-glu
%doc README  ChangeLog
%{_libdir}/%{name}/gb.opengl.glu.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.opengl.glu.*

#-----------------------------------------------------------------------------

%package gb-option
Summary: The Gambas command-line option component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-option
This component allows you to interpret command-line options.

%files gb-option
%doc README  ChangeLog
%{_libdir}/%{name}/gb.option.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.option.*

#-----------------------------------------------------------------------------

%package gb-pcre
Summary: The Gambas PCRE component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-pcre
This component allows you to use Perl compatible regular expressions
within Gambas code.

%files gb-pcre
%doc README  ChangeLog
%{_libdir}/%{name}/gb.pcre.*
%{_datadir}/%{name}/info/gb.pcre.*

#-----------------------------------------------------------------------------

%package gb-pdf
Summary: The Gambas PDF component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-pdf
This component allows you to manipulate pdf files with Gambas code.

%files gb-pdf
%doc README  ChangeLog
%{_libdir}/%{name}/gb.pdf.*
%{_datadir}/%{name}/info/gb.pdf.*

#-----------------------------------------------------------------------------

%package gb-qt4
Summary: The Gambas Qt GUI component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-qt4
This package includes the Gambas QT GUI component.

%files gb-qt4
%doc README  ChangeLog
%{_libdir}/%{name}/gb.qt4.component
%{_libdir}/%{name}/gb.qt4.so*
%{_datadir}/%{name}/info/gb.qt4.info
%{_datadir}/%{name}/info/gb.qt4.list

#-----------------------------------------------------------------------------

%package gb-qt4-ext
Summary: The Gambas qt-ext component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-qt4-ext
This package contains the Gambas qt-ext components.

%files gb-qt4-ext
%doc README  ChangeLog
%{_libdir}/%{name}/gb.qt4.ext.*
%{_datadir}/%{name}/info/gb.qt4.ext.*

#-----------------------------------------------------------------------------

%package gb-qt4-opengl
Summary: The Gambas qt-opengl component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-qt4-opengl
This package contains the Gambas qt-opengl components.

%files gb-qt4-opengl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.qt4.opengl.*
%{_datadir}/%{name}/info/gb.qt4.opengl.*

#-----------------------------------------------------------------------------

%package gb-qt4-webkit
Summary: The Gambas qt-webkit component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-qt4-webkit
This package contains the Gambas qt-webkit components.

%files gb-qt4-webkit
%doc README  ChangeLog
%{_libdir}/%{name}/gb.qt4.webkit.*
%{_datadir}/%{name}/info/gb.qt4.webkit.*

#-----------------------------------------------------------------------------

%package gb-report
Summary: The Gambas report component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-report
This package contains the Gambas Report components.

%files gb-report
%doc README  ChangeLog
%{_libdir}/%{name}/gb.report.*
%{_datadir}/%{name}/info/gb.report.*
%{_datadir}/%{name}/control/gb.report

#-----------------------------------------------------------------------------

%package gb-sdl
Summary: The Gambas SDL component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-sdl
This component use the sound, image and TTF fonts parts of the SDL
library. It allows you to simultaneously play many sounds and music
stored in a file. If OpenGL drivers are installed it uses them to 
accelerate 2D and 3D drawing.

%files gb-sdl
%doc README  ChangeLog 
%{_libdir}/%{name}/gb.sdl.so
%{_libdir}/%{name}/gb.sdl.so.*
%{_libdir}/%{name}/gb.sdl.component
%{_datadir}/%{name}/info/gb.sdl.info
%{_datadir}/%{name}/info/gb.sdl.list


#-----------------------------------------------------------------------------
%package gb-sdl2
Summary: The Gambas SDL2 component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-sdl2
This component use the sound, image and TTF fonts parts of the SDL2
library. It allows you to simultaneously play many sounds and music
stored in a file. If OpenGL drivers are installed it uses them to 
accelerate 2D and 3D drawing.

%files gb-sdl2
%doc README  ChangeLog 
%{_libdir}/%{name}/gb.sdl2.so
%{_libdir}/%{name}/gb.sdl2.so.*
%{_libdir}/%{name}/gb.sdl2.component
%{_datadir}/%{name}/info/gb.sdl2.info
%{_datadir}/%{name}/info/gb.sdl2.list

#-----------------------------------------------------------------------------

%package gb-sdl-sound
Summary: The Gambas SDL sound component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-sdl-sound
This component allows you to play sounds in Gambas. This component 
manages up to 32 sound tracks that can play sounds from memory, and
one music track that can play music from a file. Everything is mixed
in real time. 

%files gb-sdl-sound
%doc README  ChangeLog
%{_libdir}/%{name}/gb.sdl.sound.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.sdl.sound.*

#-----------------------------------------------------------------------------
%package gb-sdl2-sound
Summary: The Gambas SDL sound component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-sdl2-sound
This component allows you to play sounds in Gambas. This component 
manages up to 32 sound tracks that can play sounds from memory, and
one music track that can play music from a file. Everything is mixed
in real time  using SDL2.

%files gb-sdl2-sound
%doc README  ChangeLog
%{_libdir}/%{name}/gb.sdl2.audio.component
%{_libdir}/%{name}/gb.sdl2.audio.so
%{_libdir}/%{name}/gb.sdl2.audio.so.0
%{_libdir}/%{name}/gb.sdl2.audio.so.0.0.0
%{_datadir}/%{name}/info/gb.sdl2.audio.info
%{_datadir}/%{name}/info/gb.sdl2.audio.list

#-----------------------------------------------------------------------------
%package gb-settings
Summary: The Gambas settings component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-settings
This components allows you to deal with configuration files.

%files gb-settings
%doc README  ChangeLog
%{_libdir}/%{name}/gb.settings.*
%{_datadir}/%{name}/info/gb.settings.*

#-----------------------------------------------------------------------------

%package gb-signal
Summary: The Gambas signal component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-signal
This package contains the Gambas Signal components.

%files gb-signal
%doc README  ChangeLog
%{_libdir}/%{name}/gb.signal.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.signal.*

#-----------------------------------------------------------------------------

%package gb-v4l
Summary: The Gambas Video4Linux component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-v4l
This components allows you to use the Video4Linux interface with
Gambas.

%files gb-v4l
%doc README  ChangeLog
%{_libdir}/%{name}/gb.v4l.*
%{_datadir}/%{name}/info/gb.v4l.*

#-----------------------------------------------------------------------------

%package gb-vb
Summary: The Gambas Visual Basic(tm) compatibility component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-vb
This component aims at including some functions that imitate the 
behavior
 of Visual Basic(TM) functions. Use it only if you want to 
port some VB projects.

%files gb-vb
%doc README  ChangeLog
%{_libdir}/%{name}/gb.vb.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.vb.*

#-----------------------------------------------------------------------------

%package gb-web
Summary: The Gambas CGI component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-web
This components allows you to make CGI web applications using Gambas, 
with an ASP-like interface.

%files gb-web
%doc README  ChangeLog
%{_libdir}/%{name}/gb.web.*
%{_datadir}/%{name}/info/gb.web.*

#-----------------------------------------------------------------------------
%package gb-libxml
Summary: The Gambas libxml component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-libxml
This component allows you to use xml.

%files gb-libxml
%doc README  ChangeLog
%{_libdir}/%{name}/gb.libxml.so*
%{_libdir}/%{name}/gb.libxml.component
%{_datadir}/%{name}/info/gb.libxml.info
%{_datadir}/%{name}/info/gb.libxml.list

#------------------------------------------------------------------------------
%package gb-xml
Summary: The Gambas xml component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-xml
This component allows you to use xml.

%files gb-xml
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.xml.gambas
%{_libdir}/%{name}/gb.xml.so*
%{_libdir}/%{name}/gb.xml.component
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.xml.info
%{_datadir}/%{name}/info/gb.xml.list

#-----------------------------------------------------------------------------
%package gb-xml-html
Summary: The Gambas xml html component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-xml

%description gb-xml-html
This component allows you to use xml html.

%files gb-xml-html
%doc README  ChangeLog
%{_libdir}/%{name}/gb.xml.html.so*
%{_libdir}/%{name}/gb.xml.html.component
%{_datadir}/%{name}/info/gb.xml.html.info
%{_datadir}/%{name}/info/gb.xml.html.list

#-----------------------------------------------------------------------------
%package gb-xml-rpc
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}
Requires: %{name}-gb-xml

%description gb-xml-rpc
This component allows you to use xml-rpc.

%files gb-xml-rpc
%doc README  ChangeLog
%{_libdir}/%{name}/gb.xml.rpc*
%{_datadir}/%{name}/info/gb.xml.rpc.info
%{_datadir}/%{name}/info/gb.xml.rpc.list


#-----------------------------------------------------------------------------

%package gb-xml-xslt
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-xml-xslt
This component allows you to use xml-xslt.

%files gb-xml-xslt
%doc README  ChangeLog
%{_libdir}/%{name}/gb.xml.xslt*
%{_datadir}/%{name}/info/gb.xml.xslt*

#-----------------------------------------------------------------------------
%package gb-complex
Summary: The Gambas complex component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-complex
New component that implements a rudimentary management of complex numbers. 
This component is automatically loaded if a complex 
number constant is encountered and no loaded component 
can already handle complex numbers.

%files gb-complex
%doc README  ChangeLog
%{_libdir}/%{name}/gb.complex*
%{_datadir}/%{name}/info/gb.complex*
#-----------------------------------------------------------------------------

%package gb-data
Summary: The Gambas data component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-data
New component that adds new container data types to Gambas.

%files gb-data
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.data*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.data*
#-----------------------------------------------------------------------------
%package gb-mime
Summary: The Gambas mime component
Group: Development/Other
Requires: %{name}-runtime = %{EVRD}

%description gb-mime
New component that allows to encode and decode MIME messages.

%files gb-mime
%doc README  ChangeLog
%{_libdir}/gambas3/gb.mime.component
%{_libdir}/gambas3/gb.mime.so
%{_libdir}/gambas3/gb.mime.so.0
%{_libdir}/gambas3/gb.mime.so.0.0.0
%{_datadir}/gambas3/info/gb.mime.info
%{_datadir}/gambas3/info/gb.mime.list
%{_datadir}/mime/packages/application-x-gambas3.xml
%{_datadir}/mime/packages/application-x-gambasscript.xml

#----------------------------------------------------------------------------
%package gb-net-pop3
Summary:	Gambas3 component package for net-pop3
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}
Requires:	%{name}-gb-mime

%description gb-net-pop3
New component that implements a POP3 client.

%files gb-net-pop3
%doc README  ChangeLog
%{_libdir}/%{name}/gb.net.pop3.*
%{_datadir}/%{name}/info/gb.net.pop3.*
%{_datadir}/%{name}/control/gb.net.pop3/pop3client.png

#---------------------------------------------------------------------------

%package gb-args
Summary:	Gambas3 component package for args
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-args
%{summary}

%files gb-args
%doc README  ChangeLog
%{_libdir}/%{name}/gb.args.*
%{_datadir}/%{name}/info/gb.args.*

#---------------------------------------------------------------------------
%package gb-httpd
Summary:	Gambas3 component package for httpd
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-httpd
%{summary}.

%files gb-httpd
%doc README  ChangeLog
%{_libdir}/%{name}/gb.httpd.*
%{_datadir}/%{name}/info/gb.httpd.*


#---------------------------------------------------------------------------

%package gb-map
Summary:	Gambas3 component package for map
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-map
%{summary}.

%files gb-map
%doc README  ChangeLog
%{_libdir}/%{name}/gb.map.component
%{_libdir}/%{name}/gb.map.gambas
%{_datadir}/%{name}/info/gb.map.*
%{_datadir}/%{name}/control/gb.map/

#---------------------------------------------------------------------------
%package gb-memcached
Summary:	Gambas3 component package for memcached
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-memcached
%{summary}.

%files gb-memcached
%doc README  ChangeLog
%{_libdir}/%{name}/gb.memcached.*
%{_datadir}/%{name}/info/gb.memcached.*

#---------------------------------------------------------------------------
%package gb-clipper
Group:   Development/Other
Requires:      %{name}-runtime = %{EVRD}

%description gb-clipper
New component based on the Clipper library

%files gb-clipper
%doc README  ChangeLog
%{_libdir}/%{name}/gb.clipper.*
%{_datadir}/%{name}/info/gb.clipper.*

#---------------------------------------------------------------------------
%package gb-gmp
Summary:       Gambas3 component package for gmp
Group:   Development/Other
Requires:      %{name}-runtime = %{EVRD}

%description gb-gmp
New component based on the Gnu Multiple Precision Arithmetic 
Library that implements big integers and big rational numbers.

%files gb-gmp
%doc README  ChangeLog
%{_libdir}/%{name}/gb.gmp.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.gmp.*
#---------------------------------------------------------------------------
%package gb-logging
Summary:       Gambas3 component package for logging
Group:   Development/Other
Requires:      %{name}-runtime = %{EVRD}

%description gb-logging
%{summary}.

%files gb-logging
%doc README  ChangeLog
%{_libdir}/%{name}/gb.logging.*
%{_datadir}/%{name}/info/gb.logging.*

#---------------------------------------------------------------------------
%package gb-openal
Summary:       Gambas3 component package for openal
Group:   Development/Other
Requires:      %{name}-runtime = %{EVRD}

%description gb-openal
Component based on the OpenAL 3D audio library.

%files gb-openal
%doc README  ChangeLog
%{_libdir}/%{name}/gb.openal.*
%{_datadir}/%{name}/info/gb.openal.*

#---------------------------------------------------------------------------
%package gb-opengl-sge
Summary:       Gambas3 component package for opengl-sge
Group:   Development/Other
Requires:      %{name}-runtime = %{EVRD}
Requires:      %{name}-gb-opengl = %{EVRD}

%description gb-opengl-sge
Component that implements a simple OpenGL game engine based on the MD2 format.

%files gb-opengl-sge
%doc README  ChangeLog
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gb.opengl.sge.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.opengl.sge.*

#---------------------------------------------------------------------------
%package gb-openssl
Summary:       Gambas3 component package for openssl
Group:   Development/Other
Requires:      %{name}-runtime = %{EVRD}

%description gb-openssl
Component to wrap cryptographic functions of 
libcrypto from the OpenSSL project.

%files gb-openssl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.openssl.*
%{_datadir}/%{name}/info/gb.openssl.*

#---------------------------------------------------------------------------
%package gb-inotify
Summary:       Gambas3 component package for inotify
Group:   Development/Other
Requires:      %{name}-runtime = %{EVRD}

%description gb-inotify
Gambas3 component package for inotify.


%files gb-inotify
%doc README  ChangeLog
%{_libdir}/%{name}/gb.inotify.component
%{_libdir}/%{name}/gb.inotify.so*
%{_datadir}/%{name}/info/gb.inotify.info
%{_datadir}/%{name}/info/gb.inotify.list

#---------------------------------------------------------------------------
%package gb-markdown
Summary:	Gambas3 component package for markdown
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-markdown
Gambas3 component package for markdown.


%files gb-markdown
%doc README  ChangeLog
%{_libdir}/%{name}/gb.markdown.component
%{_libdir}/%{name}/gb.markdown.gambas
%{_datadir}/%{name}/info/gb.markdown.info
%{_datadir}/%{name}/info/gb.markdown.list

#-----------------------------------------------------------------------------
%package gb-gtk3
Summary:	Gambas3 component package for gtk3
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-gtk3
Gambas3 component package for gtk3.


%files gb-gtk3
%doc README  ChangeLog
%{_libdir}/%{name}/gb.gtk3.component
%{_libdir}/%{name}/gb.gtk3.so*
%{_datadir}/%{name}/info/gb.gtk3.info
%{_datadir}/%{name}/info/gb.gtk3.list
#-----------------------------------------------------------------------------
# since 3.7.0
%package gb-report2
Summary:	Gambas3 component package for reporting
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-report2
gb.report2 is a new and better implementation of the reporting component.

%files gb-report2
%doc README  ChangeLog
%{_libdir}/%{name}/gb.report2.component
%{_libdir}/%{name}/gb.report2.gambas
%{_datadir}/%{name}/control/gb.report2/*.png
%{_datadir}/%{name}/info/gb.report2.info
%{_datadir}/%{name}/info/gb.report2.list

#-----------------------------------------------------------------------------
%package gb-scanner
Summary:	Gambas3 component package for SANE
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-scanner
Is a new component based on SANE to help dealing with scanners.

%files gb-scanner
%doc README  ChangeLog
%{_libdir}/%{name}/gb.scanner.component
%{_libdir}/%{name}/gb.scanner.gambas
%{_datadir}/%{name}/info/gb.scanner.info
%{_datadir}/%{name}/info/gb.scanner.list

#-----------------------------------------------------------------------------
%package gb-util
Summary:	Gambas3 component package for utility functions
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}

%description gb-util
Is a new component written in Gambas that 
provides utility functions to the interpreter.

%files gb-util
%doc README  ChangeLog
%{_libdir}/%{name}/gb.util.component
%{_libdir}/%{name}/gb.util.gambas
%{_datadir}/%{name}/info/gb.util.info
%{_datadir}/%{name}/info/gb.util.list

#-----------------------------------------------------------------------------
%package gb-util-web
Summary:	Gambas3 component package for web applications
Group:		Development/Other
Requires:	%{name}-runtime = %{EVRD}


%description gb-util-web
Is a new component written in Gambas that 
provides utility functions to web applications.

%files gb-util-web
%doc README  ChangeLog
%{_libdir}/%{name}/gb.util.web.component
%{_libdir}/%{name}/gb.util.web.gambas
%{_datadir}/%{name}/control/gb.util.web/ccontainer.png
%{_datadir}/%{name}/control/gb.util.web/ccontrol.png
%{_datadir}/%{name}/info/gb.util.web.info
%{_datadir}/%{name}/info/gb.util.web.list

#-----------------------------------------------------------------------------


































