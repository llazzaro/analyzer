# install python client for hbase thrift #
HBase provide REST, Thrift and Avro web interface. There is no existing REST project for HBase. Avro has installation issue on mac, so the only choice is Thrift.


# Details #
Though a lot of people refer to some complicated ways, there is a simplest way which no one documents but already exits.... which will install hbase-thrift and thrift python module.

Open your shell, and type:
```
sudo easy_install hbase-thrift
```

Demo can be found at:
http://svn.apache.org/repos/asf/hbase/trunk/src/examples/thrift/DemoClient.py

# Relative Links #
http://www.hadoopor.com/viewthread.php?tid=1965

http://ofps.oreilly.com/titles/9781449396107/clients.html#clientsrest