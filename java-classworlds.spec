%bcond_without	javadoc		# don't build javadoc
%define		srcname	classworlds
Summary:	Classworlds Classloader Framework
Name:		java-classworlds
Version:	1.1
Release:	0.1
License:	BSD-like
Group:		Libraries/Java
URL:		http://classworlds.codehaus.org/
# svn export http://svn.codehaus.org/classworlds/tags/CLASSWORLDS_1_1/classworlds/ classworlds-1.1
Source0:	http://execve.pl/PLD/classworlds-%{version}-src.tar.gz
# Source0-md5:	0a3b11baec9ad33dafa952533185f6c0
Source1:	%{name}-build.xml
Patch0:		%{name}-project_xml.patch
BuildRequires:	ant >= 0:1.6
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires(post):	jpackage-utils >= 0:1.7.2
Requires(postun):	jpackage-utils >= 0:1.7.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Classworlds is a framework for container developers who require
complex manipulation of Java's ClassLoaders. Java's native ClassLoader
mechanims and classes can cause much headache and confusion for
certain types of application developers. Projects which involve
dynamic loading of components or otherwise represent a 'container' can
benefit from the classloading control provided by classworlds.

%package        javadoc
Summary:	Javadoc for %{srcname}
Group:		Documentation

%description    javadoc
Javadoc for %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}
find -name "*.jar" | xargs rm
cp -p %{SOURCE1} build.xml
%patch0 -p0

%build
export CLASSPATH=target/classes:target/test-classes
export OPT_JAR_LIST=:
%ant -Dbuild.sysclasspath=only jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a target/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# depmap
%add_to_maven_depmap %{srcname} %{srcname} %{version} JPP %{srcname}
%add_to_maven_depmap %{srcname} %{srcname}-boot %{version} JPP %{srcname}-boot

# poms
install -d $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -p pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{srcname}.pom

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar
%{_datadir}/maven2/poms/JPP.%{srcname}.pom
%{_mavendepmapfragdir}/%{name}

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
