# donation-analytics-solution

Luke Winslow

## Implementation

This implementation is written in Python. This is a good fit 
for low-budget clients. It will be relatively easy to maintain by novice 
developers and did not take long to implement. It could run faster in other
languages, but the data volume does not really warrant further work. On my laptop, 
it executes on >500MB datasets in under a minute. 

The code should scale well to large datasets. The only scaling issue may be 
the memory footprint of keeping the full list of contribution values around for 
median calculation. But the data sizes just didn't seem to warrant a more complex,
streaming median implementation. I am rusty with Python, so there may be some odd syntax choices. 
But I used this as a good excuse to dive back into the language. 

## Dependencies

* python (tested with v2.7)
* numpy (python package, install with `pip install numpy`)

## Other issues to consider

These are a few thoughts the client may want to consider going forward. 

1. Ignoring out-of-order records implementation details could be interpreted
more than one way. I implemented it as "ignore any previous *year* record". But
out-of-order records within the same year are still counted in the "repeat donor" decision. 
These implementations have different tradeoffs. 

2. In examining full datasets online, I found a number of negative donation values. Generally 
associated with "REATTRIBUTED" records. One may want to ignore or handle these records differently. 

3. I didn't setup continuous integration (didn't want to push the limits with extra files in submission)
but setting up Travis or something akin would make future development a bit easier. 
