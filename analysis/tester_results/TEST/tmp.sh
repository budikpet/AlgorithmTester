#!/bin/bash

tmp_file=".tmp"

for file in *.dat;
do
	sort -k1 -V $file > $tmp_file
	rm $file
	mv $tmp_file $file
done
