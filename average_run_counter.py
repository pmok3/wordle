"""
Runs GAC wordle on all 2000 words.
Returns average guess score.

"""

def run_wordle(answer, words):
    
    tries = 0
    match = False
    word_list = words
    
    while match == False:
        if tries == 0:     
            #Arise for interlink, Alert for gen_word
            word_guess = "arise" #skip compute for first step
        else:
            word_guess = interlink(word_list)
            #word_guess = gen_word(word_list)
        
        attempt = guess(word_guess, answer)
        tries += 1
        
        if attempt == "XXXXX":
            match = True
            
        else:
            word_list = analyze(word_guess, attempt, word_list)
        
    return tries

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

def guess(word, answer):
    
    ret_list = ["F","F","F","F","F"]
    answer_dict = {}

    #2 pass approach, O(n)
    #Add to dict
    for i in range(5):
        if answer[i] in answer_dict:
            answer_dict[answer[i]] += 1
        else:
            answer_dict[answer[i]] = 1
   
    #X pass
    for i in range(5):
        if word[i] == answer[i]:
            ret_list[i] = "X"
            answer_dict[word[i]] -= 1
    
    #O pass
    for i in range(5):
        if word[i] != answer[i] and word[i] in answer_dict and answer_dict[word[i]] > 0:
            answer_dict[word[i]] -= 1
            ret_list[i] = "O"
            
    return "".join(ret_list)

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

if __name__ == "__main__":
    f = open("sgb-words.txt")
    words = f.read()
    words = words.split("\n")
    
    total_guesses = 0
    
    for w in words:
        total_guesses += run_wordle(w, words)
    
    avg_guesses = total_guesses / len(words)
    print(avg_guesses)
    