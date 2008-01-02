%define	name	ghemical
%define	version	2.10
%define	release	%mkrel 3

Summary:	Molecular mechanics and quantum mechanics frontend for GNOME
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sciences/Chemistry
Source0:	http://www.uku.fi/~thassine/projects/download/%{name}-%{version}.tar.gz
URL:		http://www.uku.fi/~thassine/ghemical/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libghemical-devel = %{version} openbabel-devel >= 2.0
BuildRequires:	bonoboui-devel f2c flex gtkglext-devel mopac7-devel >= 1.10
BuildRequires:	libglade2.0-devel >= 2.4.0
BuildRequires:	mesaglut-devel libSC-devel
Requires:	libghemical-data = %{version}
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png

%description
Ghemical is a computational chemistry software package released under the 
GNU GPL.
Ghemical is written in C++. It has a graphical user interface (in fact, 
a couple of them), and it supports both quantum-mechanics (semi-empirical 
and ab initio) models and molecular mechanics models (there is an experimental
Tripos 5.2-like force field for organic molecules). Also a tool for reduced 
protein models is included. Geometry optimization, molecular dynamics
and a large set of visualization tools are currently available.

%prep
%setup -q

%build
libtoolize --copy --force
aclocal
autoconf
automake
CXXFLAGS="$RPM_OPT_FLAGS `pkg-config --cflags libbonobo-2.0` `pkg-config --cflags libbonoboui-2.0`" \
%configure2_5x	--enable-threads \
		--enable-bonobo \
		--enable-openbabel \
		--enable-shortcuts \
		--enable-gamess
#ugly hack, yeye..
perl -pi -e "s#-lmopac7#-lmopac7 `pkg-config --libs libbonobo-2.0` `pkg-config --libs libbonoboui-2.0` -lglut -lf2c#g" src/Makefile
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -d %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{name}
?package(ghemical): \
	command="%{name}" \
	icon="%{name}.png" \
	needs="x11" \
	section="More Applications/Sciences/Chemistry" \
	title="Ghemical" \
	longtitle="GNOME MM/QM Frontend" \
	xdg="true"
EOF

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=GNOME MM/QM Frontend
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Chemistry;X-MandrivaLinux-MoreApplications-Sciences-Chemistry;
EOF

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README NEWS TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop

