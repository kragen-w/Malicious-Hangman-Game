from random import choice


"""
    This program allows the user to play hangman. The number of guesses and length of the word to be guessed is determined by the user, and they can
    only enter numeric values. Then they guess letters, and only single letters are valid inputs The program checks to see if there are words that dont contain the letter the 
    user guessed, and if so, those words become the new word bank for the program. This continues until there are no words that don't contain the user's letter guess. If this
    happenes, then the program takes a random word as the answer, and the game continues as normal. If the letter shows up in the word, then
    it is revealed in the proper spot. If the user runs out of guesses or wins at any point, the game ends. The program asks the user if they want to play again, and if they
    do, then the whole game loops again. If not, the program ends.
    Filename: wild_project4_hangmanpt2.py
    Author: Kragen Wild
    Date: 5-19-23
    Course: Programming II
    Assignment: Project 4 - Hangman pt2
    Collaborators: nada
    Internet Source: nada
"""


#empty dictionary is created
the_word_dictionary = {}

#open the file
with open(f"projects/wild_project4_hangmanpt1/Dictionary.txt", "r") as a_file:
    #gets every word and strips is and lowers it, iterates through them
    for word in a_file:
        word = word.strip().lower()
        #if the key of the word length already exists, the word is appened to the list of values in that key
        if the_word_dictionary.get(len(word)) != None:
            the_word_dictionary[len(word)].append(word)
        #if not, a list is started with the key being the length of that word, starting with that word
        else:
            the_word_dictionary[len(word)] = [word]

def print_the_progress(length_of_word, guess_progress):
    """
        this function prints out the current progress of guesses the user has, with dashing being ungesssed letters, and 
        guessed letters being in their proper spot
        perameters: length_of_word: int, guess_progress: list
        return: none
        """
    #i will iterate from 0 to the length of the word-1
    for i in range(length_of_word):
        #if i is not at the last index
        if i != length_of_word-1:
            #the value in the list guess progress at index i is printed with a space between each value, and there is no new line
            print(f"{guess_progress[i]} ", end="")
        #this makes it so there is not a stray space at the end
        else:
            print(f"{guess_progress[i]}")

#the play again variable starts as true
play_again = True
#while the user wants to play again:
while play_again == True:
    
    #the length of word and number of guesses is determined by the user, and can only be numeric values
    word_length = (input("Enter a word length to play with. "))
    while not word_length.isnumeric() or int(word_length) > 24:
        word_length = (input("Enter a valid word length to play with. "))

    number_of_guesses = (input("Enter the number of guesses. "))
    while not number_of_guesses.isnumeric():
        number_of_guesses = (input("Enter a valid number of guesses. "))

    word_length = int(word_length)
    number_of_guesses = int(number_of_guesses)

    #the guess progress list is initialized with all "_" because the user has no progress at the start
    guess_progress = []
    for i in range(word_length):
        guess_progress.append("_")

    #keeps track of the amount of guesses the user has taken
    users_guesses = 0
    #keeps track if the user has won
    user_has_won = False
    #list containing the already guessed letters
    already_guessed_letters = []

    #this variable flips if there can't be any more letter removals
    dictionary_narrowed = False

    #this houses the list of words that are the length the user chose
    target_word_set = {x for x in the_word_dictionary[word_length]}

    #while there are still guesses left and the user hasnt won,
    while users_guesses != number_of_guesses and user_has_won == False:

        #the word progress and past guesses are printed
        print_the_progress(word_length, guess_progress)
        print(f"Past guesses:{already_guessed_letters}")

        #the guesses letter is inputed by the user, and this line also tells them how many guesses are left
        letter_guess = input(f"Guesses left: {number_of_guesses-users_guesses}\nGuess a letter. ").lower()

        #if the guess is non alphabet or more than one character, the program asks the user to guess again
        while not letter_guess.isalpha() or len(letter_guess) != 1:
            letter_guess = input(f"Enter valid guess. ")

        #if the guessed letter hasnt already been guessed
        if letter_guess not in already_guessed_letters:
            
            #if the dictonary hasnt already been narrowed (if there are still words to remove)
            if dictionary_narrowed == False:

                #a new empty set is made that will house all the words without the guessed letter
                set_excluding_letter = set()
                #for every word in the target word set
                for word in target_word_set:
                    #if the guessed letter isnt in the word, then the word is added to the set that houses
                    #words that dont contain the letter
                    if letter_guess not in word:
                        set_excluding_letter.add(word)

                #if the length of the set exluding the letter is 0 (meaning there are no words without the user's letter guess)
                if len(set_excluding_letter) == 0:
                    #then a random choice is made from the set to be the answer
                    answer = choice(tuple(target_word_set))
                    #the dictonary is now narrowed
                    dictionary_narrowed = True

                    #i loops through the indexes of the word
                    for i in range(word_length):

                        #if letter at index i of the answer is the letter guess
                        if answer[i] == letter_guess:

                            #the guess progress at index i becomes the letter guess
                            guess_progress[i] = letter_guess
                else:
                    #if the set containing words without the guessed letter is not empty, it will
                    #become the new target word set
                    target_word_set = set_excluding_letter


            #if the guessed letter is in the answer
            elif letter_guess in answer:

                #i loops through the indexes of the word
                for i in range(word_length):

                    #if letter at index i of the answer is the letter guess
                    if answer[i] == letter_guess:

                        #the guess progress at index i becomes the letter guess
                        guess_progress[i] = letter_guess
            
            #if there are no more blank spaces in the guess progress, then the user has won
            if "_" not in guess_progress:
                user_has_won = True

        #if the letter has already been guessed
        else:
            #while the inputted letter has been guessed previously
            while letter_guess in already_guessed_letters:

                #the new letter guess becomes the input of the user
                letter_guess = input(f"Already guessed {letter_guess}, guess another. ")
        #the guess gets added to already guessed letters 
        already_guessed_letters.append(letter_guess)   

        #the guesses goes up by one 
        users_guesses += 1

    print_the_progress(word_length, guess_progress)

    #if the user won, then a victory printout is printed
    if user_has_won == True:
        print_the_progress(word_length, guess_progress)
        print(f"You win! The word was {answer}.")

    #if they didnt win, a losing printout is printed
    else:
        if dictionary_narrowed == True:
            print(f"You lost bruh, the word was {answer}.")
        else:
            answer = choice(tuple(target_word_set))
            print(f"You lost bruh, the word was {answer}.")

    #again is the users input to playing again, if they enter y, the game loops, if not, the program ends
    again = input("Play again? Y/N ")
    if again.lower() != "y":
        play_again = False