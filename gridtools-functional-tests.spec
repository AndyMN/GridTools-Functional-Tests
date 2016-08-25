Summary: Functional Tests for Grid Tools
Name: GridTools-Functional-Tests
Group: Development/Tools
Version: 1.0
Release: 1
License: GPL
Source: https://github.com/AndyMN/GridTools-Functional-Tests/archive/master.zip
URL: https://github.com/AndyMN/GridTools-Functional-Tests.git
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Requires: python >= 2.7
Requires: dcache-srmclient
Requires: globus-gass-copy-progs
Requires: nordugrid-arc-client



%description
The GridTools functional test suite provides a framework for testing a standards-compliant storage system by running applications
against it, along with a set of tests to verify the storage system works as expected.



%prep
rm -rf $RPM_BUILD_ROOT/GridTools-Functional-Tests/
rm -rf $RPM_BUILD_DIR/GridTools-Functional-Tests/
wget -O $RPM_SOURCE_DIR/master.zip https://github.com/AndyMN/GridTools-Functional-Tests/archive/master/master.zip
unzip -o $RPM_SOURCE_DIR/master.zip -d ${RPM_BUILD_DIR}
