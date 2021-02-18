# Example Matching Engine and Tests

## Scripts (Tested on CentOS7)

- build.sh: Build docker image
- test.sh: Run unit tests
- run.sh: Run app against sample data


## Instructions: 
- git clone https://github.com/boksman/matching-engine.git
- cd matching-engine
- chmod u+x *.sh
- sudo ./test.sh  
- sudo ./run.sh

## Performance Characteristics by Scenario
- Determine if AddOrderRequest results in a match
  - O(n)  - Linear evaluation of one half the book is the most significant operation
- Removing filled orders from the resting order book
  - Runtime complexity is O(log(n)) for removing from half the book 
- Removing a cancelled order: 
  - Runtime complexity is O(log(n)) for the removal of object from a particular side of the book.  


