#
# This is template for pure python2/python3 modules (noarch)
# use template-specs/python3.spec for python3 only noarch packages
# use template-specs/python-ext.spec for binary python packages
#
#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

# NOTES:
# - 'module' should match the Python import path (first component?)
# - 'egg_name' should equal to Python egg name
# - 'pypi_name' must match the Python Package Index name
%define		module		LGTV
%define		egg_name	LGTV
%define		pypi_name	LGTV
Summary:	Command line webOS remote for LGTVs
Name:		python-LGWebOSRemote
Version:	0.2
Release:	0.1
License:	MIT
Group:		Libraries/Python
Source0:	https://github.com/klattimer/LGWebOSRemote/archive/master.zip
# Source0-md5:	95e4d2a8e3b94c1fc75a6534c6ac7749
URL:		https://github.com/klattimer/LGWebOSRemote
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
#BuildRequires:	python-
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Command line webOS remote for LGTVs. This tool uses a connection via
websockets to port 3000 on newer LG TVs.

%package -n python3-LGWebOSRemote
Summary:	Command line webOS remote for LGTVs
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-LGWebOSRemote
Command line webOS remote for LGTVs. This tool uses a connection via
websockets to port 3000 on newer LG TVs.

%prep
%setup -q -c
mv *-master/* .

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest ...
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest ...
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%if %{with enable_if_package_uses_non_standard_setup_py}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%endif

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

install -d $RPM_BUILD_ROOT%{_sysconfdir}/lgtv
mv $RPM_BUILD_ROOT/{usr/config,etc/lgtv}/config.json

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
#%dir %{_sysconfdir}/lgtv
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lgtv/config.json
%endif

%if %{with python3}
%files -n python3-LGWebOSRemote
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/lgtv
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%dir %{_sysconfdir}/lgtv
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lgtv/config.json
%endif
