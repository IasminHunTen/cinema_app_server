#!/bin/bash

if test $# -ne 1
then
	echo "expect a single argument, namely a string for the commit message"
	exit 1
fi

git add .
git commit -m \"$1\"
git push
git push heroku main
exit 0
