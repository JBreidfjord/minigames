import random

num = random.randrange(101)

print('Number is between 0 and 100\n')

guess = None
score = 0

while guess != num:
    while not guess:
        try:
            guess = int(input('Guess the number: '))
            if 0 <= guess <= 100:
                score += 1
            else:
                print('Sorry, your guess must be between 0 and 100')
                guess = None
        except ValueError:
            print('Sorry, your guess must be a whole number\n')
            guess = None
    if guess > num:
        print('Your guess was too high!\n')
        guess = None
    elif guess < num:
        print('Your guess was too low!\n')
        guess = None

print(f'Correct!\n\nYou win!\nYour score was {score}')