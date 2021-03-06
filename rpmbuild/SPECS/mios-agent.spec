Name:		mios-agent
Version:        4.3
Release:	2
Group:		None
Summary:	A python program which is used for Zabbix monitoring software with improved capability in stead of zabbix-agent
Group:		MIOS-utils
License:	GPLv2+
URL:		http://www.vermont24-7.com

#Requires:	python-json
Requires(pre):	shadow-utils
BuildRoot:	%{_topdir}/BUILD/%{name}-%{version}
%define _rpmfilename %%{NAME}-%%{VERSION}.%%{ARCH}.rpm
%define _unpackaged_files_terminate_build 0

%description
This python program is a proxy between the Zabbix server and Zabbix agent. It provides improved connectivity to
Oracle databases and Postgres databases.

%pre
/usr/bin/getent group mios > /dev/null || /usr/sbin/groupadd -g 400 mios
/usr/bin/getent passwd mios > /dev/null || /usr/sbin/useradd -g mios -d /opt/mios -s /bin/bash -m mios

%build


%install
mkdir -p %{buildroot}/opt/mios/mios-agent/bin/
mkdir -p %{buildroot}/opt/mios/mios-agent/conf/
mkdir -p %{buildroot}/opt/mios/mios-agent/init.d/
mkdir -p %{buildroot}/opt/mios/mios-agent/lib/psycopg2/
mkdir -p %{buildroot}/opt/mios/mios-agent/lib/simplejson/
mkdir -p %{buildroot}/opt/mios/mios-agent/probes/
mkdir -p %{buildroot}/usr/local/bin/
cp /opt/mios/mios-agent/bin/mios-agent %{buildroot}/opt/mios/mios-agent/bin/
cp /opt/mios/mios-agent/conf/logging.conf.example %{buildroot}/opt/mios/mios-agent/conf/
cp /opt/mios/mios-agent/conf/mios-agent.conf.example %{buildroot}/opt/mios/mios-agent/conf/
cp /opt/mios/mios-agent/init.d/mios-agent %{buildroot}/opt/mios/mios-agent/init.d/
cp /opt/mios/mios-agent/lib/daemon.py %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/lib/cx_Oracle_el5.so %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/lib/cx_Oracle_el6.so %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/lib/cx_Oracle_el7.so %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/lib/cloghandler.py %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/lib/portalocker.py %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/probes/* %{buildroot}/opt/mios/mios-agent/probes/
cp /usr/local/bin/magentlog %{buildroot}/usr/local/bin/
cp /opt/mios/mios-agent/lib/simplejson/* %{buildroot}/opt/mios/mios-agent/lib/simplejson/
cp /opt/mios/mios-agent/lib/psycopg2/* %{buildroot}/opt/mios/mios-agent/lib/psycopg2/

%clean
rm -rf %{buildroot}


%files
/opt/mios/mios-agent/bin/mios-agent
/opt/mios/mios-agent/conf/logging.conf.example
/opt/mios/mios-agent/conf/mios-agent.conf.example
/opt/mios/mios-agent/init.d/mios-agent
/opt/mios/mios-agent/lib/daemon.py
/opt/mios/mios-agent/lib/cx_Oracle_el5.so
/opt/mios/mios-agent/lib/cx_Oracle_el6.so
/opt/mios/mios-agent/lib/cx_Oracle_el7.so
/opt/mios/mios-agent/lib/cloghandler.py
/opt/mios/mios-agent/lib/portalocker.py
/opt/mios/mios-agent/probes/*
/usr/local/bin/magentlog
/opt/mios/mios-agent/lib/simplejson/*
/opt/mios/mios-agent/lib/psycopg2/*

%post
ln -s /opt/mios/mios-agent/init.d/mios-agent /etc/init.d/mios-agent
mkdir -p -m 775 /var/log/mios
mkdir -p -m 770 /var/run/mios
chown -R mios:mios /opt/mios
chown mios:mios /var/log/mios
chown mios:mios /var/run/mios
chmod -R 770 /opt/mios
chown mios:mios /usr/local/bin/magentlog
chmod 775 /usr/local/bin/magentlog

/sbin/chkconfig --add mios-agent

echo "export MAGENT_HOME=/opt/mios/mios-agent" >> /opt/mios/.bash_profile
echo "#export ORACLE_BASE=/opt/oracle" >> /opt/mios/.bash_profile
echo "#export ORACLE_VERSION=11.2.0.3" >> /opt/mios/.bash_profile
echo "#export ORACLE_HOME=\$ORACLE_BASE/product/\$ORACLE_VERSION/db" >> /opt/mios/.bash_profile
echo "#export ORACLE_SID=DBNAAM" >> /opt/mios/.bash_profile
echo "#export LD_LIBRARY_PATH=\$ORACLE_HOME/lib" >> /opt/mios/.bash_profile
echo -e "\nPlease set the ORACLE environment if you wish to monitor an Oracle database in /opt/mios/.bash_profile."
echo -e "Also make sure user mios can read the \$ORACLE_HOME/lib folder.\n"
echo -e "Create /opt/mios/mios-agent/conf/mios-agent.conf and logging.conf based on the exmaples in the same folder. Then start the agent as follows:"
echo -e "    /etc/init.d/mios-agent start\n"
echo -e "The mios-agent service had been added to chkconfig so it will autostart at future reboots.\n"
echo -e "The log can be viewed with the command \"magentlog\""
echo ""

%preun
[ -f /var/run/mios/mios-agent.pid ] && /etc/init.d/mios-agent stop
/sbin/chkconfig --del mios-agent

%postun
rm -f /etc/init.d/mios-agent
rm -rf /opt/mios/mios-agent
#check of er meerdere MIOS producten geinstalleerd zijn
aantal_mios=`find /opt/mios/ -type d | wc -l`
if [ "$aantal_mios" -eq "1" ]; then
	# Niet meer MIOS producten dus de MIOS map en user mag weg
	rm -rf /opt/mios
	/usr/sbin/userdel -fr mios
fi
rm -f /usr/local/bin/magentlog

%changelog
* Tue Nov 08 2016 Vermont 24-7 <support@vermont24-7.com> 4.3
- Made triggers in templates better readable
- Fixed ASM diskgroup monitoring
- Updated some templates
- Removed distribution code from rpm spec
* Thu Sep 17 2015 Vermont 24-7 <support@vermont24-7.com> 4.2
- Added additional library's
* Tue Oct 08 2013 Vermont 24-7 <support@vermont24-7.com> 1.0
- Initial RPM release
