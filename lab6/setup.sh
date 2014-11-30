#!/bin/bash
cp -r cloudera/ $HOME/cloudera
cd $HOME/cloudera/cdh5.1/
curl -O http://archive.cloudera.com/cdh5/cdh/5/hadoop-2.3.0-cdh5.1.2.tar.gz
tar -xvf hadoop-2.3.0-cdh5.1.2.tar.gz
cd -
cp *.xml $HOME/cloudera/cdh5.1/hadoop-2.3.0-cdh5.1.2/etc/hadoop/
cp hadoop-env.sh $HOME/cloudera/cdh5.1/hadoop-2.3.0-cdh5.1.2/etc/hadoop/
chmod 755 ./start.sh

