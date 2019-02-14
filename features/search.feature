Feature: I can search song artists and titles case insensitively
	Scenario: An empty search
		When I make a GET request to "/songs/search"
		Then the response json schema should be:
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
		And the response status should be 200
		And the response at path "$.results" should have 11 items
	
	Scenario: search for artist with exact match
		When I make a GET request to "/songs/search?message=the%20yousicians"
		Then the response at path "$.results" should have 10 items
	
	Scenario: search for title with exact match
		When I make a GET request to "/songs/search?message=babysitting"
		Then the response at path "$.results" should have 1 items

	Scenario: search partial matches
		When I make a GET request to "/songs/search?message=sunrise"
		Then the response at path "$.results" should have 1 items
