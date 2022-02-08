"""
Runs GAC wordle on all 2000 words.
Returns average guess score.

"""
from wordle_clone import *
from GAC_solver import *

def run_wordle(answer, words):
    
    tries = 0
    match = False
    word_list = words
    
    while match == False:
        if tries == 0:     
            #Arise for interlink, Alert for gen_word
            word_guess = "crane" #skip compute for first step
        else:
            #word_guess = interlink(word_list)
            word_guess = gen_word(word_list)
        
        attempt = guess(word_guess, answer)
        tries += 1
        
        if attempt == "XXXXX":
            match = True
            
        else:
            word_list = analyze(word_guess, attempt, word_list)
        
    return tries

if __name__ == "__main__":
    f = open("sgb-words.txt")
    words = f.read()
    words = words.split("\n")
    
    total_guesses = 0
    
    for w in words:
        total_guesses += run_wordle(w, words)
    
    avg_guesses = total_guesses / len(words)
    print(avg_guesses)
    
