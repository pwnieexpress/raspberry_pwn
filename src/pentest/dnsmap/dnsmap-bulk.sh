#!/bin/bash
if [[ $# -ne 1 && $# -ne 2 ]]
then
	echo "usage: `basename $0` <domains-file> [results-path]";
	echo "e.g.:";
	echo "`basename $0` domains.txt";
	echo "`basename $0` domains.txt /tmp/";
	exit
fi
for i in `cat $1`
do
	if [[ $# -eq 1 ]] 
	then	
		dnsmap $i
	elif [[ $# -eq 2 ]]
	then
		dnsmap $i -r $2
	fi
done		
