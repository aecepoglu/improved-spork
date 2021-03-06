Feature: I can find the avg difficulty for all songs
	Scenario: calculate for all songs
		When I make a GET request to "/songs/avg/difficulty"
		Then the response status should be 200
		And the response json schema should be:
			"""
			{
				"type": "object",
				"required": ["average_difficulty"],
				"properties": {
					"average_difficulty": {"type": "number"}
				}
			}

			"""
		And the response at path "$.average_difficulty" should be 10.32

	Scenario: calculate for a specific levels
		When I make a GET request to "/songs/avg/difficulty?level=6"
		Then the response status should be 200
		And the response at path "$.average_difficulty" should be 6

	Scenario: calculate for nonexistent level
		When I make a GET request to "/songs/avg/difficulty?level=99"
		Then the response status should be 400

