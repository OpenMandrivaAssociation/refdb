%define rel	1

Summary:	Reference database and bibliography tool
Name:		refdb
Version:	0.9.9
Release:	%mkrel 5
Source0:	http://prdownloads.sourceforge.net/sourceforge/refdb/%{name}-%{version}-%{rel}.tar.gz
Source1:	refdb-README.urpmi
Patch0:		refdb.in.patch
License:	GPLv2+
Group:		Sciences/Computer science
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://refdb.sourceforge.net
Requires:	apache-mod_php => 5
BuildRequires:	btparse
BuildRequires:	libdbi-devel	
BuildRequires:	libexpat-devel
BuildRequires:	libncurses-devel
BuildRequires:	libreadline-devel
BuildRequires:	perl(MARC::Charset)
BuildRequires:	perl(MARC::Record)
BuildRequires:	perl(RefDB)
BuildRequires:	perl(Term::Clui)
BuildRequires:	perl(Text::Iconv)
BuildRequires:	perl(XML::Parser)

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
rm -rf %{buildroot}
%setup -q -n	%{name}-%{version}-%{rel}

cp %{SOURCE1}	README.urpmi
%patch0 -p0

%build
%configure2_5x --disable-rpath 
%make

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/db

# LSB and pinit compliant initscript
install -D -m755 scripts/%{name} %{buildroot}/%{_initrddir}/%{name}

# Web interface
mkdir -p %{buildroot}/%{_var}/www/%{name}
mkdir -p %{buildroot}/%{_var}/www/%{name}/{css,images,includes,xsl}
install	phpweb/index.php		%{buildroot}/%{_var}/www/%{name}
install phpweb/css/*.css		%{buildroot}/%{_var}/www/%{name}/css
install phpweb/images/{*.gif,*.png}	%{buildroot}/%{_var}/www/%{name}/images
install phpweb/includes/*.php		%{buildroot}/%{_var}/www/%{name}/includes
install phpweb/xsl/*.xsl		%{buildroot}/%{_var}/www/%{name}/xsl

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
mv %{buildroot}/%{_datadir}/doc/%{name}-%{version}-%{rel} %{buildroot}/%{_datadir}/doc/%{name}

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
%{_localstatedir}/lib/%{name}/db
%{_mandir}/*/*
%config(noreplace)	%{_sysconfdir}/%{name}/*
%config(noreplace)	%{_sysconfdir}/php.d/A53_%{name}.ini
%attr(644,root,root)	%{_var}/www/%{name}/*
%config(noreplace)	%{webappconfdir}/%{name}.conf
%doc doc/*
%doc README.urpmi AUTHORS ChangeLog INSTALL NEWS README UPGRADING

%files -n %{name}-clients
%defattr(-,root,root,0755)
%{_bindir}/refdbc
%{_bindir}/refdba
%{_bindir}/refdbib

