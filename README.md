# Example Matching Engine and Tests

## Scripts (Tested on CentOS7)

- build.sh: Build docker image
- test.sh: Run unit tests
- run.sh: Run app against sample data


## Instructions: 
```
git clone https://github.com/boksman/matching-engine.git
cd matching-engine
chmod u+x *.sh
sudo ./test.sh  
sudo ./run.sh
```
## test.sh output
```
Removing intermediate container 3a0894561610
 ---> df063d9f990c
Step 6/7 : COPY . .
 ---> d1a6cf79b99e
Step 7/7 : CMD [ "python"]
 ---> Running in 4dd71313907e
Removing intermediate container 4dd71313907e
 ---> 27e980c9876a
Successfully built 27e980c9876a
Successfully tagged matching-engine:1.0.dev
Build done
docker run -t matching-engine:1.0.dev python -m pytest test
============================================================================ test session starts ============================================================================
platform linux -- Python 3.7.4, pytest-6.0.1, py-1.10.0, pluggy-0.13.1
rootdir: /app
collected 5 items

test/test_engine.py .                                                                                                                                                 [ 20%]
test/test_main.py .                                                                                                                                                   [ 40%]
test/test_message_parser.py ...                                                                                                                                       [100%]

============================================================================= 5 passed in 0.05s =============================================================================
done

```




## Performance Characteristics by Scenario
- Determine if AddOrderRequest results in a match
  - O(n)  - Linear evaluation of one half the book is the most significant operation
- Removing filled orders from the resting order book
  - Runtime complexity is O(log(n)) for removing from half the book 
- Removing a cancelled order: 
  - Runtime complexity is O(log(n)) for the removal of object from a particular side of the book.  


