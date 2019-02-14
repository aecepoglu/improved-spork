Feature: I can list songs
	Scenario: list all songs
		When I make a GET request to "/songs"
		Then the response status should be 200
		And the response json schema should be:
			"""
			{
				"type": "object",
				"required": [
					"offset",
					"pagesize",
					"cur_count",
					"total_count",
					"results"
				],
				"properties": {
					"offset": {"type": "number"},
					"pagesize": {"type": "number"},
					"cur_count": {"type": "number"},
					"total_count": {"type": "number"},
					"results": {
						"type": "array",
						"items": {
							"properties": {
								"artist": {"type": "string"},
								"title": {"type": "string"}
							}
						}
					}
				}
			}
			"""
		And the response at path "$.results" should have 11 items
		And the response at path "$.cur_count" should be 11
		And the response at path "$.total_count" should be 11

	Scenario: list the 1st page of songs
		When I make a GET request to "/songs?pagesize=3&offset=0"
		Then the response status should be 200
		And the response at path "$.cur_count" should be 3
		And the response at path "$.results" should have 3 items
		And the response at path "$.offset" should be 0
		And the response at path "$.pagesize" should be 3
		And the response at path "$.results[0].title" should be "Lycanthropic Metamorphosis"
	
	Scenario: list the final page of songs
		When I make a GET request to "/songs?pagesize=5&offset=9"
		Then the response status should be 200
		And the response at path "$.cur_count" should be 2
		And the response at path "$.pagesize" should be 5
		And the response at path "$.results[0].title" should be "Vivaldi Allegro Mashup"
