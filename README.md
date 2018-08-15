# stac-validator
Python/Flask Validator for the stac-spec

## Requirements

* Python 3.x
    * Flask
    * Requests

## Design

1. Provided the root of a catalog, recursively validate each catalog entry until you get down to the item json and validate those.
2. Stop on error (if a catalog) and return the error to the user as json, if on the web page, render the contents in a pretty format. (Idea left side shows json, right side shows error).

## TODO
Here only because we don't have an issue tracker yet.

* Get interface FORM that takes catalog root url or single item to test.
* Recursively crawl catalog
* Pretty Print or better error logging for end user
    * When a json fails to validate the code needs to catch and display those errors to the user.
* Get a deployment running

## Discussion

1. How do you tell apart catalog from items by it's json. Can an item exist without a catalog?
    * For now we assume a catalog is provided as the starting point, items are identitifed by the link rel type
