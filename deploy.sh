#!/bin/bash

/home/claudio/Enviroments/porfolio/bin/python /home/claudio/PycharmProjects/claudiopastorini.github.io/site.py build
git add * 
git commit -m "Update site"
git subtree split --prefix dist -b master
git push
git push -f origin master:master
