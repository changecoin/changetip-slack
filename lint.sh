#!/bin/bash
for f in `find ./ -name '*py' | grep -v migrations | grep -v test | grep -v __init__ | grep -v settings.py`; do
    pyflakes $f
    if [ "$?" != "0" ] ; then
        echo "$f does not pass lint check"
        exit 1
    fi
done
exit 0
