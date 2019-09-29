#!/bin/bash
set -e
set -x
mdbook build 
cd book
git init .
git add .
git commit -m "publish book"
git remote add origin git@github.com:xieyu/blog.git
git push -f origin master:gh-pages
