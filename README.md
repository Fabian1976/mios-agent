# mios-agent (UNDER CONSTRUCTION)
I'm still migrating from a different repository. So it is still incomplete.

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

PostgreSQL:
- Auto discovery of databases

To get these features to work, you will need the Zabbix templates (will be included in this repository soon!)
