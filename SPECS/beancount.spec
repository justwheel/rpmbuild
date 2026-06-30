Name:           beancount
Version:        2.3.6
Release:        1%{?dist}
Summary:        Double-Entry Accounting from Text Files

License:        GPL-2.0-only
URL:            https://github.com/beancount/beancount
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

# Build time dependencies.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

# Run time dependencies.
Requires: python3-keyring
Requires: python3-distro
Requires: python3-jinja2
Requires: python3-pyxdg
Requires: python3-dbus
Requires: python3-systemd
Requires: python3-gobject

%global _description %{expand:
A double-entry bookkeeping computer language that lets you define financial transaction records in a text file, read them in memory, generate a variety of reports from them, and provides a web interface.}

%description %_description
A double-entry bookkeeping computer language that lets you define financial
transaction records in a text file, read them in memory, generate a variety of
reports from them, and provides a web interface.


%prep
%setup -n %{unmangled_name}-%{version} -n %{unmangled_name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES

%changelog
