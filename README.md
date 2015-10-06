# YahOption

This script contains functions that can retrieve option prices from yahoo finance.

I scheduled to write 4 main functions:
1) Get expire dates list when input a company ticker. This function has two outputs, namely
   the unix time and human readable time (EDT).
2) Get stock price when input a ticker.
3) Get the whole list of call strike prices and put strike prices when input a ticker and
   an expire date.
4) Get bid price, ask price, open interest etc. when input a ticker, expire date, strike price,
   and option type (call or put).
   
   
Schedule:
10.2 - finish all four functions. (v0.01)
before 10.7 - learn Beautiful Soup and decide whether to use it. (v0.02)
before 10.14 - write an objective oriented version. v(0.03)
before 10.21 - figure out a way to get historical prices. (v0.04)
before 10.28 - refine it and upload to Github. (v0.05)


What I have done:
10.3 - Almost finished the four functions, yet the script contains many bugs. I need to check if it is working
       with every stock.
       The script is not efficient since I request the html every time when I run a function. I use '*html' to
       fix this problem. However, there must be a better solution.
10.4 - Fixed bugs. passing html to functions boost the speed.
