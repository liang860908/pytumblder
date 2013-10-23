#!/bin/sh
for i in downloads/*
do
    if [ -d $i ]; then
        tumblr=$(echo $i|sed 's/^downloads\///g')
        python run.py -f $i -b http://${tumblr}.tumblr.com $*
    fi
done
