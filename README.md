# HURDAT2 data file processing

In this project, I work with a historical data called “HURDAT2”. From http://www.nhc.noaa.gov/data/#hurdat I can download two sets of data (Pacific and Atlantic) in a strange CSV format. The strangeness is due to the intermixture of two interrelated line formats, the lack of column headers, and a ton of N/A data values (-999). There are accompanying PDFs on that same webpage that describe the data format in fine detail.

I wrote a python program to do the following things:
1. As it reads those data files, it compute and print out the following data for each storm system:
   a) storm system name
