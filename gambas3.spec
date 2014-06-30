Name:		gambas3
Summary:	Complete IDE based on a BASIC interpreter with object extensions
Version:	3.5.4
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
BuildRequires:  pkgconfig(SDL_image)
# no pkgconfig for gmime for portability
BuildRequires:  gmime-devel
BuildRequires:  pkgconfig(libv4lconvert)
#
%if %{mdvver} >= 201210
BuildRequires:  llvm-devel
%if %{mdvver} == 201200
BuildRequires:	llvm
%endif
%endif
# No jit modules in 2014.1, won't build against llvm3.4.2
# we don't have gst-1 in lts
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
%if %{mdvver} == 201410
# add math's functions to the linker
export LDFLAGS="$LDFLAGS -lm"
# export pow, ceil a.s.o math's functions
# in both compilers , gb.image component is in C
export CXXFLAGS="%{optflags} -lm"
export CFLAGS="%{optflags} -lm"
%endif

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
# attr fix
chmod -x %{buildroot}%{_datadir}/gambas3/gb.sdl/LICENSE

desktop-file-install %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
chmod -x %{buildroot}%{_datadir}/applications/%{name}.desktop 

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

#-----------------------------------------------------------------------------

%package script
Summary: The Gambas scripter package
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}


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
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-devel = %{version}
Requires: %{name}-gb-db = %{version}
Requires: %{name}-gb-db-form = %{version}
Requires: %{name}-gb-desktop = %{version}
Requires: %{name}-gb-eval-highlight = %{version}
Requires: %{name}-gb-form = %{version}
Requires: %{name}-gb-form-dialog = %{version}
Requires: %{name}-gb-form-mdi = %{version}
Requires: %{name}-gb-form-stock = %{version}
Requires: %{name}-gb-gui = %{version}
Requires: %{name}-gb-image = %{version}
Requires: %{name}-gb-image-effect = %{version}
Requires: %{name}-gb-qt4 = %{version}
Requires: %{name}-gb-qt4-ext = %{version}
Requires: %{name}-gb-qt4-webkit = %{version}
Requires: %{name}-gb-settings = %{version}
Requires: %{name}-examples = %{version}
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
%dir %{_datadir}/%{name}/examples/

#-----------------------------------------------------------------------------

%package examples
Summary: The Gambas examples
Group: Development/Other
BuildArch: noarch
Suggests: %{name}-ide = %{version}


%description examples
This package includes all the example projects provided with Gambas.

%files examples
%doc README  ChangeLog
%dir %{_datadir}/%{name}/examples/Automation/
%dir %{_datadir}/%{name}/examples/Basic/
%dir %{_datadir}/%{name}/examples/Control/
%dir %{_datadir}/%{name}/examples/Database/
%dir %{_datadir}/%{name}/examples/Drawing/
%dir %{_datadir}/%{name}/examples/Games/
%dir %{_datadir}/%{name}/examples/Image/
%dir %{_datadir}/%{name}/examples/Misc/
%dir %{_datadir}/%{name}/examples/Multimedia/
%dir %{_datadir}/%{name}/examples/Networking/
%dir %{_datadir}/%{name}/examples/OpenGL/
%dir %{_datadir}/%{name}/examples/Printing/
%dir %{_datadir}/%{name}/examples/Automation/DBusExplorer/
%{_datadir}/%{name}/examples/Automation/DBusExplorer/dbus*.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/DBusExplorer.gambas
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.directory
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.gambas/
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.hidden
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.icon.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/method.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.project
%{_datadir}/%{name}/examples/Automation/DBusExplorer/property.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.settings
%{_datadir}/%{name}/examples/Automation/DBusExplorer/signal.png
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.src/
%{_datadir}/%{name}/examples/Automation/DBusExplorer/.startup

%dir %{_datadir}/%{name}/examples/Basic/Blights/
%dir %{_datadir}/%{name}/examples/Basic/Blights/.lang/
%{_datadir}/%{name}/examples/Basic/Blights/.directory
%{_datadir}/%{name}/examples/Basic/Blights/.gambas/
%{_datadir}/%{name}/examples/Basic/Blights/.hidden
%{_datadir}/%{name}/examples/Basic/Blights/.icon*
%{_datadir}/%{name}/examples/Basic/Blights/.project
%{_datadir}/%{name}/examples/Basic/Blights/.src/
%{_datadir}/%{name}/examples/Basic/Blights/.startup
%{_datadir}/%{name}/examples/Basic/Blights/Blights.gambas
%{_datadir}/%{name}/examples/Basic/Blights/ampoule.png
%{_datadir}/%{name}/examples/Basic/Blights/bloff.xpm
%{_datadir}/%{name}/examples/Basic/Blights/blon.xpm

%dir %{_datadir}/%{name}/examples/Basic/Collection/
%dir %{_datadir}/%{name}/examples/Basic/Collection/.lang/
%{_datadir}/%{name}/examples/Basic/Collection/.directory
%{_datadir}/%{name}/examples/Basic/Collection/.gambas/
%{_datadir}/%{name}/examples/Basic/Collection/.hidden
%{_datadir}/%{name}/examples/Basic/Collection/.icon*
%{_datadir}/%{name}/examples/Basic/Collection/.project
%{_datadir}/%{name}/examples/Basic/Collection/.startup
%{_datadir}/%{name}/examples/Basic/Collection/.src/
%{_datadir}/%{name}/examples/Basic/Collection/Collection.gambas
%{_datadir}/%{name}/examples/Basic/Collection/collection.png

%dir %{_datadir}/%{name}/examples/Basic/DragNDrop/
%{_datadir}/%{name}/examples/Basic/DragNDrop/.directory
%{_datadir}/%{name}/examples/Basic/DragNDrop/.gambas/
%{_datadir}/%{name}/examples/Basic/DragNDrop/.hidden
%{_datadir}/%{name}/examples/Basic/DragNDrop/.icon*
%{_datadir}/%{name}/examples/Basic/DragNDrop/.project
%{_datadir}/%{name}/examples/Basic/DragNDrop/.startup
%{_datadir}/%{name}/examples/Basic/DragNDrop/DragNDrop.gambas
%{_datadir}/%{name}/examples/Basic/DragNDrop/.src/
%{_datadir}/%{name}/examples/Basic/DragNDrop/drop.png

%dir %{_datadir}/%{name}/examples/Basic/Object/
%dir %{_datadir}/%{name}/examples/Basic/Object/.lang/
%{_datadir}/%{name}/examples/Basic/Object/.directory
%{_datadir}/%{name}/examples/Basic/Object/.gambas/
%{_datadir}/%{name}/examples/Basic/Object/.hidden
%{_datadir}/%{name}/examples/Basic/Object/.icon*
%{_datadir}/%{name}/examples/Basic/Object/.project
%{_datadir}/%{name}/examples/Basic/Object/.startup
%{_datadir}/%{name}/examples/Basic/Object/.src/
%{_datadir}/%{name}/examples/Basic/Object/Object.gambas
%{_datadir}/%{name}/examples/Basic/Object/object.png

%dir %{_datadir}/%{name}/examples/Basic/Timer/
%dir %{_datadir}/%{name}/examples/Basic/Timer/.lang/
%{_datadir}/%{name}/examples/Basic/Timer/.directory
%{_datadir}/%{name}/examples/Basic/Timer/.gambas/
%{_datadir}/%{name}/examples/Basic/Timer/.hidden
%{_datadir}/%{name}/examples/Basic/Timer/.icon*
%{_datadir}/%{name}/examples/Basic/Timer/.project
%{_datadir}/%{name}/examples/Basic/Timer/.startup
%{_datadir}/%{name}/examples/Basic/Timer/.src/
%{_datadir}/%{name}/examples/Basic/Timer/Timer.gambas
%{_datadir}/%{name}/examples/Basic/Timer/timer.png

