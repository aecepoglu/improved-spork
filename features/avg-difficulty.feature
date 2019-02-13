Feature: I can find the avg difficulty for all songs
	Scenario: see the calculation for all songs
		When I make a GET request to "/songs/avg/difficulty"
		Then the response status should be 200
		And the respone json schema should be:
			"""
			{
				"type": "object",
				"properties": {
					"average_difficulty": {"type": "number"}
				}
			}

			"""
		And the response at path "$average_difficulty" should be 10.32

	Scenario: see the calculation for songs at a specific level
		When I make a GET request to "/songs/avg/difficulty?level=6"
		Then the response status should be 200
		And the response at path "$average_difficulty" should be 6

