# Wordle clone + solver + backtesting

I created something. 

Or rather, I found about this game last week and decided that one challenge a day wasn't going to cut it, and decided to make my own clone. After all, the rules seemed simple enough to implement. Following this, I figured I could make a solver using principles that I had learned in school, and had last touched in those very same courses. 

Here's how I did it.

# Wordle clone
The actual Wordle game is played directly in the console. For me, most of my development takes place in Anaconda's Spyder so that's exactly where I "played" Wordle. A bit lacking in the graphics department, I know. But it gets the job done.

Development of "the game" itself was quite simple, and the entire section of code where the actual "game" takes place is a simple while loop that makes sure you haven't guessed incorrectly 6 times.

The more complex part was in how the guesses were evaluated.

For reference, I use the following notation:
* X - Green - Correct letter, correct position
* O - Yellow - Correct letter, wrong position
* F - Black - Wrong letter

I started off by lazily comparing each letter in each word and comparing it to the other word. For a word with 5 letters, this meant running through 5 comparisons per letter, or 25 total computations.

Then, I decided to make it a little bit faster and stored the answer keyword in a hashset for constant time search. The issue now, was how do I make it a thorough check that encompasses all testcases? My current methodology was perfectly fine for words with distinct letters -- but what about words with less than 5 unique letters, such as "apple"? Or what about guesses with less than 5 unique letters?

Well, I noticed a few patterns emerge from Wordle:
* X always takes priority. That is to say, if the word you're looking for is "beach" and you guess "hatch", your result will be "FOFXX" -- indicating that the first "h" was a fail.
* You will know how many instances of a letter a word has. In essence, there is always some sort of 1 to 1 mapping of letters that allows logical deductions to be made. Like the example above, we can see that only one of the "h"'s was assigned a valid state.

With these in mind I implemented a two pass solution - one for the X's and one for the O's, in that order. Adjustments were made to accommodate words with less than 5 unique letters. Namely using a hashmap instead of a hashset, that also tracked letter count. Whenever a letter was encountered and processed, I would subtract it from the counter. This eliminated situations were letters were getting double counted, such as guessing "hatch" for "beach" -- without this fix, it would have been evaluated as "OOFXX".

Having a complete evaluation function in hand, it's safe to say that the wordle clone is complete. The remaining parts were word generation (I downloaded a dataset somewhere and randomly chose words from that set) and some print statements to make sure that everything was working smoothly. I also added in an encryption function that uses the mapping A -> 1, B -> 2 ... Z -> 26 to display the answer in debug situations but I've yet to use it thus far.

# Solver

At its core, the solver consists of a section that removes words, and a section that makes educated guesses. 
* Note that I didn't say adds words. This is because when starting, the program is given access to all words and must choose one to guess from that linguistic superset.

Removing words is fairly straight forward for the most part.
* For the X case, we iterate through the entire wordset and prune out words that don't have letters in the matching X position.
* For the O case, we iterate through the remaining wordset and prune out words that don't have letters in the O position, but have them in another position.
* For the F case, it gets a bit tricky. In the simple case where the guess has 5 unique letters, words that contain any F letters are pruned. 

In the more complicated case where the guess has less than 5 unique letters, we implement a letter counter and prune words with N counts of that letter and above. 

* For example, let's say that we're guessing "hatch" for the word "beach" and have received "FOFXX" as a result. In the simple F case, all words containing "h" would have been pruned from the set, which is problematic. The solution, therefore, is to recognize that the word "hatch" has two instances of the letter "h" using a counter, and now prune all words containing 2 or more "h"'s. This way we know that any remaining words have at least 1 "h", and after the X "h" pruning we know that the "h" is in its proper position.

This process of iterating through the intermediate X/O/F strings and trimming down the remaining feasible wordset is akin to the Generalized Arc Consistency algorithm I once learned about in CSC384.

For guessing, I approached it in two different ways, though there are many other valid methods to do so including linguistic analysis and so on, that I don't know about. I also mention the term "convergence" quite a fair bit in the following sections, so bear with me. All it really means is the iterative process of the guesser trimming down the wordset to a single remaining word, aka the solution.
### Frequency Table ###
https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html

Intuitively, one would expect the use of frequency tables to help guess words. After all, a word like "query" with the letters "q" and "y" is expected to appear less frequently than a word like "react". Well, Samuel Morse of the eponymous encoding protocol figured that out in the 19th Century, and procured a table for us to aid our guesses. 

One way of applying this knowledge is via a score sum, the word with the highest frequency score would be chosen to use as a guess. There was a problem, though: "eerie" was always the top word, presumably for its three "E"'s. From this, I incentivized the guesser to prioritize words with unique letters. This had two main purposes: to reduce redundancy of guesses, and to speed up convergence by introducing more consonants to the evaluator.

This idea evolved and eventually I turned to generating a frequency table using the existing wordset over applying Morse's code. I reasoned that because Morse's data was based off text he saw in his own time, his table would be better suited to words of his era. From here, creating a new frequency table from the existing wordset seemed to be the next logical step; as the guesser would have a better understanding of which words were more or less likely to appear and thus make a better informed decision from that data. For the standard wordset, this word was "alert". 

### Prim's Algorithm for generating Minimal Spanning Trees ###
https://en.wikipedia.org/wiki/Prim%27s_algorithm 

Here's some food for thought.

What if instead of words you were dealing with, you were dealing with a graph of nodes and edges? Each distinct word would represent a single node. And shared letters in any position would represent edges. So the words "brick" and "idler" would share an edge, but neither of the two would be connected with "jazzy". The result would be a dense graph, with each node having multiple edges. 

Prim's algorithm, for the uninitiated, is essentially a way to construct a fully connected set of nodes using the minimum edge weight possible. From this algorithm I had the idea of what if we were to do the opposite; to deconstruct a fully connected set of nodes in the least number of moves? Since we know that Prim's Algorithm is a greedy based solution, I reasoned that doing the converse to greedily obtain the quickest wordset convergence would be a viable approach.

To do so, I took the rank of each node, or how many edges each node possessed. An edge, defined as sharing 1 or more letter with another word.

The word with the highest rank among the dataset was chosen as the most likely guess, as in the absence of future knowledge one could reasonably expect the fastest convergence using this method. For the standard wordset, this word was "arise".

# Backtesting

Backtesting these strategies is fairly straightforward, and I've included some base code to do so. They run on the entire wordset, and can be optimized performance wise as seen fit. For my strategies, I skipped the first compute step completely as it was a redundant calculation yielding the same "ALERT" or "ARISE" for every word.

### Results ###
For the frequency table based solver, it takes an average of 3.68 guesses over the entire wordset. For the rank based solver, it's slightly higher at 4.02.
Nowhere near the 3.42 top score I've seen somewhere, but still respectable.

# Conclusion

And that's it! Feel free to try out the code for yourself, and let me know if there are any issues / improvements that I can make!
