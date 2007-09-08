%define short_name httpclient
%define name       jakarta-commons-%{short_name}
%define version    3.0.1
%define release    3
%define gcj_support 1
%define section    free

Name:           %{name}
Version:        %{version}
Release:        %mkrel %{release}
Epoch:          1
Summary:        Jakarta Commons HTTPClient Package
License:        Apache License
Source0:        http://archive.apache.org/dist/jakarta/commons/httpclient/source/commons-httpclient-%{version}-src.tar.bz2
Patch1:		%{name}-examples.patch
URL:            http://jakarta.apache.org/commons/httpclient/
Group:          Development/Java
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant
BuildRequires:  jakarta-commons-codec
BuildRequires:  jakarta-commons-logging >= 0:1.0.3
BuildRequires:  jce >= 0:1.2.2
BuildRequires:  jsse >= 0:1.0.3.01
BuildRequires:	java-devel
BuildRequires:  java-javadoc
BuildRequires:  jakarta-commons-logging-javadoc

Requires:       jakarta-commons-logging >= 0:1.0.3

Provides:       commons-%{short_name}
Obsoletes:      commons-%{short_name}

%description
The Hyper-Text Transfer Protocol (HTTP) is perhaps the most significant
protocol used on the Internet today. Web services, network-enabled
appliances and the growth of network computing continue to expand the
role of the HTTP protocol beyond user-driven web browsers, and increase
the number of applications that may require HTTP support.
Although the java.net package provides basic support for accessing
resources via HTTP, it doesn't provide the full flexibility or
functionality needed by many applications. The Jakarta Commons HTTP
Client component seeks to fill this void by providing an efficient,
up-to-date, and feature-rich package implementing the client side of the
most recent HTTP standards and recommendations.
Designed for extension while providing robust support for the base HTTP
protocol, the HTTP Client component may be of interest to anyone
building HTTP-aware client applications such as web browsers, web
service clients, or systems that leverage or extend the HTTP protocol
for distributed communication.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        demo
Summary:        Demos for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
%{summary}.

%package        manual
Summary:        Manual for %{name}
Group:          Development/Java

%description    manual
%{summary}.


%prep
%setup -q -n commons-%{short_name}-%{version}
%patch1 -p1
mkdir lib # duh
rm -rf docs/apidocs docs/*.patch docs/*.orig docs/*.rej


%build
export CLASSPATH=%(build-classpath jsse jce junit jakarta-commons-codec jakarta-commons-logging)
%ant \
  -Dbuild.sysclasspath=first \
  -Djavadoc.j2sdk.link=%{_javadocdir}/java \
  -Djavadoc.logging.link=%{_javadocdir}/jakarta-commons-logging \
  dist


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/commons-%{short_name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}
mv dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr src/examples src/contrib $RPM_BUILD_ROOT%{_datadir}/%{name}

# manual and docs
rm -f dist/docs/{BUILDING,TESTING}.txt
ln -s %{_javadocdir}/%{name} dist/docs/apidocs

%{__perl} -pi -e 's/\r$//g' *.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}


%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt RELEASE_NOTES.txt
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc dist/docs/*


