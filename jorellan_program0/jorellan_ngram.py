#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:22:16 2018

@author: Jennifer
"""
import re 
from collections import Counter 
import random 
print('\n')

num_of_results = 100 #set how many results you want

#read and create a giant string
my_corpus = open("corpus.txt")
my_corpus = my_corpus.readlines()
my_corpus = ' '.join(my_corpus)

#remove non-letter characters
my_corpus = re.sub("[^a-zA-Z .!?']+", '', my_corpus)


#everything lowercase and remove whitespace 
my_corpus = my_corpus.lower()
my_corpus = my_corpus.strip()

#divide into words and remove empty strings
my_corpus = my_corpus.split(" ")
while '' in my_corpus:
    my_corpus.remove('')  

#--------------------------------------------------------------------------------#
#Build a Unigram Model
unigram = dict(Counter(my_corpus))

#Run unigram model
words_uni = list(unigram.keys()) #all the words in a list
nums_uni = list(unigram.values())  #the #of occurances in a list

#randomly choose the number of words you want and print them
result_uni = random.choices(words_uni, weights=nums_uni, cum_weights=None, k=num_of_results)
result_uni = ' '.join(result_uni)  #change from list to string

#Print the results
print("Unigram Model: ")
print(result_uni)
#print(unigram)
print('\n')

#--------------------------------------------------------------------------------#
#Build a Bigram Model
bigrams = {}
for i in range(len(my_corpus)-1):
    if my_corpus[i] in bigrams.keys(): #if the word is in the key of the 1st dictionary
      if my_corpus[i+1] in bigrams[my_corpus[i]].keys():#if the next word is in the key of the 2nd dictionary
          bigrams[my_corpus[i]][my_corpus[i+1]] = bigrams[my_corpus[i]][my_corpus[i+1]]+1 #add 1 more to the number
      else:
          bigrams[my_corpus[i]][my_corpus[i+1]] = 1 
          #if the word is in the key of the 1st dictionary but the next work is not in the key of the 2nd dictionary, add it with a value of 1
    else:
        bigrams[my_corpus[i]] = {my_corpus[i+1]:1}
        #if the word is not in the key of the 1st dictionary, add the word and the next word with a value of 1 

#Run bigram model
result_bi = [0]*num_of_results #create a list of zeros the length of the results you want

def second_word(next_word): #figure out what the next word is 
    if next_word in bigrams.keys(): #if the current word is in the key of the first dictionary
        choice = list(bigrams[next_word].keys()) #all the words in the second dictionary
        weight = list(bigrams[next_word].values()) #the #of time the pair occurs
        word = random.choices(choice, weights=weight, cum_weights=None, k=1)[0] #figure our the next word 
    else:
        word = random.choices(words_uni, weights=nums_uni)[0] #if not in the key of the first dictionary, get a random word form the unigram
    return word

current_word = random.choices(words_uni, weights=nums_uni)[0]  #start with a random word from the unigram
result_bi[0] = current_word #set the first word equal to the word you got from the bigram

#print the results 
print("Bigram Model Starting With The Word '" + current_word + "': ")
for i in range(1, len(result_bi)): #for the remaining words in the result_bi list
    current_word = second_word(current_word) #the current word is the result of second_word()
    result_bi[i] = current_word #the current word is added to the result_bi list

result_bi = ' '.join(result_bi)  #change from list to string
print(result_bi)
#print(bigrams)
print("\n")

#--------------------------------------------------------------------------------#
#Build a Trigram Model 
trigrams = {}
for i in range(len(my_corpus)-2): 
    if tuple(my_corpus[i:i+2]) in trigrams.keys(): #if the two word tuple in in the key of the first dictionary
      if my_corpus[i+2] in trigrams[tuple(my_corpus[i:i+2])].keys(): #if the next word in the keys of the second dictionary 
          trigrams[tuple(my_corpus[i:i+2])][my_corpus[i+2]] = trigrams[tuple(my_corpus[i:i+2])][my_corpus[i+2]]+1 #add 1 to the value of the second dictionary
      else:
          trigrams[tuple(my_corpus[i:i+2])][my_corpus[i+2]] = 1 
          #if the two word tuple is in the first dictionary, but the next word is not in the second dictionary, add the word third word to the dictionary with a value of 1
    else:
        trigrams[tuple(my_corpus[i:i+2])] = {my_corpus[i+2]:1}
        #if the two word tuple is not in the dictionary, add the tuple to the first dictionary and the thrid word with a value of 1 in the second dictionary
        
#Run trigram model
result_tri = [0]*num_of_results #create a list of zeros the length of the results you want

def third_word(nxt_word): #figure out what the next word is 
    if nxt_word in trigrams.keys(): #if the tuple is in the key of the first dictionary
        choice = list(trigrams[nxt_word].keys()) #all the words in the second dictionary
        weight = list(trigrams[nxt_word].values()) #the #of time the triples occurs
        word = random.choices(choice, weights=weight, cum_weights=None, k=1)[0] #figure out the next word
        word = (nxt_word[1], word) #create a tuple of the second and third word 
    else: #if the tuple is not in the key of the first dictionary
        word = second_word(nxt_word[1]) #find the next word based on the bigram
        word = (nxt_word[1], word) #create a tuple of the second and third word 
    return word 
 

one_word = random.choices(words_uni, weights=nums_uni)[0] #randomly choose the first word with from unigram
two_word = [one_word, 0] #create a list with the first word
two_word[1] = second_word(one_word) #randomly choose the second word with from bigram and add it to the list two_word
eval_word = tuple(two_word) #change the two first words to a tuple 

#print the results 
print("Trigram Model Starting With The Words '" + eval_word[0] +  " " + eval_word[1]+ "': ")
result_tri[0] = eval_word[0] #the first word is the result of the unigram
result_tri[1] = eval_word[1] #the second word is the result of the bigram
for i in range(2, len(result_tri)): #for the remaining words in the result_tri list
    eval_word = third_word(eval_word) #the evaluation words is the result of third_word()
    result_tri[i] = eval_word[1] #the last word returned is added to the result_tri list 

result_tri = ' '.join(result_tri)  #change from list to string
print(result_tri)
#print(trigrams)
