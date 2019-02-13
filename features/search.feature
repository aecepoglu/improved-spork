Feature: I can search song artists and titles case insensitively
	Scenario: An empty search
		When I make a GET request to "/songs/search"
		Then the respone json schema should be:
			"""
			{
				"type": "object",
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
								"title": {"type": "string"},
							}
						}
					}
				}
			}
			"""
		And the response at path "$.results" should have 11 items
	
	Scenario: search by artist
		When I make a GET request to "/songs/search?message=the yousicians"
		Then the response at path "$.results" should have 10 items
	
	Scenario: search by title
		When I make a GET request to "/songs/search?message=babysitting"
		Then the response at path "$.results" should have 1 items

	Scenario: search partial matches
		When I make a GET request to "/songs/search?message=sunrise"
		Then the response at path "$.results" should have 0 items