%dir %{_datadir}/%{name}/examples/Control/ArrayOfControls/
%dir %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.directory
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.gambas/
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.hidden
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.icon*
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.project
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.startup
%{_datadir}/%{name}/examples/Control/ArrayOfControls/.src/
%{_datadir}/%{name}/examples/Control/ArrayOfControls/green1.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/green.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/phone.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/red1.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/red.png
%{_datadir}/%{name}/examples/Control/ArrayOfControls/ArrayOfControls.gambas

%dir %{_datadir}/%{name}/examples/Control/Embedder/
%dir %{_datadir}/%{name}/examples/Control/Embedder/.lang/
%{_datadir}/%{name}/examples/Control/Embedder/.directory
%{_datadir}/%{name}/examples/Control/Embedder/.gambas/
%{_datadir}/%{name}/examples/Control/Embedder/.hidden
%{_datadir}/%{name}/examples/Control/Embedder/.icon*
%{_datadir}/%{name}/examples/Control/Embedder/.project
%{_datadir}/%{name}/examples/Control/Embedder/.settings
%{_datadir}/%{name}/examples/Control/Embedder/.startup
%{_datadir}/%{name}/examples/Control/Embedder/.src/
%{_datadir}/%{name}/examples/Control/Embedder/Embedder.gambas
%{_datadir}/%{name}/examples/Control/Embedder/embedder.png

%dir %{_datadir}/%{name}/examples/Control/HighlightEditor/
%dir %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/
%{_datadir}/%{name}/examples/Control/HighlightEditor/.directory
%{_datadir}/%{name}/examples/Control/HighlightEditor/.gambas/
%{_datadir}/%{name}/examples/Control/HighlightEditor/.hidden
%{_datadir}/%{name}/examples/Control/HighlightEditor/.icon*
%{_datadir}/%{name}/examples/Control/HighlightEditor/.project
%{_datadir}/%{name}/examples/Control/HighlightEditor/.startup
%{_datadir}/%{name}/examples/Control/HighlightEditor/.src/
%{_datadir}/%{name}/examples/Control/HighlightEditor/HighlightEditor.gambas
%{_datadir}/%{name}/examples/Control/HighlightEditor/download.html
%{_datadir}/%{name}/examples/Control/HighlightEditor/editor.png

%dir %{_datadir}/%{name}/examples/Control/MapView/
%{_datadir}/%{name}/examples/Control/MapView/.directory
%{_datadir}/%{name}/examples/Control/MapView/.gambas/
%{_datadir}/%{name}/examples/Control/MapView/.hidden/
%{_datadir}/%{name}/examples/Control/MapView/.icon*
%{_datadir}/%{name}/examples/Control/MapView/.project
%{_datadir}/%{name}/examples/Control/MapView/.src/
%{_datadir}/%{name}/examples/Control/MapView/.startup
%{_datadir}/%{name}/examples/Control/MapView/MapView.gambas

%dir %{_datadir}/%{name}/examples/Control/TextEdit/
%dir %{_datadir}/%{name}/examples/Control/TextEdit/.lang/
%{_datadir}/%{name}/examples/Control/TextEdit/.directory
%{_datadir}/%{name}/examples/Control/TextEdit/.gambas/
%{_datadir}/%{name}/examples/Control/TextEdit/.hidden
%{_datadir}/%{name}/examples/Control/TextEdit/.icon*
%{_datadir}/%{name}/examples/Control/TextEdit/.project
%{_datadir}/%{name}/examples/Control/TextEdit/.startup
%{_datadir}/%{name}/examples/Control/TextEdit/.src/
%{_datadir}/%{name}/examples/Control/TextEdit/TextEdit.gambas
%{_datadir}/%{name}/examples/Control/TextEdit/edit.png
%{_datadir}/%{name}/examples/Control/TextEdit/text.html

%dir %{_datadir}/%{name}/examples/Control/TreeView/
%dir %{_datadir}/%{name}/examples/Control/TreeView/.lang/
%{_datadir}/%{name}/examples/Control/TreeView/.directory
%{_datadir}/%{name}/examples/Control/TreeView/.gambas/
%{_datadir}/%{name}/examples/Control/TreeView/.hidden
%{_datadir}/%{name}/examples/Control/TreeView/.icon*
%{_datadir}/%{name}/examples/Control/TreeView/.project
%{_datadir}/%{name}/examples/Control/TreeView/.startup
%{_datadir}/%{name}/examples/Control/TreeView/.src/
%{_datadir}/%{name}/examples/Control/TreeView/Female.png
%{_datadir}/%{name}/examples/Control/TreeView/Male.png
%{_datadir}/%{name}/examples/Control/TreeView/treeview.png
%{_datadir}/%{name}/examples/Control/TreeView/TreeView.gambas

%dir %{_datadir}/%{name}/examples/Control/Wizard/
%dir %{_datadir}/%{name}/examples/Control/Wizard/.lang/
%{_datadir}/%{name}/examples/Control/Wizard/.directory
%{_datadir}/%{name}/examples/Control/Wizard/.gambas/
%{_datadir}/%{name}/examples/Control/Wizard/.hidden
%{_datadir}/%{name}/examples/Control/Wizard/.icon*
%{_datadir}/%{name}/examples/Control/Wizard/.project
%{_datadir}/%{name}/examples/Control/Wizard/.startup
%{_datadir}/%{name}/examples/Control/Wizard/.src/
%{_datadir}/%{name}/examples/Control/Wizard/Wizard.gambas
%{_datadir}/%{name}/examples/Control/Wizard/wizard.png

%dir %{_datadir}/%{name}/examples/Database/Database/
%dir %{_datadir}/%{name}/examples/Database/Database/.lang/
%{_datadir}/%{name}/examples/Database/Database/.component
%{_datadir}/%{name}/examples/Database/Database/.directory
%{_datadir}/%{name}/examples/Database/Database/.gambas/
%{_datadir}/%{name}/examples/Database/Database/.hidden
%{_datadir}/%{name}/examples/Database/Database/.icon*
%{_datadir}/%{name}/examples/Database/Database/.project
%{_datadir}/%{name}/examples/Database/Database/.startup
%{_datadir}/%{name}/examples/Database/Database/.src/
%{_datadir}/%{name}/examples/Database/Database/Database.gambas
%{_datadir}/%{name}/examples/Database/Database/database.png

%dir %{_datadir}/%{name}/examples/Database/MySQLExample/
%dir %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/
%{_datadir}/%{name}/examples/Database/MySQLExample/.action
%{_datadir}/%{name}/examples/Database/MySQLExample/.directory
%{_datadir}/%{name}/examples/Database/MySQLExample/.gambas/
%{_datadir}/%{name}/examples/Database/MySQLExample/.hidden
%{_datadir}/%{name}/examples/Database/MySQLExample/.icon*
%{_datadir}/%{name}/examples/Database/MySQLExample/icons/
%{_datadir}/%{name}/examples/Database/MySQLExample/MySQLExample.gambas
%{_datadir}/%{name}/examples/Database/MySQLExample/.project
%{_datadir}/%{name}/examples/Database/MySQLExample/.src/
%{_datadir}/%{name}/examples/Database/MySQLExample/.startup

