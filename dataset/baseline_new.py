from sys import argv
# randint(a, b) returns a random integer from [a,b] inclusive.
from random import randint

# Defines a dictionary that returns a 0 when the key is missing.
def DictWithDef(dict):
    def __missing__(self, key):
        return 0

# Opens the file containing the data created before,
#     and reads in the text within the file.
data_file = open(argv[1], 'r')
data_string = data_file.read()

# Dictionary to keep track of number each genre that appear.
genre_counts = {}

# Keeps track of the total number of genres.
total_genre_count = 0

# List to keep track of each movie title.
movie_titles = []

# A Dictionary that keeps track of each movie's actual genres.
movies_to_genres = {}

print("Now parsing input data.")

# Iterate through each newline seperated line.
# This allows us to count the number of each genre.
for line in data_string.split("\n"):
    if line == "": break
    # The columns are seperated with tabs.
    columns = line.split("\t")
    title = columns[0]

    # Add the current title to the list of titles.
    movie_titles.append(title)

    # This dictionary will map movie titles to lists of genres.
    movies_to_genres[title] = []

    # In order to remove the '[' and the ']'.
    unformatted_genres = columns[2][1:len(columns[2])-1]
    for genre_line in unformatted_genres.split(", "):
        if genre_line == "": break

        # In order to remove the 's.
        genre = genre_line[1:len(genre_line)-1]        
        
        # Increment the number of each genre by one.
        if genre not in genre_counts.keys(): genre_counts[genre] = 0
        genre_counts[genre] = genre_counts[genre] + 1

        # Increment the total number of genres.
        total_genre_count += 1

        # Adds the genre to the movie's list of correct genres.
        movies_to_genres[title].append(genre)

print("Done parsing input data.")

# Keeps track of the total number of guesses and the correct number of guesses.
correct_guesses = 0
total_guesses = 0

# Iterate through each movie, generating a random genre.
for movie in movie_titles:
    # Super complicated algorithm to generate random genres.
    i = randint(0, total_genre_count)
    for genre in genre_counts.keys():
        if i < 0: break
        guess = genre
        i -= genre_counts[genre]
    if guess in movies_to_genres[movie]: correct_guesses += 1
    total_guesses += 1

print("Done generating weighted random genres.")
print("Total Number of Unique Genres: " + str(len(genre_counts)))
print("Total Guesses: " + str(total_guesses))
print("Correct Guess Fraction: " + str(float(correct_guesses/total_guesses)))

# Keeps track of the total number of guesses and the correct number of guesses.
correct_guesses = 0
total_guesses = 0

# Iterate through each movie, generating a random genre.
for movie in movie_titles:
    # Super complicated algorithm to generate random genres.
    i = randint(0, len(genre_counts.keys())-1)
    guess = list(genre_counts.keys())[i]
    if guess in movies_to_genres[movie]: correct_guesses += 1
    total_guesses += 1

print("Done generating truly random genres.")
print("Total Number of Unique Genres: " + str(len(genre_counts)))
print("Total Guesses: " + str(total_guesses))
print("Correct Guess Fraction: " + str(float(correct_guesses/total_guesses)))
