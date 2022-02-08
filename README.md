# Wordle clone + solver + backtesting

I created something. 

Or rather, I found about this game last week and decided that one challenge a day wasn't going to cut it, and decided to make my own clone. After all, the rules seemed simple enough to implement. After this, I figured I could make a solver using principles that I had learned in school, and had last touched in those very same courses. 

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
* X always takes priority. That is to say, if the word you're looking for is "beach" and you guess "hatch", your result will be "FOOXX" -- indicating that the first "h" was a fail.
* You will know how many instances of a letter a word has. In essence, there is always some sort of 1 to 1 mapping of letters that allows logical deductions to be made. Like the example above, we can see that only one of the "h"'s was assigned a valid state.

With these in mind I implemented a two pass solution - one for the X's and one for the O's, in that order. Adjustments were made to accommodate words with less than 5 unique letters. Namely using a hashmap instead of a hashset, that also tracked letter count. Whenever a letter was encountered and processed, I would subtract it from the counter. This eliminated situations were letters were getting double counted, such as guessing "hatch" for "beach" -- without this fix, it would have been evaluated as "OOFXX".

Having a complete evaluation function in hand, it's safe to say that the wordle clone is complete. The remaining parts were word generation (I downloaded a dataset somewhere and randomly chose words from that set) and some print statements to make sure that everything was working smoothly. I also added in an encryption function that uses the mapping A -> 1, B -> 2 ... Z -> 26 to display the answer in debug situations but I've yet to use it thus far.