%dir %{_datadir}/%{name}/examples/Database/PictureDatabase/
%dir %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/
%{_datadir}/%{name}/examples/Database/PictureDatabase/.directory
%{_datadir}/%{name}/examples/Database/PictureDatabase/.gambas/
%{_datadir}/%{name}/examples/Database/PictureDatabase/.hidden
%{_datadir}/%{name}/examples/Database/PictureDatabase/.icon*
%{_datadir}/%{name}/examples/Database/PictureDatabase/.project
%{_datadir}/%{name}/examples/Database/PictureDatabase/.startup
%{_datadir}/%{name}/examples/Database/PictureDatabase/.src/
%{_datadir}/%{name}/examples/Database/PictureDatabase/Images/
%{_datadir}/%{name}/examples/Database/PictureDatabase/PictureDatabase.gambas

%dir %{_datadir}/%{name}/examples/Drawing/AnalogWatch/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.directory
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.gambas/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.hidden
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.icon*
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.project
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.startup
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/AnalogWatch.gambas
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/.src/
%{_datadir}/%{name}/examples/Drawing/AnalogWatch/timer.png

%dir %{_datadir}/%{name}/examples/Drawing/Barcode/
%dir %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/
%{_datadir}/%{name}/examples/Drawing/Barcode/.directory
%{_datadir}/%{name}/examples/Drawing/Barcode/.gambas/
%{_datadir}/%{name}/examples/Drawing/Barcode/.hidden
%{_datadir}/%{name}/examples/Drawing/Barcode/.icon*
%{_datadir}/%{name}/examples/Drawing/Barcode/.project
%{_datadir}/%{name}/examples/Drawing/Barcode/.settings
%{_datadir}/%{name}/examples/Drawing/Barcode/.startup
%{_datadir}/%{name}/examples/Drawing/Barcode/.src/
%{_datadir}/%{name}/examples/Drawing/Barcode/Barcode.gambas
%{_datadir}/%{name}/examples/Drawing/Barcode/barcode.png

%dir %{_datadir}/%{name}/examples/Drawing/Chart/
%dir %{_datadir}/%{name}/examples/Drawing/Chart/.lang/
%{_datadir}/%{name}/examples/Drawing/Chart/.directory
%{_datadir}/%{name}/examples/Drawing/Chart/.gambas/
%{_datadir}/%{name}/examples/Drawing/Chart/.hidden
%{_datadir}/%{name}/examples/Drawing/Chart/.icon*
%{_datadir}/%{name}/examples/Drawing/Chart/.project
%{_datadir}/%{name}/examples/Drawing/Chart/.src/
%{_datadir}/%{name}/examples/Drawing/Chart/.startup
%{_datadir}/%{name}/examples/Drawing/Chart/Chart.gambas
%{_datadir}/%{name}/examples/Drawing/Chart/graph.png

%dir %{_datadir}/%{name}/examples/Drawing/Clock/
%dir %{_datadir}/%{name}/examples/Drawing/Clock/.lang/
%{_datadir}/%{name}/examples/Drawing/Clock/.directory
%{_datadir}/%{name}/examples/Drawing/Clock/.gambas/
%{_datadir}/%{name}/examples/Drawing/Clock/.hidden
%{_datadir}/%{name}/examples/Drawing/Clock/.icon*
%{_datadir}/%{name}/examples/Drawing/Clock/.project
%{_datadir}/%{name}/examples/Drawing/Clock/.startup
%{_datadir}/%{name}/examples/Drawing/Clock/.src/
%{_datadir}/%{name}/examples/Drawing/Clock/Clock.gambas
%{_datadir}/%{name}/examples/Drawing/Clock/img/

%dir %{_datadir}/%{name}/examples/Drawing/Fractal/
%dir %{_datadir}/%{name}/examples/Drawing/Fractal/.lang
%{_datadir}/%{name}/examples/Drawing/Fractal/.directory
%{_datadir}/%{name}/examples/Drawing/Fractal/.gambas/
%{_datadir}/%{name}/examples/Drawing/Fractal/.icon*
%{_datadir}/%{name}/examples/Drawing/Fractal/.project
%{_datadir}/%{name}/examples/Drawing/Fractal/.startup
%{_datadir}/%{name}/examples/Drawing/Fractal/.src/
%{_datadir}/%{name}/examples/Drawing/Fractal/Fractal.gambas
%{_datadir}/%{name}/examples/Drawing/Fractal/icon.png
%{_datadir}/%{name}/examples/Drawing/Fractal/rose.jpg

%dir %{_datadir}/%{name}/examples/Drawing/Gravity/
%dir %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/
%{_datadir}/%{name}/examples/Drawing/Gravity/.directory
%{_datadir}/%{name}/examples/Drawing/Gravity/.gambas/
%{_datadir}/%{name}/examples/Drawing/Gravity/.hidden
%{_datadir}/%{name}/examples/Drawing/Gravity/.icon*
%{_datadir}/%{name}/examples/Drawing/Gravity/.project
%{_datadir}/%{name}/examples/Drawing/Gravity/.startup
%{_datadir}/%{name}/examples/Drawing/Gravity/.src/
%{_datadir}/%{name}/examples/Drawing/Gravity/Gravity.gambas
%{_datadir}/%{name}/examples/Drawing/Gravity/gravity.png

