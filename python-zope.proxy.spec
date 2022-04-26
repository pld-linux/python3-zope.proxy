#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (installed package required)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	zope.proxy
Summary:	Mostly-transparent wrappers around another object
Summary(pl.UTF-8):	Prawie przezroczyste obudowywanie innych obiektów
Name:		python-%{module}
Version:	4.5.0
Release:	5
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.proxy/zope.proxy-%{version}.tar.gz
# Source0-md5:	f18df4454bd57e7352be922f7a43dffb
URL:		https://www.zope.dev/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-zope.interface
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.testrunner
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
Obsoletes:	Zope-Proxy < 3.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Proxies are special objects which serve as mostly-transparent wrappers
around another object, intervening in the apparent behavior of the
wrapped object only when necessary to apply the policy (e.g., access
checking, location brokering, etc.) for which the proxy is
responsible.

%description -l pl.UTF-8
Proxy to specjalne obiekty służące jako prawie przezroczyste
obudowanie innego obiektu, wkraczające w zwykłe zachowanie
obudowywanego obiektu tylko w razie potrzeby, aby zastosować politykę
(np. kontrolę dostępu, pośredniczenie itp.), za którą odpowiada proxy.

%package devel
Summary:	Header file for C extensions using zope.proxy module
Summary(pl.UTF-8):	Plik nagłówkowy dla rozszerzeń w C wykorzystujących moduł zope.proxy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-devel >= 1:2.7

%description devel
Header file for C extensions using zope.proxy module.

%description devel -l pl.UTF-8
Plik nagłówkowy dla rozszerzeń w C wykorzystujących moduł zope.proxy.

%package -n python3-%{module}
Summary:	Mostly-transparent wrappers around another object
Summary(pl.UTF-8):	Prawie przezroczyste obudowywanie innych obiektów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
Proxies are special objects which serve as mostly-transparent wrappers
around another object, intervening in the apparent behavior of the
wrapped object only when necessary to apply the policy (e.g., access
checking, location brokering, etc.) for which the proxy is
responsible.

%description -n python3-%{module} -l pl.UTF-8
Proxy to specjalne obiekty służące jako prawie przezroczyste
obudowanie innego obiektu, wkraczające w zwykłe zachowanie
obudowywanego obiektu tylko w razie potrzeby, aby zastosować politykę
(np. kontrolę dostępu, pośredniczenie itp.), za którą odpowiada proxy.

%package -n python3-%{module}-devel
Summary:	Header file for C extensions using zope.proxy module
Summary(pl.UTF-8):	Plik nagłówkowy dla rozszerzeń w C wykorzystujących moduł zope.proxy
Group:		Development/Libraries
Requires:	python3-%{module} = %{version}-%{release}
Requires:	python3-devel >= 1:3.5

%description -n python3-%{module}-devel
Header file for C extensions using zope.proxy module.

%description -n python3-%{module}-devel -l pl.UTF-8
Plik nagłówkowy dla rozszerzeń w C wykorzystujących moduł zope.proxy.

%package apidocs
Summary:	API documentation for Python zope.proxy module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.proxy
Group:		Documentation

%description apidocs
API documentation for Python zope.proxy module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.proxy.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/zope/proxy/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/zope/proxy/tests
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zope/proxy/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zope/proxy/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py_sitedir}/zope/proxy
%{py_sitedir}/zope/proxy/*.py[co]
%attr(755,root,root) %{py_sitedir}/zope/proxy/_zope_proxy_proxy.so
%{py_sitedir}/zope.proxy-%{version}-py*.egg-info
%{py_sitedir}/zope.proxy-%{version}-py*-nspkg.pth

%files devel
%defattr(644,root,root,755)
%{py_incdir}/zope.proxy
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py3_sitedir}/zope/proxy
%{py3_sitedir}/zope/proxy/*.py
%{py3_sitedir}/zope/proxy/__pycache__
%attr(755,root,root) %{py3_sitedir}/zope/proxy/_zope_proxy_proxy.cpython-*.so
%{py3_sitedir}/zope.proxy-%{version}-py*.egg-info
%{py3_sitedir}/zope.proxy-%{version}-py*-nspkg.pth

%files -n python3-%{module}-devel
%defattr(644,root,root,755)
%{py3_incdir}/zope.proxy
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
