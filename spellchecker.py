from fileinput import close
from itertools import chain 
import nltk
import re
import numpy
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize, punkt, PunktSentenceTokenizer, RegexpTokenizer

#Define functions to use for Levenshtein Distance (Logic from: https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/)
def printDistances(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()
        
def ldMatrix(token1, token2):
    distances = distances = numpy.zeros((len(token1) + 1, len(token2) + 1))
    
    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1
    
    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if(token1[t1 - 1] == token2[t2 - 1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    #printDistances(distances, len(token1), len(token2)) #Does output distances
    
    return distances[len(token1)][len(token2)]

def calcDictDistance(word, numWords):
    f = open("C:/Users/Ally Thach/Documents/mobydick.txt", "r")
    l = f.readlines()
    f.close()
    
    dictWordDist = []
    wordIndex = 0
    
    #NOTE: the code below is to convert list -> str
    lNew = ' '.join(l)
    
    for line in lNew:
        wordDistance = ldMatrix(word, lNew.strip())
        if wordDistance >= 10:
            wordDistance = 9
        dictWordDist.append(str(int(wordDistance)) + "-" + lNew.strip())
        wordIndex = wordIndex + 1
        
    closestWords = []
    wordDetails = []
    currWordDist = 0
    dictWordDist.sort()
    print(dictWordDist)
    
    for i in range(numWords):
        currWordDist = dictWordDist[i]
        wordDetails = currWordDist.split("-")
        closestWords.append(wordDetails[1])
    return closestWords

#Opens mobydick.txt, reads file and removes any trailing white space
with open("C:/Users/Ally Thach/Documents/mobydick.txt", "r") as file:
    data = file.read().rstrip()
    
#print(data)

#Using the NLTK, tokenizes the data; puts all the words into a list
tokens = word_tokenize(data)
#print(tokens)
#print(type(tokens)) #type class list

#Using RegexpTokenizer, gets rid of all punctuation
newTokens = nltk.RegexpTokenizer(r"\w+")
newData = newTokens.tokenize(data)
#print(newData)

#Opens large.txt, reads file and removes any trailing white space; A dictionary of words found at https://phillipmfeldman.org/English/spelling%20dictionaries.html
with open("C:/Users/Ally Thach/Documents/large.txt", "r") as dictionary:
    dictData = dictionary.read().rstrip()
    
#print(dictData)
#print(type(dictData)) #type class str

#Creates an array for misspelled words (AKA words not in the dictionary) to be stored in
misspelledWords = []

#For every word in newData, checks it with the words in the dictionary. If the word does not exist in the dictionary, adds it to the array of misspelled words. 
for word in newData:
    if word not in dictData:
        misspelledWords.append(word)
        
#print(misspelledWords)
#print(type(misspelledWords)) #type class list
#print(len(misspelledWords))

#Note: the code below is to convert list -> str
newMisspelledWords = ' '.join(misspelledWords)
#print(newMisspelledWords)
#print(type(newMisspelledWords)) #type class str

#Loops through every word in newMisspelledWords and calculates the LD + recommends two "correct" words
for x in newMisspelledWords:
    print("I am entering the newMisspelledWords loop\n")
    print(x + " : " + calcDictDistance(x, 2))
    #print(calcDictDistance(y, 1))
    print("I have finished calculating distances for one word")
    print("\n")



