%define rel	1

Summary:	Reference database and bibliography tool
Name:		refdb
Version:	0.9.9
Release:	%mkrel 7
License:	GPLv2+
Group:		Sciences/Computer science
URL:		http://refdb.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/sourceforge/refdb/%{name}-%{version}-%{rel}.tar.gz
Source1:	refdb-README.urpmi
Patch0:		refdb.in.patch
Patch1:		refdb-0.9.9-1-fix-format-errors.patch
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
Requires(post): rpm-helper
Requires(preun): rpm-helper
%if %mdkversion < 201010
Requires(postun): rpm-helper
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}

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

%build
%configure2_5x --disable-rpath 
%make

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/db

# LSB and pinit compliant initscript
install -D -m755 scripts/%{name} %{buildroot}/%{_initrddir}/%{name}

# Web interface
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/{css,images,includes,xsl}
install	phpweb/index.php		%{buildroot}%{_datadir}/%{name}
install phpweb/css/*.css		%{buildroot}%{_datadir}/%{name}/css
install phpweb/images/{*.gif,*.png}	%{buildroot}%{_datadir}/%{name}/images
install phpweb/includes/*.php		%{buildroot}%{_datadir}/%{name}/includes
install phpweb/xsl/*.xsl		%{buildroot}%{_datadir}/%{name}/xsl

# apache configuration
install -d -m 755 %{buildroot}%{webappconfdir}
cat > %{buildroot}%{webappconfdir}/%{name}.conf << EOR
# RefDB Apache configuration
Alias /%{name} %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
	Options +ExecCGI
	Order allow,deny
	Allow from all

    php_value session.auto_start = 1
    php_value register_globals = On
</Directory>
EOF

%makeinstall_std

# Remove some documentation files
%{__rm} -f	doc/*.xml
%{__rm} -f	doc/Makefile*
%{__rm} -f	doc/refdbmanualfig*
%{__rm} -f	doc/refdb-manual.fo
%{__rm} -rf	doc/include
%{__rm} -f	doc/citestylex/ele-desc/*~

# Clean some paths introduced by the install-sh scrip
mv %{buildroot}/%{_datadir}/doc/%{name}-%{version}-%{rel} \
    %{buildroot}/%{_datadir}/doc/%{name}

%clean
%{__rm} -rf	%{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif
%_post_service	%{name}
chmod 1777 %{_datadir}/%{name}

%preun
%_preun_service	%{name}

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

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
%attr(644,root,root)	%{_datadir}/%{name}/*
%config(noreplace)	%{webappconfdir}/%{name}.conf
%doc doc/*
%doc README.urpmi AUTHORS ChangeLog INSTALL NEWS README UPGRADING

%files -n %{name}-clients
%defattr(-,root,root,0755)
%{_bindir}/refdbc
%{_bindir}/refdba
%{_bindir}/refdbib
