#!/bin/bash

git add .
git commit -m \"$@\"
git push
git push heroku main
exit 0
