# Common Git Commands

*Update on 06/08/2018*

Tags: Github

+ **Author: Yunqiu Xu**

---
## 1. Set Your Profile
+ `git config --global user.name "Yunqiu Xu"`
+ `git config --global user.email "your email"`
+ `git config --list`
+ `exit`

## 2. Set Your Repository
+ `pwd` show your current position
+ `cd /xyq/` switch to given position
+ `ls` list the files in this position
+ `touch fileName` create a empty file here
+ `mkdir xyq` create a folder here
+ `git init` initialize this folder as a git repository

## 3. Check the Status of Git Repository
+ This repository should be a "git repository" (using `git init`)
+ `git status` check the status
+ `git diff` check the differences

## 4. Commit Your Changes
+ `git add xyq.py` add your file to the cache
    + `git add .` add all the files in this repository
+ `git rm -cached` remove the files in the cache
+ `git commit -m 'your comment'`
+ `git log` check the commit history
+ `git reset --hard HEAD^` go back to previous version
    + `git reset --hard HEAD` current version
    + `git reset --hard HEAD^^` second last version
    + `git reset --hard HEAD^^^` third last version

+ A simple example:
```shell
git add xxx.py
git commit -m 'this it my submission'
git push origin master
```
    
## 5. Connect to Github
+ `ssh-keygen -t rsa` generate the SSH key
+ `cd ~/.ssh`
+ `cat id_rsa.pub` check the SSH key
+ Github -- Settings -- SSH and GPG keys -- New SSH Key -- Add your SSH key here
+ `ssh -T git@github.com` check whether SSH is added successfully

## 6. Clone the Repository
+ `git clone git@github.com:YunqiuXu/my_notes.git`
+ Then you can make some changes and push it back to Github

## 7. Push Your Files to Github
+ Create an empty repository on Github, whose name is same to your local repository
+ `git pull origin master` if the remote repository is not empty, you'd better to pull it to local first
+ `git push -u origin master` push the committed files to Github

## 8. Get Latest Changes
+ `git fetch origin master:temp` get remote branch and set its name as "temp"
+ `git diff temp` check the differences between "temp" and your local repository
+ `git merge` merge these branches
    + If there are changes that you want to keep, use `git commit` to commit them
+ Another method can be `git pull`, which is equal to `git fetch + git merge`

## 9. Branch Operations
+ `git branch` check current branches
+ `git branch xyq` create a new branch
+ `git checkout xyq` switch to another branch
+ `git branch -d xyq` delete branch
+ `git merge` merge the branches
