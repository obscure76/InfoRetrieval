Sources:
http://docs.python.org/
http://stackoverflow.com/
www.piazza.com
Introduction to Information Retrieval, Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schutze.

##################################################################################################
Part1:
From a tweet corpus calculates top hubs and authorities based on Kleinbergs Hubs and Authorities algorithm

Run it as python sample.py tweets.txt
It will create a hna file output which lists top 20 users with highest Hubs and Authorities scores


##################################################################################################
Part2:
Report results for all the three folders of data.
Run the file as 
python <learn.py> <dir1> <dir2> <dir3>

This code will train a linear kernel sklearn SVM classifier with the training data set in each of the provided directories 
and then evaluate on the test sets provided in each of the corresponding directories.

At the end, it prints out the most significant features in each of the directory being classified and reports the accuracy 
of the classfication as a percentage.

C=30 was taken for better results.

This is done under requirement of CSCE 670 Information retrieval course
