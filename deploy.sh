#!/bin/bash

/home/claudio/Enviroments/portfolio/bin/python3.6 /home/claudio/PycharmProjects/claudiopastorini.github.io/site.py build
git add * 
git commit -m "Update site"
git subtree split --prefix dist -b master
git push
git push -f origin master:master
