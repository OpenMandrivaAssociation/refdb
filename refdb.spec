%define		name refdb
%define		version 0.9.8.1
%define		rel pre9
#%define		release %mkrel 0.%{rel}.1
%define		release %mkrel 1

Summary:	RefDB is a reference database and bibliography tool

Name:		%{name}
Version:	%{version}
Release:	%{release}
#Source0:	http://refdb.sourceforge.net/pre/refdb-%{version}-%{rel}.tar.bz2
#Source0:	http://prdownloads.sourceforge.net/sourceforge/refdb/refdb-%{version}.tar.bz2
Source0:	http://prdownloads.sourceforge.net/sourceforge/refdb/refdb-0.9.8-1.tar.bz2
Source1:	refdb-README.urpmi
Patch0:		refdb.in.patch
Patch1:		refdbsearch.php.in.patch

License:	GPL
Group:		Sciences/Computer science
Url:		http://refdb.sourceforge.net

Requires(pre):	rpm-helper
Requires:	apache-mod_php => 5
Requires:	readline
Buildrequires:	btparse
Buildrequires:	libdbi-devel	
Buildrequires:	libexpat-devel
Buildrequires:	libncurses-devel
BuildRequires:	libreadline-devel
Buildrequires:	perl(MARC::Charset)
Buildrequires:	perl(MARC::Record)
Buildrequires:	perl(RefDB)
Buildrequires:	perl(Term::Clui)
Buildrequires:	perl(Text::Iconv)
Buildrequires:	perl(XML::Parser)
#Buildrequires:		docbook-style-xsl
#Buildrequires:		openjade
#Buildrequires:		tei-xsl
#Buildrequires:		libxslt-proc
#Buildrequires:		tidy

#BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
#BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRoot:	%{_tmppath}/%{name}-0.9.8-1

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

%prep		rm -rf %{buildroot}
#%setup -q -n	%{name}-%{version}-%{rel}
#%setup -q -n	%{name}-%{version}
%setup -q -n	%{name}-0.9.8-1

cp %{SOURCE1}	README.urpmi
%patch0 -p0
%patch1 -p0

%build
%configure --disable-rpath 
%make

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}/%{_localstatedir}/%{name}/db

# LSB and pinit compliant initscript
install -D -m755 scripts/%{name} %{buildroot}/%{_initrddir}/%{name}

# Web interface
mkdir -p %{buildroot}/%{_var}/www/%{name}
install	phpweb/admin.php \
	phpweb/external.php \
	phpweb/include.php \
	phpweb/index.html \
	phpweb/login.php \
	phpweb/refdb-prl-del.php \
	phpweb/refdbadd.html \
	phpweb/refdbadd.php \
	phpweb/refdbadmin.php \
	phpweb/refdbdbquery.php \
	phpweb/refdbkajquery.html \
	phpweb/refdbkajsearch.php \
	phpweb/refdblogout.php \
	phpweb/*.css \
	phpweb/refdbquery.html \
	phpweb/refdbsearch.php %{buildroot}/%{_var}/www/%{name}

# apache configuration
install -d -m755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{webappconfdir}/%{name}.conf << EORefDBconf
# RefDB Apache configuration
Alias /%{name}/ "%{_var}/www/%{name}/"

<Directory %{_var}/www/%{name}>
	Options +ExecCGI
	AllowOverride None
	Order allow,deny
	Allow from all
	AddType application/x-httpd-php .php .phtml
</Directory>
EORefDBconf

# php ini
install -d %{buildroot}%{_sysconfdir}/php.d/
cat > %{buildroot}%{_sysconfdir}/php.d/A53_%{name}.ini << EOphpini
;session.save_path = "/tmp"
;session.use_cookies = 1
session.auto_start = 1
register_globals = On
EOphpini

%makeinstall_std

# Remove some documentation files
%{__rm} -f	doc/*.xml
%{__rm} -f	doc/Makefile*
%{__rm} -f	doc/refdbmanualfig*
%{__rm} -f	doc/refdb-manual.fo
%{__rm} -rf	doc/include
%{__rm} -f	doc/citestylex/ele-desc/*~

# Clean some paths introduced by the install-sh scrip
#mv %{buildroot}/%{_datadir}/doc/%{name}-%{version}-%{rel} %{buildroot}/%{_datadir}/doc/%{name}-%{version}
mv %{buildroot}/%{_datadir}/doc/%{name}-0.9.8-1 %{buildroot}/%{_datadir}/doc/%{name}-%{version}

%clean
%{__rm} -rf	%{buildroot}

%post
%{_post_webapp}
%_post_service	%{name}
chmod 1777 %{_var}/www/%{name}

%preun
%_preun_service	%{name}

%postun
%{_postun_webapp}

%files
%defattr(-,root,root,0755)
%exclude	%{_bindir}/refdbc
%exclude	%{_bindir}/refdba
%exclude	%{_bindir}/refdbib
%{_bindir}/*
%exclude	%{_datadir}/%{name}/www
%{_datadir}/%{name}*
%{_initrddir}/refdb
%{_localstatedir}/%{name}/db
%{_mandir}/*/*
%config(noreplace)	%{_sysconfdir}/%{name}/*
%config(noreplace)	%{_sysconfdir}/php.d/A53_%{name}.ini
%attr(644,root,root)	%{_var}/www/%{name}/*
%config(noreplace)	%{webappconfdir}/%{name}.conf
%doc doc/*
%doc README.urpmi AUTHORS ChangeLog COPYING INSTALL NEWS README UPGRADING

%files -n %{name}-clients
%defattr(-,root,root,0755)
%{_bindir}/refdbc
%{_bindir}/refdba
%{_bindir}/refdbib


