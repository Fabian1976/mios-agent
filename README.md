# MIOS-agent

The MIOS-agent is mainly an addition to the Zabbix-agent and functions as a proxy between the Zabbix-server and agent. It's primary goal is to provide connection pooling to several database backends.

It can monitor Oracle, PostgreSQL and mongo databases
It has featured such as:

Oracle:
- Auto discovery of Oracle SID's
- Auto discovery of Oracle tablespaces
- Auto discovery of Oracle temporary tablespaces
- Auto discovery of ASM diskgroups
- Auto discovery of ASM disks
- Auto discovery of Advanced Queuing
- Monitoring of cache hitratio's
- PGA/SGA monitoring
- Flash recovery monitoring
- Process and session monitoring
- sysstat monitoring (physical and logical reads/writes)
- Lock monitoring
- Redolog switch monitoring
- dbconsole look-a-like screen

PostgreSQL:
- Auto discovery of databases
- Sessions monitoring
- DML monitoring
- Lock monitoring
- Replication status monitoring
- Cache hitratio monitoring

## Installation
There are several ways to install this. Install it on the DB node where a zabbix-agent is allready present.

### Building the RPM
You can clone this repo:
```
git clone https://github.com/Fabian1976/mios-agent.git
```
Build the RPM (see dir rpmbuild for SPEC file)
and install the RPM on a Oracle server where a zabbix-agent is allready present.

Modify these parameters in /etc/zabbix/zabbix/zabbix_agentd.conf:
```
Server=127.0.0.1

ListenPort=10051
```

Check the .bash_profile in the home folder of the MIOS user and make sure the Oracle environment is correct. Also make sure the mios user has read access to the Oracle lib folder (using setfacl or adding the MIOS user to oinstall group).

Go to the mios-agent/conf folder and modify the mios-agent.conf file to match your environment.
Make sure the zabbix_agent in the common section is set to 127.0.0.1

Change the db section [oracle.*] of [postgres.*]

The * should be replaced by the SID you want to monitor for Oracle database and the dbname for PostgreSQL databases.

Oracle example:
```
[oracle.el5test]
user     = mios
password = m0n1t0R
host     = tverdbo02.vermont24-7.com
port     = 1521
service  = el5test.vermont24-7.com
oa_dir   = /opt/oracle/admin
```

PostgreSQL example:
```
[postgres.postgres]
host            = 10.10.3.8
port            = 5432
user            = postgres
password        = postgres

[postgres.confluence]
host            = 10.10.3.8
port            = 5432
user            = confluence
password        = confluence
```

The SID and dbname in the conf file are used for the auto discovery feature.

For Oracle you need to create a DB user which has access to the dictionaries:
```
create user mios identified by m0n1t0R default tablespace users account unlock;
grant connect to mios;
grant resource to mios;
grant create session to mios;
grant select any dictionary to mios;
```

You can grant select access to any other table you wish to use in you monitoring.

