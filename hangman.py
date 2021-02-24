from random import choice
import sqlite3, re

connection = sqlite3.connect('games.db')
cursor = connection.cursor()

difficulty = None
while not difficulty:
    diff_select = input('Please input difficulty - Easy, Medium, or Hard: ').lower()
    if diff_select in ('easy', 'medium', 'hard'):
        difficulty = diff_select
        print(f'\n{difficulty.title()} difficulty selected')
    else:
        print('\nIncorrect difficulty name selected, please try again\n')
        difficulty = None

cursor.execute("SELECT word, highscore FROM hangman WHERE difficulty = ?", (difficulty, ))
words = cursor.fetchall()
word = choice(words)
highscore = word[1]
word = word[0]

printout = ' '.join('_'*len(word))

guessed_letters = []
remaining_guesses = 6
score = 0

while True:
    print(printout)
    guess = input('\nGuess a letter: ')
    if len(guess) != 1 or not re.fullmatch('[a-zA-Z]', guess):
        print('\nGuess must be a single letter, try again')
        continue
    
    if guess in guessed_letters:
        print("\nYou've already guessed that, try something else")
        continue

    score += 1
    guessed_letters.append(guess)

    if guess not in word:
        remaining_guesses -= 1
        if remaining_guesses > 1:
            print(f'\nIncorrect, try again\nYou have {remaining_guesses} incorrect guesses remaining')
        elif remaining_guesses == 1:
            print(f'\nIncorrect, try again\nYou have {remaining_guesses} incorrect guess remaining\nWatch out!')
        elif remaining_guesses == 0:
            break
        continue

    if guess in word:
        print('\nCorrect!')
        locations = [letter.start() for letter in re.finditer(guess, word)]
        printout = printout.replace(' ', '')
        for location in locations:
            printout = printout[:location] + guess + printout[location + 1:]

        if printout == word:
            break
        else:
            printout = ' '.join(printout)
            continue

if remaining_guesses > 0:
    print(f'\nYou win!\nThe word was {word.title()}\nYour score was {score}')
    if highscore != 27:
        if score > highscore:
            print(f'The previous high score for this word was {highscore}\nCongratulations!')
        elif score < highscore:
            print(f'The high score for this word is {highscore}')
        elif score == highscore:
            print(f'You tied the high score!')

else:
    print(f'\nYou lose!\nThe word was {word.title()}\nBetter luck next time!')