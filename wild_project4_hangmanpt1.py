from random import randint


"""
    This program allows the user to play hangman. The number of guesses and length of the word to be guessed is determined by the user, and they can
    only enter numeric values. Then they guess letters, and only single letters are valid inputs. If the letter shows up in the word, then
    it is revealed in the proper spot. If the user runs out of guesses or wins, the game ends. The program asks the user if they want to play again, and if they
    do, then the whole game loops again. If not, the program ends.
    Filename: wild_project4_hangmanpt1.py
    Author: Kragen Wild
    Date: 5-11-23
    Course: Programming II
    Assignment: Project 4 - Hangman pt1
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
    while not word_length.isnumeric():
        word_length = (input("Enter a valid word length to play with. "))

    number_of_guesses = (input("Enter the number of guesses. "))
    while not number_of_guesses.isnumeric():
        number_of_guesses = (input("Enter a valid number of guesses. "))

    word_length = int(word_length)
    number_of_guesses = int(number_of_guesses)

    #the word is chosen from the dicionary, using the length of the word as the key, at random from the list of words at that key
    word_index = randint(1,len(the_word_dictionary[word_length]))
    answer = the_word_dictionary[word_length][word_index]

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

    #while there are still guesses left and the user hasnt won,
    while users_guesses != number_of_guesses and user_has_won == False:
        #the word is printed nicely useing the function defined above
        print_the_progress(word_length, guess_progress)

        #the guesses letter is inputed by the user, and this line also tells them how many guesses are left
        letter_guess = input(f"Guesses left: {number_of_guesses-users_guesses}\nGuess a letter. ").lower()

        #if the guess is non alphabet or more than one character, the program asks the user to guess again
        while not letter_guess.isalpha() or len(letter_guess) != 1:
            letter_guess = input(f"Enter valid guess. ")

        #if the guessed letter hasnt already been guessed
        if letter_guess not in already_guessed_letters:

            #if the guessed letter is in the answer
            if letter_guess in answer:

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

    #if the user won, then a victory printout is printed
    if user_has_won == True:
        print_the_progress(word_length, guess_progress)
        print(f"you win, the word was {answer}.")

    #if they didnt win, a losing printout is printed
    else:
        print(f"You lost bruh, the word was {answer}.")

    #again is the users input to playing again, if they enter y, the game loops, if not, the program ends
    again = input("Play again? Y/N ")
    if again.lower() != "y":
        play_again = False
