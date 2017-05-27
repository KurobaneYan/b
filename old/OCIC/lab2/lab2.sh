#!/bin/bash
#echo $(ps axu | grep $1)
$(ps axu | grep $1 | awk '$11 == "bash" {print "kill " $2}') 
