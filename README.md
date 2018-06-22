# FIXProtocolReader

The Chicago Mercantile Exchange (CME) publishes a file from its public FTP site (http://www.cmegroup.com/confluence/display/EPICSANDBOX/MDP+3.0+-+FTP+Site+Information) that can be used to determine information for receiving market data for futures contracts. The file is a FIX protocol file that contains security definitions for future, spread, and option contracts.

This is a FIX protocol parser to answer specific set of questions:

1. How many instruments of each security type (tag 167) exist?
2. How many futures (tag 167) instruments exist in each product complex (tag 462)?
3. What are the names (tag 55) of the earliest four expirations (tag 200) for the futures (tag 167) instruments with asset (tag 6937) 'GE' and have zero legs (tag 555)?