%dir %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/
%dir %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.directory
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.gambas/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.hidden
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.icon*
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.project
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.startup
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.src/
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/OnScreenDisplay.gambas
%{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/icon.png

%dir %{_datadir}/%{name}/examples/Drawing/Painting/
%dir %{_datadir}/%{name}/examples/Drawing/Painting/.lang
%{_datadir}/%{name}/examples/Drawing/Painting/.directory
%{_datadir}/%{name}/examples/Drawing/Painting/.gambas/
%{_datadir}/%{name}/examples/Drawing/Painting/.hidden
%{_datadir}/%{name}/examples/Drawing/Painting/.icon*
%{_datadir}/%{name}/examples/Drawing/Painting/.project
%{_datadir}/%{name}/examples/Drawing/Painting/.startup
%{_datadir}/%{name}/examples/Drawing/Painting/.src/
%{_datadir}/%{name}/examples/Drawing/Painting/Example*
%{_datadir}/%{name}/examples/Drawing/Painting/clovis.jpg
%{_datadir}/%{name}/examples/Drawing/Painting/gambas.*svg
%{_datadir}/%{name}/examples/Drawing/Painting/icon.png
%{_datadir}/%{name}/examples/Drawing/Painting/image.jpg
%{_datadir}/%{name}/examples/Drawing/Painting/Painting.gambas

%dir %{_datadir}/%{name}/examples/Drawing/GSLSpline/
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.directory
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.gambas/
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.icon*
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.project
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.src/
%{_datadir}/%{name}/examples/Drawing/GSLSpline/.startup
%{_datadir}/%{name}/examples/Drawing/GSLSpline/GSLSpline.gambas
%{_datadir}/%{name}/examples/Drawing/GSLSpline/spline.png

%dir %{_datadir}/%{name}/examples/Drawing/Tablet/
%{_datadir}/%{name}/examples/Drawing/Tablet/.directory
%{_datadir}/%{name}/examples/Drawing/Tablet/.gambas/
%{_datadir}/%{name}/examples/Drawing/Tablet/.icon*
%{_datadir}/%{name}/examples/Drawing/Tablet/.project
%{_datadir}/%{name}/examples/Drawing/Tablet/.src/
%{_datadir}/%{name}/examples/Drawing/Tablet/.startup
%{_datadir}/%{name}/examples/Drawing/Tablet/Icon.png
%{_datadir}/%{name}/examples/Drawing/Tablet/Tablet.gambas

%dir %{_datadir}/%{name}/examples/Games/BeastScroll/
%{_datadir}/%{name}/examples/Games/BeastScroll/.dir_icon.png
%{_datadir}/%{name}/examples/Games/BeastScroll/.directory
%{_datadir}/%{name}/examples/Games/BeastScroll/.gambas/
%{_datadir}/%{name}/examples/Games/BeastScroll/.hidden
%{_datadir}/%{name}/examples/Games/BeastScroll/.icon*
%{_datadir}/%{name}/examples/Games/BeastScroll/.project
%{_datadir}/%{name}/examples/Games/BeastScroll/.startup
%{_datadir}/%{name}/examples/Games/BeastScroll/.src/
%{_datadir}/%{name}/examples/Games/BeastScroll/BeastScroll.gambas
%{_datadir}/%{name}/examples/Games/BeastScroll/b-title.mod
%{_datadir}/%{name}/examples/Games/BeastScroll/bgd*.png
%{_datadir}/%{name}/examples/Games/BeastScroll/fireworks.png
%{_datadir}/%{name}/examples/Games/BeastScroll/logo.png
%{_datadir}/%{name}/examples/Games/BeastScroll/scrolltext.png
%{_datadir}/%{name}/examples/Games/BeastScroll/sprite*.png

%dir %{_datadir}/%{name}/examples/Games/Concent/
%dir %{_datadir}/%{name}/examples/Games/Concent/.lang/
%{_datadir}/%{name}/examples/Games/Concent/.directory
%{_datadir}/%{name}/examples/Games/Concent/.gambas/
%{_datadir}/%{name}/examples/Games/Concent/.hidden
%{_datadir}/%{name}/examples/Games/Concent/.icon*
%{_datadir}/%{name}/examples/Games/Concent/.project
%{_datadir}/%{name}/examples/Games/Concent/.settings
%{_datadir}/%{name}/examples/Games/Concent/.startup
%{_datadir}/%{name}/examples/Games/Concent/*.wav
%{_datadir}/%{name}/examples/Games/Concent/CHANGELOG
%{_datadir}/%{name}/examples/Games/Concent/Concent.gambas
%{_datadir}/%{name}/examples/Games/Concent/.src/
%{_datadir}/%{name}/examples/Games/Concent/imagenes/

%dir %{_datadir}/%{name}/examples/Games/DeepSpace/
%dir %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/
%{_datadir}/%{name}/examples/Games/DeepSpace/.directory
%{_datadir}/%{name}/examples/Games/DeepSpace/.gambas/
%{_datadir}/%{name}/examples/Games/DeepSpace/.hidden
%{_datadir}/%{name}/examples/Games/DeepSpace/.icon*
%{_datadir}/%{name}/examples/Games/DeepSpace/.project
%{_datadir}/%{name}/examples/Games/DeepSpace/.startup
%{_datadir}/%{name}/examples/Games/DeepSpace/.src/
%{_datadir}/%{name}/examples/Games/DeepSpace/DeepSpace.gambas
%{_datadir}/%{name}/examples/Games/DeepSpace/doc/
%{_datadir}/%{name}/examples/Games/DeepSpace/images/
%{_datadir}/%{name}/examples/Games/DeepSpace/object.data/

%dir %{_datadir}/%{name}/examples/Games/GameOfLife/
%dir %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/
%{_datadir}/%{name}/examples/Games/GameOfLife/.debug
%{_datadir}/%{name}/examples/Games/GameOfLife/.directory
%{_datadir}/%{name}/examples/Games/GameOfLife/.gambas/
%{_datadir}/%{name}/examples/Games/GameOfLife/.hidden
%{_datadir}/%{name}/examples/Games/GameOfLife/.icon*
%{_datadir}/%{name}/examples/Games/GameOfLife/.project
%{_datadir}/%{name}/examples/Games/GameOfLife/.settings
%{_datadir}/%{name}/examples/Games/GameOfLife/.startup
%{_datadir}/%{name}/examples/Games/GameOfLife/.src/
%{_datadir}/%{name}/examples/Games/GameOfLife/GameOfLife.gambas
%{_datadir}/%{name}/examples/Games/GameOfLife/glob2*.png

%dir %{_datadir}/%{name}/examples/Games/GNUBoxWorld/
%dir %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.directory
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.gambas/
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.hidden
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.icon*
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/License
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.project
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.startup
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/.src/
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/GNUBoxWorld.gambas
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/abajo.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/arriba.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/derecha.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/destino.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/ganador.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/izquierda.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/logo.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/movibleendestino.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/movible.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/obstaculo*.png
%{_datadir}/%{name}/examples/Games/GNUBoxWorld/piso.png
%dir %{_datadir}/%{name}/examples/Games/Invaders
%{_datadir}/%{name}/examples/Games/Invaders/invaders.png
%{_datadir}/%{name}/examples/Games/Invaders/.directory
%{_datadir}/%{name}/examples/Games/Invaders/.gambas/
%{_datadir}/%{name}/examples/Games/Invaders/.icon*
%{_datadir}/%{name}/examples/Games/Invaders/.project
%{_datadir}/%{name}/examples/Games/Invaders/.src/
%{_datadir}/%{name}/examples/Games/Invaders/.startup
%{_datadir}/%{name}/examples/Games/Invaders/Invaders.*

%dir %{_datadir}/%{name}/examples/Games/MineSweeper/
%dir %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/
%{_datadir}/%{name}/examples/Games/MineSweeper/.directory
%{_datadir}/%{name}/examples/Games/MineSweeper/.gambas/
%{_datadir}/%{name}/examples/Games/MineSweeper/.icon*
%{_datadir}/%{name}/examples/Games/MineSweeper/.project
%{_datadir}/%{name}/examples/Games/MineSweeper/.src/
%{_datadir}/%{name}/examples/Games/MineSweeper/.startup
%{_datadir}/%{name}/examples/Games/MineSweeper/MineSweeper.gambas
%{_datadir}/%{name}/examples/Games/MineSweeper/image/

%dir %{_datadir}/%{name}/examples/Games/Pong/
%{_datadir}/%{name}/examples/Games/Pong/.directory
%{_datadir}/%{name}/examples/Games/Pong/.gambas/
%{_datadir}/%{name}/examples/Games/Pong/.icon*
%{_datadir}/%{name}/examples/Games/Pong/.project
%{_datadir}/%{name}/examples/Games/Pong/.src/
%{_datadir}/%{name}/examples/Games/Pong/.startup
%{_datadir}/%{name}/examples/Games/Pong/Pong.gambas
%{_datadir}/%{name}/examples/Games/Pong/SPEED
%{_datadir}/%{name}/examples/Games/Pong/pong.png

%dir %{_datadir}/%{name}/examples/Games/Puzzle1To8
%dir %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.directory
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.gambas/
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.hidden
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.icon*
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.project
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.startup
%{_datadir}/%{name}/examples/Games/Puzzle1To8/.src/
%{_datadir}/%{name}/examples/Games/Puzzle1To8/ejemplo1.png
%{_datadir}/%{name}/examples/Games/Puzzle1To8/ejemplo2.png
%{_datadir}/%{name}/examples/Games/Puzzle1To8/logo.png
%{_datadir}/%{name}/examples/Games/Puzzle1To8/Licence
%{_datadir}/%{name}/examples/Games/Puzzle1To8/Puzzle*.gambas

%dir %{_datadir}/%{name}/examples/Games/RobotFindsKitten/
%dir %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.directory
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.gambas/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.hidden
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.icon*
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.project
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.startup
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/.src/
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/COPYING
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/RobotFindsKitten.gambas
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/heart.png
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/nkis.txt
%{_datadir}/%{name}/examples/Games/RobotFindsKitten/readme.txt

%dir %{_datadir}/%{name}/examples/Games/Snake/
%dir %{_datadir}/%{name}/examples/Games/Snake/.lang/
%{_datadir}/%{name}/examples/Games/Snake/.directory
%{_datadir}/%{name}/examples/Games/Snake/.gambas/
%{_datadir}/%{name}/examples/Games/Snake/.hidden
%{_datadir}/%{name}/examples/Games/Snake/.icon*
%{_datadir}/%{name}/examples/Games/Snake/.project
%{_datadir}/%{name}/examples/Games/Snake/.startup
%{_datadir}/%{name}/examples/Games/Snake/.src/
%{_datadir}/%{name}/examples/Games/Snake/Snake.gambas
%{_datadir}/%{name}/examples/Games/Snake/apple.png
%{_datadir}/%{name}/examples/Games/Snake/body.png
%{_datadir}/%{name}/examples/Games/Snake/*.wav
%{_datadir}/%{name}/examples/Games/Snake/head.png

%dir %{_datadir}/%{name}/examples/Games/Solitaire/
%dir %{_datadir}/%{name}/examples/Games/Solitaire/.lang/
%{_datadir}/%{name}/examples/Games/Solitaire/.directory
%{_datadir}/%{name}/examples/Games/Solitaire/.gambas/
%{_datadir}/%{name}/examples/Games/Solitaire/.hidden
%{_datadir}/%{name}/examples/Games/Solitaire/.icon*
%{_datadir}/%{name}/examples/Games/Solitaire/.project
%{_datadir}/%{name}/examples/Games/Solitaire/.startup
%{_datadir}/%{name}/examples/Games/Solitaire/.src/
%{_datadir}/%{name}/examples/Games/Solitaire/Solitaire.gambas
%{_datadir}/%{name}/examples/Games/Solitaire/ball.png
%{_datadir}/%{name}/examples/Games/Solitaire/new.png
%{_datadir}/%{name}/examples/Games/Solitaire/quit.png
%{_datadir}/%{name}/examples/Games/Solitaire/redo.png
%{_datadir}/%{name}/examples/Games/Solitaire/undo.png

%dir %{_datadir}/%{name}/examples/Games/StarField/
%{_datadir}/%{name}/examples/Games/StarField/.directory
%{_datadir}/%{name}/examples/Games/StarField/.gambas/
%{_datadir}/%{name}/examples/Games/StarField/.icon*
%{_datadir}/%{name}/examples/Games/StarField/.project
%{_datadir}/%{name}/examples/Games/StarField/.src/
%{_datadir}/%{name}/examples/Games/StarField/.startup
%{_datadir}/%{name}/examples/Games/StarField/StarField.gambas
%{_datadir}/%{name}/examples/Games/StarField/enterprise.png
%{_datadir}/%{name}/examples/Games/StarField/logo.png

%dir %{_datadir}/%{name}/examples/Image/ImageViewer/
%dir %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/
%{_datadir}/%{name}/examples/Image/ImageViewer/.directory
%{_datadir}/%{name}/examples/Image/ImageViewer/.gambas/
%{_datadir}/%{name}/examples/Image/ImageViewer/.hidden
%{_datadir}/%{name}/examples/Image/ImageViewer/.icon*
%{_datadir}/%{name}/examples/Image/ImageViewer/image.png
%{_datadir}/%{name}/examples/Image/ImageViewer/ImageViewer.gambas
%{_datadir}/%{name}/examples/Image/ImageViewer/.project
%{_datadir}/%{name}/examples/Image/ImageViewer/.startup
%{_datadir}/%{name}/examples/Image/ImageViewer/.src/
%{_datadir}/%{name}/examples/Image/ImageViewer/test.png

%dir %{_datadir}/%{name}/examples/Image/Lighttable/
%dir %{_datadir}/%{name}/examples/Image/Lighttable/.lang/
%{_datadir}/%{name}/examples/Image/Lighttable/.action/
%{_datadir}/%{name}/examples/Image/Lighttable/.gambas/
%{_datadir}/%{name}/examples/Image/Lighttable/.src/
%{_datadir}/%{name}/examples/Image/Lighttable/.directory
%{_datadir}/%{name}/examples/Image/Lighttable/.hidden
%{_datadir}/%{name}/examples/Image/Lighttable/.icon*
%{_datadir}/%{name}/examples/Image/Lighttable/.project
%{_datadir}/%{name}/examples/Image/Lighttable/.settings
%{_datadir}/%{name}/examples/Image/Lighttable/.startup
%{_datadir}/%{name}/examples/Image/Lighttable/CHANGELOG
%{_datadir}/%{name}/examples/Image/Lighttable/close.png
%{_datadir}/%{name}/examples/Image/Lighttable/FStart.*
%{_datadir}/%{name}/examples/Image/Lighttable/hand1.png
%{_datadir}/%{name}/examples/Image/Lighttable/help-contents.png
%{_datadir}/%{name}/examples/Image/Lighttable/Help*.html
%{_datadir}/%{name}/examples/Image/Lighttable/Liesmich.txt
%{_datadir}/%{name}/examples/Image/Lighttable/Lighttable.gambas
%{_datadir}/%{name}/examples/Image/Lighttable/lighttable.png
%{_datadir}/%{name}/examples/Image/Lighttable/LTicon.png
%{_datadir}/%{name}/examples/Image/Lighttable/move.png
%{_datadir}/%{name}/examples/Image/Lighttable/Readme.txt
%{_datadir}/%{name}/examples/Image/Lighttable/zoom-in.png

%dir %{_datadir}/%{name}/examples/Image/PhotoTouch/
%dir %{_datadir}/%{name}/examples/Image/PhotoTouch/.lang/
%{_datadir}/%{name}/examples/Image/PhotoTouch/.directory
%{_datadir}/%{name}/examples/Image/PhotoTouch/.gambas/
%{_datadir}/%{name}/examples/Image/PhotoTouch/.info
%{_datadir}/%{name}/examples/Image/PhotoTouch/.icon*
%{_datadir}/%{name}/examples/Image/PhotoTouch/.list
%{_datadir}/%{name}/examples/Image/PhotoTouch/.project
%{_datadir}/%{name}/examples/Image/PhotoTouch/.src/
%{_datadir}/%{name}/examples/Image/PhotoTouch/.startup
%{_datadir}/%{name}/examples/Image/PhotoTouch/PhotoTouch.gambas
%{_datadir}/%{name}/examples/Image/PhotoTouch/*.png

%dir %{_datadir}/%{name}/examples/Misc/Console/
%dir %{_datadir}/%{name}/examples/Misc/Console/.lang/
%{_datadir}/%{name}/examples/Misc/Console/.directory
%{_datadir}/%{name}/examples/Misc/Console/.gambas/
%{_datadir}/%{name}/examples/Misc/Console/.hidden
%{_datadir}/%{name}/examples/Misc/Console/.icon*
%{_datadir}/%{name}/examples/Misc/Console/.project
%{_datadir}/%{name}/examples/Misc/Console/.startup
%{_datadir}/%{name}/examples/Misc/Console/Console.gambas
%{_datadir}/%{name}/examples/Misc/Console/terminal.png
%{_datadir}/%{name}/examples/Misc/Console/.src/

%dir %{_datadir}/%{name}/examples/Misc/Evaluator/
%dir %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/
%{_datadir}/%{name}/examples/Misc/Evaluator/.directory
%{_datadir}/%{name}/examples/Misc/Evaluator/.gambas/
%{_datadir}/%{name}/examples/Misc/Evaluator/.hidden
%{_datadir}/%{name}/examples/Misc/Evaluator/.icon*
%{_datadir}/%{name}/examples/Misc/Evaluator/.project
%{_datadir}/%{name}/examples/Misc/Evaluator/.startup
%{_datadir}/%{name}/examples/Misc/Evaluator/Evaluator.gambas
%{_datadir}/%{name}/examples/Misc/Evaluator/.src/
%{_datadir}/%{name}/examples/Misc/Evaluator/calculator.png

%dir %{_datadir}/%{name}/examples/Misc/Explorer/
%dir %{_datadir}/%{name}/examples/Misc/Explorer/.lang/
%{_datadir}/%{name}/examples/Misc/Explorer/.directory
%{_datadir}/%{name}/examples/Misc/Explorer/.gambas/
%{_datadir}/%{name}/examples/Misc/Explorer/.hidden
%{_datadir}/%{name}/examples/Misc/Explorer/.icon*
%{_datadir}/%{name}/examples/Misc/Explorer/.project
%{_datadir}/%{name}/examples/Misc/Explorer/.startup
%{_datadir}/%{name}/examples/Misc/Explorer/Explorer.gambas
%{_datadir}/%{name}/examples/Misc/Explorer/.src/
%{_datadir}/%{name}/examples/Misc/Explorer/folder.png

%dir %{_datadir}/%{name}/examples/Misc/Notepad/
%dir %{_datadir}/%{name}/examples/Misc/Notepad/.lang/
%{_datadir}/%{name}/examples/Misc/Notepad/.directory
%{_datadir}/%{name}/examples/Misc/Notepad/.gambas/
%{_datadir}/%{name}/examples/Misc/Notepad/.hidden
%{_datadir}/%{name}/examples/Misc/Notepad/.icon*
%{_datadir}/%{name}/examples/Misc/Notepad/.project
%{_datadir}/%{name}/examples/Misc/Notepad/.startup
%{_datadir}/%{name}/examples/Misc/Notepad/.src/
%{_datadir}/%{name}/examples/Misc/Notepad/Notepad.gambas
%{_datadir}/%{name}/examples/Misc/Notepad/notepad.png

%dir %{_datadir}/%{name}/examples/Misc/PDFViewer/
%dir %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/
%{_datadir}/%{name}/examples/Misc/PDFViewer/.directory
%{_datadir}/%{name}/examples/Misc/PDFViewer/.gambas/
%{_datadir}/%{name}/examples/Misc/PDFViewer/.hidden
%{_datadir}/%{name}/examples/Misc/PDFViewer/.icon*
%{_datadir}/%{name}/examples/Misc/PDFViewer/.project
%{_datadir}/%{name}/examples/Misc/PDFViewer/.startup
%{_datadir}/%{name}/examples/Misc/PDFViewer/.src/
%{_datadir}/%{name}/examples/Misc/PDFViewer/PDFViewer.gambas
%{_datadir}/%{name}/examples/Misc/PDFViewer/pdf.png

%dir %{_datadir}/%{name}/examples/Multimedia/CDPlayer/
%dir %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.project
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/CDPlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/CDPlayer/cdrom.png

%dir %{_datadir}/%{name}/examples/Multimedia/MediaPlayer/
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.info
#need gst1
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.list
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.project
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/MediaPlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/MediaPlayer/*.png

%dir %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/
%dir %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.project
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/MoviePlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/MoviePlayer/video.png

%dir %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/
%dir %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.directory
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.icon*
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.project
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.src/
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.startup
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/MusicPlayer.gambas
%{_datadir}/%{name}/examples/Multimedia/MusicPlayer/sound.png

%dir %{_datadir}/%{name}/examples/Multimedia/MyWebCam/
%dir %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.directory
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.gambas/
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.icon*
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.project
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.src/
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/.startup
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/MyWebCam.gambas
%{_datadir}/%{name}/examples/Multimedia/MyWebCam/camera.png

%dir %{_datadir}/%{name}/examples/Multimedia/WebCam/
%{_datadir}/%{name}/examples/Multimedia/WebCam/.directory
%{_datadir}/%{name}/examples/Multimedia/WebCam/.gambas/
%{_datadir}/%{name}/examples/Multimedia/WebCam/.icon*
%{_datadir}/%{name}/examples/Multimedia/WebCam/.project
%{_datadir}/%{name}/examples/Multimedia/WebCam/.src/
%{_datadir}/%{name}/examples/Multimedia/WebCam/.startup
%{_datadir}/%{name}/examples/Multimedia/WebCam/WebCam.gambas
%{_datadir}/%{name}/examples/Multimedia/WebCam/camera.png
%{_datadir}/%{name}/examples/Multimedia/WebCam/settings.png

%dir %{_datadir}/%{name}/examples/Networking/ClientSocket/
%dir %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/
%{_datadir}/%{name}/examples/Networking/ClientSocket/.directory
%{_datadir}/%{name}/examples/Networking/ClientSocket/.gambas/
%{_datadir}/%{name}/examples/Networking/ClientSocket/.hidden
%{_datadir}/%{name}/examples/Networking/ClientSocket/.icon*
%{_datadir}/%{name}/examples/Networking/ClientSocket/.project
%{_datadir}/%{name}/examples/Networking/ClientSocket/.startup
%{_datadir}/%{name}/examples/Networking/ClientSocket/ClientSocket.gambas
%{_datadir}/%{name}/examples/Networking/ClientSocket/.src/
%{_datadir}/%{name}/examples/Networking/ClientSocket/socket.png

%dir %{_datadir}/%{name}/examples/Networking/DnsClient/
%dir %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/
%{_datadir}/%{name}/examples/Networking/DnsClient/.directory
%{_datadir}/%{name}/examples/Networking/DnsClient/.gambas/
%{_datadir}/%{name}/examples/Networking/DnsClient/.hidden
%{_datadir}/%{name}/examples/Networking/DnsClient/.icon*
%{_datadir}/%{name}/examples/Networking/DnsClient/.project
%{_datadir}/%{name}/examples/Networking/DnsClient/.startup
%{_datadir}/%{name}/examples/Networking/DnsClient/DnsClient.gambas
%{_datadir}/%{name}/examples/Networking/DnsClient/.src/
%{_datadir}/%{name}/examples/Networking/DnsClient/dnsclient.png

%dir %{_datadir}/%{name}/examples/Networking/HTTPGet/
%dir %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/
%{_datadir}/%{name}/examples/Networking/HTTPGet/.directory
%{_datadir}/%{name}/examples/Networking/HTTPGet/.gambas/
%{_datadir}/%{name}/examples/Networking/HTTPGet/.hidden
%{_datadir}/%{name}/examples/Networking/HTTPGet/.icon*
%{_datadir}/%{name}/examples/Networking/HTTPGet/.project
%{_datadir}/%{name}/examples/Networking/HTTPGet/.startup
%{_datadir}/%{name}/examples/Networking/HTTPGet/.src/
%{_datadir}/%{name}/examples/Networking/HTTPGet/HTTPGet.gambas
%{_datadir}/%{name}/examples/Networking/HTTPGet/httpclient.png

%dir %{_datadir}/%{name}/examples/Networking/HTTPPost/
%dir %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/
%{_datadir}/%{name}/examples/Networking/HTTPPost/.directory
%{_datadir}/%{name}/examples/Networking/HTTPPost/.gambas/
%{_datadir}/%{name}/examples/Networking/HTTPPost/.hidden
%{_datadir}/%{name}/examples/Networking/HTTPPost/.icon*
%{_datadir}/%{name}/examples/Networking/HTTPPost/.project
%{_datadir}/%{name}/examples/Networking/HTTPPost/.startup
%{_datadir}/%{name}/examples/Networking/HTTPPost/.src/
%{_datadir}/%{name}/examples/Networking/HTTPPost/HTTPPost.gambas
%{_datadir}/%{name}/examples/Networking/HTTPPost/httpclient.png

%dir %{_datadir}/%{name}/examples/Networking/POPMailbox/
%{_datadir}/%{name}/examples/Networking/POPMailbox/.directory
%{_datadir}/%{name}/examples/Networking/POPMailbox/.gambas/
%{_datadir}/%{name}/examples/Networking/POPMailbox/.icon*
%{_datadir}/%{name}/examples/Networking/POPMailbox/.project
%{_datadir}/%{name}/examples/Networking/POPMailbox/.src/
%{_datadir}/%{name}/examples/Networking/POPMailbox/.startup
%{_datadir}/%{name}/examples/Networking/POPMailbox/POPMailbox.gambas
%{_datadir}/%{name}/examples/Networking/POPMailbox/pop3client.png

%dir %{_datadir}/%{name}/examples/Networking/SerialPort/
%dir %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/
%{_datadir}/%{name}/examples/Networking/SerialPort/.directory
%{_datadir}/%{name}/examples/Networking/SerialPort/.gambas/
%{_datadir}/%{name}/examples/Networking/SerialPort/.hidden
%{_datadir}/%{name}/examples/Networking/SerialPort/.icon*
%{_datadir}/%{name}/examples/Networking/SerialPort/.project
%{_datadir}/%{name}/examples/Networking/SerialPort/.startup
%{_datadir}/%{name}/examples/Networking/SerialPort/.src/
%{_datadir}/%{name}/examples/Networking/SerialPort/SerialPort.gambas
%{_datadir}/%{name}/examples/Networking/SerialPort/serialport.png

%dir %{_datadir}/%{name}/examples/Networking/ServerSocket/
%dir %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/
%{_datadir}/%{name}/examples/Networking/ServerSocket/.directory
%{_datadir}/%{name}/examples/Networking/ServerSocket/.gambas/
%{_datadir}/%{name}/examples/Networking/ServerSocket/.hidden
%{_datadir}/%{name}/examples/Networking/ServerSocket/.icon*
%{_datadir}/%{name}/examples/Networking/ServerSocket/.project
%{_datadir}/%{name}/examples/Networking/ServerSocket/.startup
%{_datadir}/%{name}/examples/Networking/ServerSocket/.src/
%{_datadir}/%{name}/examples/Networking/ServerSocket/ServerSocket.gambas
%{_datadir}/%{name}/examples/Networking/ServerSocket/serversocket.png

%dir %{_datadir}/%{name}/examples/Networking/UDPServerClient/
%dir %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.directory
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.gambas/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.hidden
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.icon*
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.project
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.startup
%{_datadir}/%{name}/examples/Networking/UDPServerClient/.src/
%{_datadir}/%{name}/examples/Networking/UDPServerClient/UDPServerClient.gambas
%{_datadir}/%{name}/examples/Networking/UDPServerClient/udpsocket.png

%dir %{_datadir}/%{name}/examples/Networking/WebBrowser/
%dir %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/
%{_datadir}/%{name}/examples/Networking/WebBrowser/.directory
%{_datadir}/%{name}/examples/Networking/WebBrowser/.gambas/
%{_datadir}/%{name}/examples/Networking/WebBrowser/.hidden
%{_datadir}/%{name}/examples/Networking/WebBrowser/.icon*
%{_datadir}/%{name}/examples/Networking/WebBrowser/.project
%{_datadir}/%{name}/examples/Networking/WebBrowser/.startup
%{_datadir}/%{name}/examples/Networking/WebBrowser/.src/
%{_datadir}/%{name}/examples/Networking/WebBrowser/WebBrowser.gambas
%{_datadir}/%{name}/examples/Networking/WebBrowser/konqueror.png
%{_datadir}/%{name}/examples/Networking/WebBrowser/list-*.png

%dir %{_datadir}/%{name}/examples/OpenGL/3DWebCam/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.directory
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.gambas/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.hidden
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.icon*
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.project
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.startup
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/3DWebCam.gambas
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/.src/
%{_datadir}/%{name}/examples/OpenGL/3DWebCam/webcam.png

%dir %{_datadir}/%{name}/examples/OpenGL/GambasGears/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.directory
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.gambas/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.hidden
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.icon*
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.project
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.startup
%{_datadir}/%{name}/examples/OpenGL/GambasGears/GambasGears.gambas
%{_datadir}/%{name}/examples/OpenGL/GambasGears/.src/
%{_datadir}/%{name}/examples/OpenGL/GambasGears/gears.png

%dir %{_datadir}/%{name}/examples/OpenGL/Md2Model/
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.directory
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.gambas/
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.icon*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.project
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.settings
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.src/
%{_datadir}/%{name}/examples/OpenGL/Md2Model/.startup
%{_datadir}/%{name}/examples/OpenGL/Md2Model/Md2Model.gambas
%{_datadir}/%{name}/examples/OpenGL/Md2Model/Weapon.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/bauul.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/goblin.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/icon.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/igdosh.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/knight.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/ogro.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/rat.*
%{_datadir}/%{name}/examples/OpenGL/Md2Model/rhino.*

%dir %{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.directory
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.gambas/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.icon*
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.project
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.src/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/.startup
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/NeHe.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/NeHeTutorial.gambas
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/*.txt
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/Star.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/barrel.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/ceiling.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/crate.jpeg
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/floor.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/glass.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/icon.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorial/wall.jpeg

%dir %{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.directory
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.gambas/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.icon*
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.project
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.src/
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/.startup
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/NeHeTutorialShell.gambas
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/icon.png
%{_datadir}/%{name}/examples/OpenGL/NeHeTutorialShell/nehe.png

%dir %{_datadir}/%{name}/examples/OpenGL/PDFPresentation/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.directory
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.gambas/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.hidden
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.icon*
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.project
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.settings
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.startup
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/.src/
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/PDFPresentation.gambas
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/icon.png
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/logo.png
%{_datadir}/%{name}/examples/OpenGL/PDFPresentation/music.xm

%dir %{_datadir}/%{name}/examples/OpenGL/TunnelSDL/
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.dir_icon.png
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.directory
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.gambas/
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.icon*
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.project
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.src/
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/.startup
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/CHANGELOG
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/TunnelSDL.gambas
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/texture.png
%{_datadir}/%{name}/examples/OpenGL/TunnelSDL/tunnelsdl.png

%dir %{_datadir}/%{name}/examples/Printing/Printing/
%{_datadir}/%{name}/examples/Printing/Printing/.directory
%{_datadir}/%{name}/examples/Printing/Printing/.gambas/
%{_datadir}/%{name}/examples/Printing/Printing/.hidden
%{_datadir}/%{name}/examples/Printing/Printing/.icon*
%{_datadir}/%{name}/examples/Printing/Printing/.project
%{_datadir}/%{name}/examples/Printing/Printing/.startup
%{_datadir}/%{name}/examples/Printing/Printing/molly-malone.txt
%{_datadir}/%{name}/examples/Printing/Printing/printer-laser.png
%{_datadir}/%{name}/examples/Printing/Printing/.src/
%{_datadir}/%{name}/examples/Printing/Printing/Printing.gambas

%dir %{_datadir}/%{name}/examples/Printing/ReportExample/
%{_datadir}/%{name}/examples/Printing/ReportExample/.connection/
%{_datadir}/%{name}/examples/Printing/ReportExample/.directory
%{_datadir}/%{name}/examples/Printing/ReportExample/.gambas/
%{_datadir}/%{name}/examples/Printing/ReportExample/.hidden/
%{_datadir}/%{name}/examples/Printing/ReportExample/.icon*
%{_datadir}/%{name}/examples/Printing/ReportExample/.project
%{_datadir}/%{name}/examples/Printing/ReportExample/.settings
%{_datadir}/%{name}/examples/Printing/ReportExample/.src/
%{_datadir}/%{name}/examples/Printing/ReportExample/.startup
%{_datadir}/%{name}/examples/Printing/ReportExample/ReportExample.gambas
%{_datadir}/%{name}/examples/Printing/ReportExample/gambas.svg

# Translation files
%lang(ca) %{_datadir}/%{name}/examples/Basic/Blights/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Blights/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Blights/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Blights/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Basic/Blights/.lang/fr.*o
%lang(sv) %{_datadir}/%{name}/examples/Basic/Blights/.lang/sv.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Collection/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Collection/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Collection/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Collection/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Object/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Object/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Object/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Object/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Basic/Timer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Basic/Timer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Basic/Timer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Basic/Timer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/ArrayOfControls/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/Embedder/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/Embedder/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/Embedder/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/Embedder/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/HighlightEditor/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/fr.*o
%lang(sv) %{_datadir}/%{name}/examples/Control/TextEdit/.lang/sv.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/TreeView/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/TreeView/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/TreeView/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Control/TreeView/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Control/Wizard/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Control/Wizard/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Control/Wizard/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/Database/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Database/Database/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Database/Database/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Database/Database/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Database/MySQLExample/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Database/PictureDatabase/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Barcode/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Chart/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Clock/.lang/es.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Fractal/.lang/cs.*o
%lang(fr) %{_datadir}/%{name}/examples/Drawing/Fractal/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/Gravity/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Drawing/OnScreenDisplay/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Drawing/Painting/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Drawing/Painting/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Drawing/Painting/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Concent/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Concent/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Concent/.lang/de.*o
%lang(en) %{_datadir}/%{name}/examples/Games/Concent/.lang/en.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Concent/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Games/Concent/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/DeepSpace/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/GameOfLife/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/GNUBoxWorld/.lang/es*.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/cs.*o
%lang(ja) %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/ja.*o
%lang(zh) %{_datadir}/%{name}/examples/Games/MineSweeper/.lang/zh*.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Puzzle1To8/.lang/es*.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/RobotFindsKitten/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Snake/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Snake/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Snake/.lang/de.*o
%lang(ca) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Games/Solitaire/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Image/ImageViewer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/de.*o
%lang(en) %{_datadir}/%{name}/examples/Image/Lighttable/.lang/en.*o
%lang(fr) %{_datadir}/%{name}/examples/Image/PhotoTouch/.lang/fr.*o
%lang(fr) %{_datadir}/%{name}/examples/Misc/Console/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Evaluator/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Explorer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/Notepad/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Misc/PDFViewer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/CDPlayer/.lang/es.*o
%dir %{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.lang
%lang(fr) %{_datadir}/%{name}/examples/Multimedia/MediaPlayer/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/MoviePlayer/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/es.*o
%lang(fr) %{_datadir}/%{name}/examples/Multimedia/MusicPlayer/.lang/fr.*o
%lang(ca) %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Multimedia/MyWebCam/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/ClientSocket/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/DnsClient/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/HTTPGet/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/HTTPPost/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/SerialPort/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/ServerSocket/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/cs.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/UDPServerClient/.lang/es.*o
%lang(ca) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/ca.*o
%lang(cs) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/cs.*o
%lang(de) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/de.*o
%lang(es) %{_datadir}/%{name}/examples/Networking/WebBrowser/.lang/es.*

#-----------------------------------------------------------------------------

%package gb-cairo
Summary: The Gambas Cairo component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-gb-db = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-gb-db = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-gb-db = %{version}

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
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-gb-db = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-gb-db = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

%description gb-gui
This is a component that just loads gb.qt if you are running KDE or
gb.gtk in the other cases.

%files gb-gui
%doc README  ChangeLog
%{_libdir}/%{name}/gb.gui.*
%{_datadir}/%{name}/info/gb.gui.*

#-----------------------------------------------------------------------------
%if %{mdvver} < 201410
%package gb-jit
Summary: The Gambas JIT component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}

%description gb-jit
This component provides the jit compiler for gambas.

%files gb-jit
%doc README  ChangeLog
%{_libdir}/%{name}/gb.jit.*
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.jit.info
%{_datadir}/%{name}/info/gb.jit.list
%endif
#-----------------------------------------------------------------------------
%package gb-image
Summary: The Gambas image manipulation component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

%description gb-media
This package contains the Gambas media component.

%files gb-media
%doc README  ChangeLog
%{_libdir}/%{name}/gb.media.*
%{_datadir}/%{name}/info/gb.media.*
%endif

#-----------------------------------------------------------------------------
%package gb-mysql
Summary: The Gambas mysql component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-gb-net = %{version}-%{release}

%description gb-net-curl
This component allows your programs to easily become FTP or HTTP clients.

%files gb-net-curl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.net.curl.so*
%{_libdir}/%{name}/gb.net.curl.component
%dir %{_datadir}/%{name}/info
%{_datadir}/%{name}/info/gb.net.curl.info
%{_datadir}/%{name}/info/gb.net.curl.list

#-----------------------------------------------------------------------------

%package gb-net-smtp
Summary: The Gambas SMTP component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{name}-gb-net = %{version}-%{release}

%description gb-net-smtp
This component allows you to send emails using the SMTP protocol.

%files gb-net-smtp
%doc README  ChangeLog
%{_libdir}/%{name}/gb.net.smtp.*
%{_datadir}/%{name}/info/gb.net.smtp.*

#-----------------------------------------------------------------------------

%package gb-opengl
Summary: The Gambas OpenGL component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
%{_datadir}/%{name}/gb.sdl

#-----------------------------------------------------------------------------

%package gb-sdl-sound
Summary: The Gambas SDL sound component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}

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

%package gb-settings
Summary: The Gambas settings component
Group: Development/Other
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}
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
Requires: %{name}-runtime = %{version}-%{release}
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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires: %{name}-runtime = %{version}-%{release}

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
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	%{name}-gb-mime

%description gb-net-pop3
New component that implements a POP3 client.

%files gb-net-pop3
%doc README  ChangeLog
%{_libdir}/%{name}/gb.net.pop3.*
%{_datadir}/%{name}/info/gb.net.pop3.*

#---------------------------------------------------------------------------

%package gb-args
Summary:	Gambas3 component package for args
Group:		Development/Other
Requires:	%{name}-runtime = %{version}-%{release}

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
Requires:	%{name}-runtime = %{version}-%{release}

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
Requires:	%{name}-runtime = %{version}-%{release}

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
Requires:	%{name}-runtime = %{version}-%{release}

%description gb-memcached
%{summary}.

%files gb-memcached
%doc README  ChangeLog
%{_libdir}/%{name}/gb.memcached.*
%{_datadir}/%{name}/info/gb.memcached.*

#---------------------------------------------------------------------------
%package gb-clipper
Group:   Development/Other
Requires:      %{name}-runtime = %{version}-%{release}

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
Requires:      %{name}-runtime = %{version}-%{release}

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
Requires:      %{name}-runtime = %{version}-%{release}

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
Requires:      %{name}-runtime = %{version}-%{release}

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
Requires:      %{name}-runtime = %{version}-%{release}
Requires:      %{name}-gb-opengl = %{version}-%{release}

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
Requires:      %{name}-runtime = %{version}-%{release}

%description gb-openssl
Component to wrap cryptographic functions of 
libcrypto from the OpenSSL project.

%files gb-openssl
%doc README  ChangeLog
%{_libdir}/%{name}/gb.openssl.*
%{_datadir}/%{name}/info/gb.openssl.*

#---------------------------------------------------------------------------














































