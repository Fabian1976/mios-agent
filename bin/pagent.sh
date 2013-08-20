set -x
export PYTHONPATH=/usr/lib64/python2.6/site-packages
export PAGENT_HOME=/home/mios/pagent
export LOGFILE=${PAGENT_HOME}/log/pagent.log
# Load Oracle environment
source /home/oracle/.bash_profile

EPOC=`perl -e 'print time();'`
/home/mios/pagent/bin/pagent -c ${PAGENT_HOME}/etc/pagent.ini >>${LOGFILE} 2>&1

while :
do
    if /sbin/pidof -x ${PAGENT_HOME}/bin/pagent >&- 2>&-
    then
        sleep 60
        continue
    fi
    EPOC2=`perl -e 'print time();'`
    DIFF=`expr $EPOC2 - $EPOC`
    if test $DIFF -gt 60
    then
        echo "`date` restart pagent" >>$LOGFILE
        EPOC=`perl -e 'print time();'`
        ${PAGENT_HOME}/bin/pagent -c ${PAGENT_HOME}/etc/pagent.ini
        sleep 3
    else
        echo "`date` no restart pagent" >>$LOGFILE
        exit 1
    fi
done
