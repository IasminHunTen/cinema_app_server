#!/bin/bash

if test $# -eq 0
then
	echo "missing commit messge"
	exit 1
fi

git add .
git commit -m \"$@\"
git push
git push heroku main
exit 0
