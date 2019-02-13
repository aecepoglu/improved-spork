Feature: my server works
	Scenario: I check if my homepage is available
		Given the server is setup
		When I make a GET request to "/"
		Then the response status should be 200
		And the response should equal "The server works."
