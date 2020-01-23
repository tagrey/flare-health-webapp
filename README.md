I used Flask and Python to make this app and used a MySQL database to store data between server restarts. The overall architecture includes app.py, which contains each endpoint as well as makes all SQL queries; analyze.py, which contains all logic for the frequency analysis, stemming, and exclusion of stop words when necessary as well as tests for stemming; templates/index.html, which is always rendered with various messages populated via the flash function of Flask; and files, which just contains a text file version of the stop words.

I ran the following SQL commands to set up the database:
	CREATE DATABASE IF NOT EXISTS word_freq;
	USE word_freq;

	CREATE TABLE IF NOT EXISTS recent_analyses (
	    original_text      TEXT             NOT NULL,
	    exclude_stop_words  BOOLEAN    NOT NULL,
	    word_frequencies  TEXT     NOT NULL,
	    date DATE NOT NULL
	);

A lot of my time was spent orienting myself with Flask as well as playing with CSS and HTML--I still don't have a great handle on how to make elements do what you want them to, so I couldn't quite get the layout right in 8 hours, but all of the information and functionality is there.

File uploads were handled by saving the file in question to the location example.txt within the application folder. Ideally, I would have a better way to deal with this, but I spent the hours I worked on this optimizing other things.

In terms of stemming, my approach deals with all of the test cases given, but definitely also incorrectly stems plural nouns among some other things; however, given the scale of this project, I thought it was permissible. Determining if a word is a verb is a whole other animal.

To handle switching excluding stop words on and off, I included a little checkbox that toggles that feature--it's represented as a 1 or 0 in the dropdown menu for True or False--once again, a small thing I ran out of time for.

The database always saves a new analysis--it is not limited to 10 entries, but the query always sorts them by date and just picks the top 10. Ideally I would be throwing out entries that aren't the 10 newest, but that didn't seem like a huge space optimization problem given the scope.