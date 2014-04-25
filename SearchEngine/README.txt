Sources:

http://docs.python.org/
http://stackoverflow.com/
www.piazza.com
Introduction to Information Retrieval, Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schutze.


run part1.py <dirname>
Enter query or 'exit':

run part2.py <dirname>
Enter query or 'exit':

Top 50 results are displayed.

Both of the files take around 40 secs to index the directory provided as an argument to the file and 
recursively process it.

Part1:
This is a basic Boolean search and currently performs AND operation on all of the query terms:

Part2:
This is a vector space model search, where documents are ranked based on dot product of tf-idf values with query. 
