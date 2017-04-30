from sys import argv

# Open the file passed in through the command line.
dataset = open(argv[1], 'r').read()

# Open the other file passed in through the command line.
summaries = open(argv[2], 'r').read()

# Maps wikipedia movie ids to movie titles.
movies_to_ids = {}

all_ids = []

# Keeps track of every unique genre found in the dataset.
all_genres = []

# Keeps track of every unique movie found in the dataset.
all_movies = []

# Maps each movie to it's genres.
movies = {}

ids_to_summaries = {}

for line in summaries.split("\n"):
	if line == "": break
	all_ids.append(line.split("\t")[0])
	ids_to_summaries[line.split("\t")[0]] = line.split("\t")[1]

# Each line in the file is seperated into tab-seperated columns, 
#	the third of which is the title of the movie.
#	the ninth of which is the genres of the movie.
# Each movie is also given mutliple genres.

# Move through each line in the dataset.
for line in dataset.split("\n"):
	if line == "": break
	# Split the columns by the tabs.
	columns = line.split("\t")

	# Pick the columns containing thid id, the name, and the unformated genres.
	movie_id = columns[0]
	name = columns[2]
	genres_unformatted = columns[8]

	if movie_id in all_ids:

		# Each movie title will map to a list of genres.
		movies[name] = []

		movies_to_ids[name] = movie_id;

		# Need to unformat the genres.
		i = (len(genres_unformatted))
		genres_unformatted2 = genres_unformatted[1:i-1]
		for genre_line in genres_unformatted2.split(", "):
			if genre_line == "": break
			genre_quotes = genre_line.split(": ")[1]
			genre = genre_quotes[1:len(genre_quotes)-1]
			if genre not in all_genres: all_genres.append(genre)
			movies[name].append(genre)

		all_movies.append(name)

# Outputs the number of genres and number of movies, used for debugging.
print("Number of genres: " + str(len(all_genres)))
print("Number of movies: " + str(len(all_movies)))

# Creates the output file.
output = open("data.txt", 'w')

# For each movie, write the relevant data to the output file.
for movie in all_movies:
	output.write(movie + "\t" + ids_to_summaries[movies_to_ids[movie]] + "\t" + str(movies[movie]) + "\n")
