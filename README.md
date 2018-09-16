# HURDAT2 data file processing

In this project, I work with a historical data called “HURDAT2”. From http://www.nhc.noaa.gov/data/#hurdat I can download two sets of data (Pacific and Atlantic) in a strange CSV format. The strangeness is due to the intermixture of two interrelated line formats, the lack of column headers, and a ton of N/A data values (-999). There are accompanying PDFs on that same webpage that describe the data format in fine detail.

I wrote a python program to do the following things:
1. As it reads those data files, it compute and print out the following data for each storm system:
  * Storm system name
  * Date range recorded for the storm
  * Find numerically the highest **Maximun sustained wind (in knots)** and when it occurred (date and time). 
  * How many times it had a "landfall"
  * For each storm, use an accumulator to compute and report the TOTAL distance each storm was tracked (This requires a special function such as provided in the PyGeodesy library).
  * Calculate the speed in knots that storm center moved, a.k.a "storm propagation". 

2. I investigate a scientific hypothesis: Based on physics, I expect that the quadrant with the
highest winds (and therefore longest radius of high wind) should typically be somewhere between 45-90 degrees clockwise of the storm’s recent direction of movement. To determine this, between each pair of data samples, compute the initial compass bearing (in degrees) of the storm’s movement. Then look at the columns of data for the highest level of non-zero radii (64-kt, 50-kt, or 34-kt) at that time, to see if it did fall into that quadrant or not (True or False). Finally, for the whole data set, show what % of the time this was true.
