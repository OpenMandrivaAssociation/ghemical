%define releasedate 20111012
Name:		ghemical
Version:	3.0.0
Release:	3
Summary:	Molecular mechanics and quantum mechanics frontend for GNOME
License:	GPLv2+
Group:		Sciences/Chemistry
URL:		http://www.bioinformatics.org/ghemical/ghemical/index.html
Source0:	http://www.bioinformatics.org/ghemical/download/release%{releasedate}/%{name}-%{version}.tar.gz
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png

BuildRequires:	gcc-gfortran
BuildRequires:	ghemical-devel >= %{version}
BuildRequires:	openbabel-devel >= 2.2
BuildRequires:	pkgconfig(libbonoboui-2.0)
BuildRequires:	f2c
BuildRequires:	flex
BuildRequires:	gtkglext-devel
BuildRequires:	mopac7-devel >= 1.14
BuildRequires:	oglappth-devel >= 0.98
BuildRequires:	pkgconfig(libglade-2.0) >= 2.4.0
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	SC-devel
BuildRequires:	intltool

Requires:	libghemical-data >= 2.99.1


%description
Ghemical is a computational chemistry application.
Ghemical is written in C++. It has a graphical user interface (in fact, 
a couple of them), and it supports both quantum-mechanics (semi-empirical 
and ab initio) models and molecular mechanics models (there is an experimental
Tripos 5.2-like force field for organic molecules). Also a tool for reduced 
protein models is included. Geometry optimization, molecular dynamics
and a large set of visualization tools are currently available.

%prep
%setup -q
#help : use default www-browser
perl -pi -e "s|mozilla|www-browser|" src/gtk_app.cpp

%build
# never do like this...
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

autoreconf -fi
%configure2_5x	--enable-threads \
		--enable-bonobo \
		--enable-openbabel \
		--enable-shortcuts \
		--enable-gamess

%make LIBS="`pkg-config --libs libbonobo-2.0` `pkg-config --libs libbonoboui-2.0` \
 `pkg-config libglade-2.0 --libs` `pkg-config gtkglext-1.0 --libs` \
 -lghemical -lmopac7 -loglappth -lopenbabel -lf2c `sc-config --libs`"

%install
%makeinstall_std

install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=GNOME MM/QM Frontend
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Science;Chemistry;
EOF

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog README NEWS TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
