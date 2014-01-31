Name:		mios-agent
Version:        3.5
Release:	1%{?dist}
Summary:	A python program which is used for Zabbix monitoring software with improved capability in stead of zabbix-agent

License:	GPLv2+
URL:		http://www.vermont24-7.com

Requires:	python2-devel
Requires(pre):	shadow-utils
BuildRoot:	%{_topdir}/BUILD/%{name}-%{version}-%{release}-root

%description
This python program is a proxy between the Zabbix server and Zabbix agent. It provides improved connectivity to
Oracle databases and Postgres databases.

%pre
/usr/bin/getent group vermont > /dev/null || /usr/sbin/groupadd -g 400 vermont
/usr/bin/getent passwd mios > /dev/null || /usr/sbin/useradd -g mios -d /home/mios -s /bin/bash -m mios

%build


%install
mkdir -p %{buildroot}/opt/mios/mios-agent/bin/
mkdir -p %{buildroot}/opt/mios/mios-agent/conf/
mkdir -p %{buildroot}/opt/mios/mios-agent/init.d/
mkdir -p %{buildroot}/opt/mios/mios-agent/lib/
mkdir -p %{buildroot}/opt/mios/mios-agent/probes/
mkdir -p %{buildroot}/usr/local/bin/
cp /opt/mios/mios-agent/bin/mios-agent %{buildroot}/opt/mios/mios-agent/bin/
cp /opt/mios/mios-agent/conf/logging.conf %{buildroot}/opt/mios/mios-agent/conf/
cp /opt/mios/mios-agent/conf/mios-agent.conf %{buildroot}/opt/mios/mios-agent/conf/
cp /opt/mios/mios-agent/init.d/mios-agent %{buildroot}/opt/mios/mios-agent/init.d/
cp /opt/mios/mios-agent/lib/daemon.pyc %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/lib/cx_Oracle.so %{buildroot}/opt/mios/mios-agent/lib/
cp /opt/mios/mios-agent/probes/* %{buildroot}/opt/mios/mios-agent/probes/
cp /usr/local/bin/magentlog %{buildroot}/usr/local/bin/

%clean
rm -rf %{buildroot}


%files
/opt/mios/mios-agent/bin/mios-agent
/opt/mios/mios-agent/conf/logging.conf
/opt/mios/mios-agent/conf/mios-agent.conf
/opt/mios/mios-agent/init.d/mios-agent
/opt/mios/mios-agent/lib/daemon.pyc
/opt/mios/mios-agent/lib/cx_Oracle.so
/opt/mios/mios-agent/probes/*
/usr/local/bin/magentlog

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

echo "export MAGENT_HOME=/opt/mios/mios-agent" >> /home/mios/.bash_profile
echo "#export ORACLE_BASE=/opt/oracle" >> /home/mios/.bash_profile
echo "#export ORACLE_VERSION=11.2.0.3" >> /home/mios/.bash_profile
echo "#export ORACLE_HOME=\$ORACLE_BASE/product/\$ORACLE_VERSION/db" >> /home/mios/.bash_profile
echo "#export ORACLE_SID=DBNAAM" >> /home/mios/.bash_profile
echo "#export LD_LIBRARY_PATH=\$ORACLE_HOME/lib" >> /home/mios/.bash_profile
echo -e "\nPlease set the ORACLE environment if you wish to monitor an Oracle database in /home/mios/.bash_profile\n"
echo -e "Make the appropiate changes in /opt/mios/mios-agent/conf/mios-agent.conf and then start the agent as follows:"
echo -e "    /etc/init.d/mios-agent start\n"
echo -e "The mios-agent service had been added to chkconfig so it will autostart at future reboots.\n"
echo -e "The log can be views with the command \"magentlog\""

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
* Tue Oct 08 2013 Vermont 24-7 <support@vermont24-7.com> %{version}-%{release}
- Initial RPM release
