#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (installed package required)

%define module	zope.proxy
Summary:	Mostly-transparent wrappers around another object
Summary(pl.UTF-8):	Prawie przezroczyste obudowywanie innych obiektów
Name:		python3-%{module}
Version:	6.1
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/z/zope.proxy/zope_proxy-%{version}.tar.gz
# Source0-md5:	6d6f76315521181046b1e52213b1d847
URL:		https://www.zope.dev/
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.security
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
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
Requires:	python3-devel >= 1:3.8

%description devel
Header file for C extensions using zope.proxy module.

%description devel -l pl.UTF-8
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
%setup -q -n zope_proxy-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zope/proxy/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zope/proxy/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py3_sitedir}/zope/proxy
%{py3_sitedir}/zope/proxy/*.py
%{py3_sitedir}/zope/proxy/__pycache__
%attr(755,root,root) %{py3_sitedir}/zope/proxy/_zope_proxy_proxy.cpython-*.so
%{py3_sitedir}/zope.proxy-%{version}-py*.egg-info
%{py3_sitedir}/zope.proxy-%{version}-py*-nspkg.pth

%files devel
%defattr(644,root,root,755)
%{py3_incdir}/zope.proxy

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
