#Oracle environment
export ORACLE_BASE=/opt/oracle
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0.3/db
export LD_LIBRARY_PATH=$ORACLE_HOME/lib

nohup /usr/bin/python ./pagent -c ../etc/pagent.ini --loglevel=DEBUG &
