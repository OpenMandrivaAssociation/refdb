%define rel	1

Summary:	Reference database and bibliography tool
Name:		refdb
Version:	0.9.9
Release:	13
License:	GPLv2+
Group:		Sciences/Computer science
URL:		http://refdb.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/sourceforge/refdb/%{name}-%{version}-%{rel}.tar.gz
Source1:	refdb-README.urpmi
Patch0:		refdb.in.patch
Patch1:		refdb-0.9.9-1-fix-format-errors.patch
Patch2:		refdb-0.9.9-1-fix-underlinking.patch
Patch3:		refdb-0.9.9-1-fix-doc-installation.patch
Requires:	apache-mod_php => 5
BuildRequires:	btparser
BuildRequires:	libdbi-devel	
BuildRequires:	expat-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	readline-devel
BuildRequires:	gettext-devel
BuildRequires:	perl(MARC::Charset)
BuildRequires:	perl(MARC::Record)
BuildRequires:	perl(RefDB)
BuildRequires:	perl(Term::Clui)
BuildRequires:	perl(Text::Iconv)
BuildRequires:	perl(XML::Parser)
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
RefDB is a reference database and bibliography tool for
SGML, XML, and LaTeX documents, sort of a Reference
Manager or BibTeX for markup languages. It is portable and
known to run on Linux, FreeBSD, and Windows/Cygwin.

%package -n %{name}-clients
Summary:	Clients for using %{name}
Group:		Networking/Remote access

%description	-n %{name}-clients
Clients allowing to connect to the refdb server.

%prep		
%setup -q -n	%{name}-%{version}-%{rel}

cp %{SOURCE1}	README.urpmi
%patch0 -p 0
%patch1 -p 1
%patch2 -p 1
%patch3 -p 1
autoreconf

%build
%configure2_5x --disable-rpath 
%make

%install
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/db

# LSB and pinit compliant initscript
install -D -m755 scripts/%{name} %{buildroot}/%{_initrddir}/%{name}

# Web interface
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/{css,images,includes,xsl}
install	phpweb/index.php	%{buildroot}%{_datadir}/%{name}
install phpweb/css/*.css	%{buildroot}%{_datadir}/%{name}/css
install phpweb/images/{*.gif,*.png}	%{buildroot}%{_datadir}/%{name}/images
install phpweb/includes/*.php	%{buildroot}%{_datadir}/%{name}/includes
install phpweb/xsl/*.xsl	%{buildroot}%{_datadir}/%{name}/xsl

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
# RefDB Apache configuration
Alias /%{name} %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
	Options +ExecCGI
	Require all granted

    php_flag session.auto_start 1
    php_flag register_globals on
</Directory>
EOF

%makeinstall_std

find %{buildroot}%{_docdir} -name *~ | xargs rm -f

%post
%_post_service	%{name}
chmod 1777 %{_datadir}/%{name}

%preun
%_preun_service	%{name}

%files
%{_bindir}/bib2ris-utf8
%{_bindir}/db2ris
%{_bindir}/eenc
%{_bindir}/en2ris
%{_bindir}/marc2ris
%{_bindir}/med2ris
%{_bindir}/refdb-backup
%{_bindir}/refdb-init
%{_bindir}/refdb-ms
%{_bindir}/refdb-restore
%{_bindir}/refdb-sruserver
%{_bindir}/refdb_dos2unix
%{_bindir}/refdb_latex2utf8txt
%{_bindir}/refdbd
%{_bindir}/refdbjade
%{_bindir}/refdbsru
%{_bindir}/refdbxml
%{_bindir}/refdbxp
%{_bindir}/runbib
%{_bindir}/refdbnd
%{_datadir}/%{name}
%{_initrddir}/refdb
%{_localstatedir}/lib/%{name}
%{_mandir}/*/*
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_webappconfdir}/%{name}.conf
%doc doc/*
%doc README.urpmi AUTHORS ChangeLog INSTALL NEWS README UPGRADING

%files -n %{name}-clients
%{_bindir}/refdbc
%{_bindir}/refdba
%{_bindir}/refdbib
%{_bindir}/refdbctl

