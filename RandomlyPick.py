# !/usr/bin/env python
# coding: utf-8

# RandomlyPick
# Author : Yunqiu Xu
# Pick a candidate randomly

from random import randint

# create class Candidate to store the information of candidate
class Candidate(object):
    def __init__(self,name):
        self.name=name
        self.vote=0

# input the list of candidates, and the number of voters
# return the list where the votenumber of every candidates changes
def countVote(candidateList,voterNumber):
    for voter in range(voterNumber):
        vote=randint(0,len(candidateList)-1)
        candidateList[vote].vote += 1

# reset all the votes
def refresh(candidateList):
    for item in candidateList:
        item.vote=0


if __name__ =="__main__":
    # input all the candidates
    print "Enter all the candidates:"
    candidateList=[]
    while True:
        candidateName=raw_input("Candidate name: ")
        if not candidateName:
            print "Input end!"
            break
        candidateList.append(Candidate(candidateName))

    candidateNumber = int(raw_input("Enter the number of candidates you wanna choose: "))
    if candidateNumber == 0 or candidateNumber>len(candidateList):
        print "Wrong input, kidding me?"
        exit()

    voterNumber = int(raw_input("Enter the number of voters: "))
    while candidateNumber!=0:
        print "Now we pick a new candidate:"
        countVote(candidateList, voterNumber)
        print "The result is :"
        maxIndex=0
        for i in range(len(candidateList)):
            print "{} : {}".format(candidateList[i].name,candidateList[i].vote)
            if candidateList[i].vote>candidateList[maxIndex].vote:
                maxIndex=i
        print "So {}, you are the chosen one!".format(candidateList[maxIndex].name)
        candidateList.remove(candidateList[maxIndex])
        candidateNumber-=1
        refresh(candidateList)

    print "Finish!"
    exit()

