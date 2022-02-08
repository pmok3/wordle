# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def run_wordle_GAC(words):
    print("I'm going to try to guess your word.\n")
    
    i = 1
    
    while i <= 6:
        #guess = gen_word(words) #Word with most frequent letters
        guess = interlink(words) #Most interlinked word
        print("Guess: %s" % guess)
    
        result = input("How did I do? _ _ _ _ _")
        words = analyze(guess, result, words)
        print("Remaining words:")
        print(words)
        
        #Exit
        if len(words) == 1:
            break
        
        i += 1
    else:
        print("Failed!\n")
        return
    
    print("Success! Very Nice!\n")
    
def share(a, b):
    #Returns true if two words share one or more letters
    a_set = set(a)
    for i in range(len(b)):
        if b[i] in a_set:
            return True
        
    return False

def interlink(words):
    #Find the most interlinked word
    rank_dict = {}
    
    for i in range(len(words)):
        rank = 0
        
        for j in range(len(words)):
            if i != j:
                if share(words[i], words[j]) == True:
                    rank += 1
            rank_dict[words[i]] = rank
            
    #Take max
    max_val = -1
    max_word = ""
    
    for k in rank_dict.keys():
        rank = rank_dict[k]
        if rank > max_val:
            max_val = rank
            max_word = k
    
    return max_word
    
def gen_freq_table(words):
    #Creates a frequency table using the relative frequency of letters present
    #in the wordset. Akin to taking the greedy solution in a minimal spanning tree.
    
    freq_arr = [0]*26
    freq_table = {}
    
    for w in words:
        seen = set()
        for i in range(5):
            if i not in seen:
                freq_arr[ord(w[i])-97] += 1
                seen.add(i)
    
    total_letters = len(words)*5
    for i in range(26):
        freq_arr[i] /= total_letters
        
        #Convert to dict form
        freq_table[chr(i+65)] = freq_arr[i]*26
    
    return freq_table

def analyze(guess, result, words):
    new_words = words
    num_F = [0]*26
    
    for i in range(len(result)):
        if result[i].upper() == "X":
            new_words = position_include_prune(guess[i], i, new_words)
        elif result[i].upper() == "O":
            new_words = position_exclude_prune(guess[i], i, new_words)
        elif result[i].upper() == "F":
            failed_letter = ord(guess[i])-97
            new_words = prune(guess.count(guess[i])-num_F[failed_letter], guess[i], new_words)
            num_F[failed_letter] += 1
    
    return new_words

def gen_word(word_list):
    
    #Add a heuristic here
    max_score = -1
    max_word = ""
    freq_table = gen_freq_table(word_list)
    
    for i in range(len(word_list)):
        word = word_list[i]
        word_score = freq_score(word, freq_table)
        
        if word_score > max_score:
            max_score = word_score
            max_word = word
    
    return max_word

def freq_score(word, freq_table):
    score = 0
    seen = set()
    
    for w in word.upper():
        if w not in seen: 
            score += freq_table[w]
            seen.add(w)
        
    return score

def prune(n, letter, words):
    #Prunes all words with n number of letters and above.
    #For letters that don't match. For words with multiple letters, use a higher n.
    new_words = []
    
    for w in words:
        if w.count(letter) < n:
            new_words.append(w)
    return new_words

def position_exclude_prune(letter, position, words):
    #Prunes all words with letters in a certain position but are still contained.
    #For letters that match in the wrong position
    new_words = []
    
    for w in words:
        if letter != w[position] and letter in w:
            new_words.append(w)
    
    return new_words

def position_include_prune(letter, position, words):
    #Prunes all words with letters not in a certain position.
    #For letters that match and in the right position
    new_words = []
    
    for w in words:
        if letter == w[position]:
            new_words.append(w)
    
    return new_words

if __name__ == "__main__":
    f = open("sgb-words.txt")
    words = f.read()
    words = words.split("\n")
    
    run_wordle_GAC(words)
