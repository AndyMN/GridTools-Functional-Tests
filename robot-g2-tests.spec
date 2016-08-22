Summary: The robot-G2 functional test suite
Name: robot-g2
Group: Development/Tools
Version: 1.0
Release: 1
License: GPL
Source: https://github.com/AndyMN/robot-g2-tests/archive/master.zip
URL: https://github.com/AndyMN/robot-g2-tests.git
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Requires: python >= 2.7
Requires: dcache-srmclient
Requires: globus-gass-copy-progs
Requires: nordugrid-arc-client



%description
The G2 suite provides a framework for testing a standards-compliant storage system by running applications
against it, along with a set of tests to verify the storage system works as expected.



%prep
rm -rf $RPM_BUILD_ROOT/robot-g2*
rm -rf $RPM_BUILD_DIR/robot-g2*
rm -rf /scratch/jenkins/robotframework-g2*
wget -O $RPM_SOURCE_DIR/master.zip https://github.com/AndyMN/robot-g2-tests/archive/master/master.zip
unzip -o $RPM_SOURCE_DIR/master.zip -d /scratch/jenkins/
