#!/bin/bash

#below script gives hostnames in a /24 subnet

echo Enter network address:
read net_add

for i in {1..254}
do
	echo $net_add.$i
	nslookup$net_add.$i
done