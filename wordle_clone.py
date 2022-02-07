import random

def run_wordle():
    print("Welcome to Wordle!\n")
    print("Guess the word, you have 6 tries.")
    print("\nHere are the rules:\n")
    print("For a matching letter in the right position, X will be used.")
    print("For a matching letter in the wrong position, O will be used.")
    print("For a wrong letter, F will be used.")
    
    tries = 0
    match = False
    answer = gen_word(words)
    print("DEBUG: %s" % encrypt(answer))
    
    while fail_condition(tries, match) == False:
        while True: #implement do-while loop
            print("Take a guess! Your word must be exactly 5 letters in length!")
            word_guess = input("What's the word? Input it here: _____ ")
            if len(word_guess) == 5:
                break
        
        attempt = guess(word_guess, answer)
        tries += 1
        
        print(attempt)
        if attempt == "XXXXX":
            match = True
            print("\n\nCongrats, you did it in %d attempt(s)!\n\n" % tries)
            return 
        
            
        
    print("\n\n You've used up all 6 guesses. Better luck next time!\n\n")
    return

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
        

def gen_word(word_list):
    
    rand_num = random.randint(0, len(word_list)-1)
    return word_list[rand_num]

def fail_condition(tries, match):
    #Only fail when 6 guesses are made and none are matching
    if tries == 6 and not match:
        return True
    return False

def encrypt(word): #Use this to debug without giving away the answer
    new_word = ""
    
    for s in word:
        new_word += str(ord(s)-96)
        
    return new_word

if __name__ == "__main__":
    f = open("sgb-words.txt")
    words = f.read()
    words = words.split("\n")
    
    run_wordle()
    