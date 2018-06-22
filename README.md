# FIXProtocolReader
This is a FIX protocol parser to answer specific set of questions:

1. How many instruments of each security type (tag 167) exist?
2. How many futures (tag 167) instruments exist in each product complex (tag 462)?
3. What are the names (tag 55) of the earliest four expirations (tag 200) for the futures (tag 167) instruments with asset (tag 6937) 'GE' and have zero legs (tag 555)?
