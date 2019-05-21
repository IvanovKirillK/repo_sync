#!/usr/bin/env bash
cd $1
echo "###########################"
date
for remote in `git branch -r`; do git branch --track ${remote#origin/} $remote; done
echo "Fetching all"
git fetch --all
echo "Pulling all"
git pull --all
echo "Pushing all"
git push --all
