Feature: Need to manipulate dates for the git rollback system

Scenario: With a date and a month delta the result is the target date
Given date "1/22/1980" and delta "5"
When I get the date delta
Then the result should be "6/22/1980"