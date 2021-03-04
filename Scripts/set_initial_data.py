import sys, csv, sqlite3

con = sqlite3.connect("../sqlite:///../db.sqlite3") # change to 'sqlite:///your_filename.db'
cur = con.cursor()

def main():
	for x in range(1, 672):
		cur.execute("INSERT into auth_user VALUES (?, '', null, 0, ?, 'user', '', 0, 0, date('now'), ?);", [x, "user" + str(x), str(x)])
	with open('movies_metadata.csv', "r", encoding="cp437") as f: # CSV file input
					reader = csv.reader(f, delimiter=';') # no header information with delimiter
					for row in reader:
						if row[5].isnumeric() and len(row) > 23 and row[23].isnumeric() and int(row[23]) > 0:
							cur.execute("REPLACE INTO web_movie (id, title, genres, poster_path, production_companies, overview, vote_average, vote_count) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", [row[5],row[20],row[3],row[11],row[12],row[9],row[22],row[23]])
	with open('ratings_small.csv', "r", encoding="cp437") as f: # CSV file input
					reader = csv.reader(f, delimiter=';') # no header information with delimiter
					for row in reader:
						if row[0].isnumeric():
							cur.execute("REPLACE INTO web_movierating (rating, movie_id, user_id) VALUES(?, ?, ?);", [int(float(row[2]) * 2),row[1],row[0]])
						
	con.commit()
	con.close()


if __name__=='__main__':
    main()