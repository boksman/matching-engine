# Example Matching Engine and Tests

## Scripts (Tested on CentOS7)

- build.sh: Build docker image
- test.sh: Run unit tests
- run.sh: Run app against sample data

## Performance Characteristics by Scenario
- Determine if AddOrderRequest results in a match
- Removing filled orders from the resting order book
  - Runtime complexity is O(log(n))
- Removing a cancelled order:
  - Runtime complexity is O(log(n)) for the removal of object from a particular side of the book. 