Now you can start the mios-agent (don't forget to restart the zabbix-agent first because we have changed the listen port and server ip) as follows:
```
/etc/init.d/mios-agent start
```
You can view the log in /var/log/mios/mios-agent.log (or use the command magentlog). stdout and stderr are written to /tmp/mios-agent.stdout(err)

### Manual installation

Or you can install everything manually like follows:
- Create a user called mios with it's home folder set to "/opt/mios"
- Change to that user, stay in the home folder and type:
```
git clone https://github.com/Fabian1976/mios-agent.git
```
- Modify the .bash_profile in it's home folder and add the following contents:
```
#MIOS-AGENT environment
export MAGENT_HOME=/opt/mios/mios-agent
#Oracle environment
export ORACLE_BASE=/opt/oracle
export ORACLE_VERSION=11.2.0.4
export ORACLE_HOME=$ORACLE_BASE/product/$ORACLE_VERSION/db
export LD_LIBRARY_PATH=$ORACLE_HOME/lib
```

Create a symlink to start it using /etc/init.d:
```
ln -s /opt/mios/mios-agent/init.d/mios-agent /etc/init.d/mios-agent
```

Create the file /usr/local/bin/magentlog with the following content:
```
less +F /var/log/mios/mios-agent.log
```

Modify these parameters in /etc/zabbix/zabbix/zabbix_agentd.conf:
```
Server=127.0.0.1

ListenPort=10051
```

Go to the mios-agent/conf folder and modify the mios-agent.conf file to match your environment.
Make sure the zabbix_agent in the common section is set to 127.0.0.1

Change the db section [oracle.*] of [postgres.*]

The * should be replaced by the SID you want to monitor for Oracle database and the dbname for PostgreSQL databases.

Oracle example:
```
[oracle.el5test]
user     = mios
password = m0n1t0R
host     = tverdbo02.vermont24-7.com
port     = 1521
service  = el5test.vermont24-7.com
oa_dir   = /opt/oracle/admin
```

PostgreSQL example:
```
[postgres.postgres]
host            = 10.10.3.8
port            = 5432
user            = postgres
password        = postgres

[postgres.confluence]
host            = 10.10.3.8
port            = 5432
user            = confluence
password        = confluence
```

The SID and dbname in the conf file are used for the auto discovery feature.

For Oracle you need to create a DB user which has access to the dictionaries:
```
create user mios identified by m0n1t0R default tablespace users account unlock;
grant connect to mios;
grant resource to mios;
grant create session to mios;
grant select any dictionary to mios;
```

You can grant select access to any other table you wish to use in you monitoring.

Now you can start the mios-agent (don't forget to restart the zabbix-agent first because we have changed the listen port and server ip) as follows:
```
/etc/init.d/mios-agent start
```
You can view the log in /var/log/mios/mios-agent.log (or use the command magentlog). stdout and stderr are written to /tmp/mios-agent.stdout(err)

## Using the templates
The templates used by Zabbix are in the templates folder of this repo (who would of thought).

Import these template on the Zabbix-server. First import the Oracle.xml of Postgres.xml template, and then the Oracle SID discovery.xml and Postgres DB discovery.xml templates.

Assign the Oracle SID discovery template to the host on which the mios-agent was installed, and wait for the auto-discovery to complete (usualy within the hour).

## How does the mios-agent work
When you add the SID discovery template to a host, it will sent this request to the agent:
```
oracle.sid_discover
```

This will return the SID's which you defined in the agent conf file and create host's with the SID as host name and "{#SIDNAME} on {#FQDN}" as visible name. It will also link the Oracle template to this new host.

The agent used pre-configured query's in the probes folder of the agent. The name of the probe, matches the name of the Zabbix key. So in the Oracle template a key will look like this:
```
oracle.librarycache_hitratio_total[{HOSTNAME},]
```
As you can see, the hostname is sent to the agent so that it knows (based on the agent conf) which SID to query. The second parameter is empty in this example. The second parameter can be used to sent a variable to a probe (query). I will adress the second parameter later on.

The Oracle template has several auto discovery rules. ASM and Advanced Queuing rules are disabled by default. The tablespace and tempspace discovery are enabled by default.

The tablespace discovery rule sents this to the agent:
```
oracle.tablespace_discover[{HOSTNAME}]
```

The agent will return the tablespaces it can find and assign them to TBSNAME variable in Zabbix.
Several items are created for each tablespace found:
```
oracle.tablespace_allocated_size[{HOSTNAME},{#TBSNAME}]
oracle.tablespace_max_size[{HOSTNAME},{#TBSNAME}]
oracle.tablespace_used_size[{HOSTNAME},{#TBSNAME}]
```
As you can see, the second parameter is used to sent the tablespace name. If we look at 1 of the probe files for tablespace monitoring, it will look like this:
```
type=oracle
select sum(bytes) from dba_data_files where tablespace_name = 'MIOS_ARG_2'
```
The MIOS_ARG_2 part will be replaced by the second parameter of the zabbix key.

You can also build custom probes for your own tables like this.

There is also a file called sync_probes in the probes folder. This can be used to sync probes from a different server to the Oracle server.

## Todo:
Make the mios-agent more efficient. An example:
To monitor a tablespace, the agent now uses 3 querys per tablespace. In the future this will be 1 query to gather all info. This will be modified in the agent. No template modification will be necessary. The same goes for the ASM monitoring.
