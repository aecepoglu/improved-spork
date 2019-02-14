Feature: I can post ratings to songs
	Scenario: rate a song that has 0 ratings
		Given I made a GET request to "/songs?pagesize=1"
		And I saved the response at path "$.results[0]._id" to variable "MY_ID"
		When I make a POST request to "/songs/rating?song_id=<MY_ID>&rating=4" expanding variables
		Then the response json should be:
			"""
			{
				"num_ratings": 1,
				"max_rating": 4,
				"min_rating": 4,
				"avg_rating": 4
			}
			"""
	
	Scenario: rate a song that has ratings
		Given I made a GET request to "/songs?pagesize=1"
		And I saved the response at path "$.results[0]._id" to variable "MY_ID"
		And I made a POST request to "/songs/rating?song_id=<MY_ID>&rating=3" expanding variables
		And I made a POST request to "/songs/rating?song_id=<MY_ID>&rating=5" expanding variables
		And I made a POST request to "/songs/rating?song_id=<MY_ID>&rating=2" expanding variables
		When I make a POST request to "/songs/rating?song_id=<MY_ID>&rating=4" expanding variables

		Then the response json should be:
			"""
			{
				"num_ratings": 4,
				"max_rating": 5,
				"min_rating": 2,
				"avg_rating": 3.5
			}
			"""

	Scenario: get ratings of a song
		Given I made a GET request to "/songs?pagesize=1"
		And I saved the response at path "$.results[0]._id" to variable "MY_ID"
		And I made a POST request to "/songs/rating?song_id=<MY_ID>&rating=3" expanding variables
		And I made a POST request to "/songs/rating?song_id=<MY_ID>&rating=5" expanding variables
		When I make a GET request to "/songs/avg/rating?song_id=<MY_ID>" expanding variables
		Then the response json should be:
			"""
			{
				"num_ratings": 2,
				"max_rating": 5,
				"min_rating": 3,
				"avg_rating": 4
			}
			"""
	
	Scenario: rate a nonexistent song
		When I make a POST request to "/songs/rating?song_id=123456123456&rating=4"
		Then the response status should be 400
		And the response text should be "no such song"

	Scenario: don't supply song_id param
		When I make a POST request to "/songs/rating"
		Then the response status should be 400
		And the response text should be "'song_id' is required"

	Scenario: don't supply rating param
		When I make a POST request to "/songs/rating?song_id=something"
		Then the response status should be 400
		And the response text should be "'rating' is required"

	Scenario: get ratings of a nonexistent song
		When I make a GET request to "/songs/avg/rating?song_id=123456123456"
		Then the response status should be 400
		And the response text should be "no such song"

	Scenario: rate too low
		Given I made a GET request to "/songs?pagesize=0"
		And I saved the response at path "$.results[0]._id" to variable "MY_ID"
		When I make a POST request to "/songs/rating?song_id=<MY_ID>&rating=0" expanding variables
		Then the response status should be 400
		And the response text should be "Rating too low. Must be between 1 and 5."

	Scenario: rate too high
		Given I made a GET request to "/songs?pagesize=1"
		And I saved the response at path "$.results[0]._id" to variable "MY_ID"
		When I make a POST request to "/songs/rating?song_id=<MY_ID>&rating=6" expanding variables
		Then the response status should be 400
		And the response text should be "Rating too high. Must be between 1 and 5."
