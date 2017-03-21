# jump-start text document clustering
# very rough initial clustering using scikit-learn

# This program goes on to demonstrate additional text
# processing capabilities of Python. Here we gather up
# text from 297 blog pages dealing with web analytics,
# creating a document corpus for analysis. 
# We note that three blogs (003, 008, and 009)
# had only one document. We drop these from this analysis,
# defining a new input directory called results_for_clustering.
#
# We rely upon scikit-learn for our analysis, employing
# a bag-of-words approach to text analytics.

# An essential characteristic of working with text is
# the identification of features within text. 
# Without features, there is little we can do in
# terms of machine learing. Features are the variables
# we use in our analyses. In this example, we could use
# a terms-by-documents matrix to define features.
# But even more useful is a TF-IDF approach from scikit-learn.
# This applies an intelligent bag-of-words approach by
# throwing away words that occur way too often across an
# entire document collection, as well as throwing away words
# that occur so seldom as to be of little value in clustering.
# What we get from the TF-IDF process is a set of word
# vectors (TF-IDF values) for input to cluster analysis.

# See documentation at 
# <http://scikit-learn.org/stable/auto_examples/document_clustering.html>

# let's make our program compatible with Python 3.0/1/2/3
from __future__ import division, print_function
from future_builtins import ascii, filter, hex, map, oct, zip

import os  # operating system commands
import numpy as np  # for array definition and calculations
import sklearn as sk  # machine learning methods
import sklearn.feature_extraction.text as sktext  # text analytics
import sklearn.cluster as skcluster  # clustering methods
import pandas as pd  # includes contingency matrix

# Previous work provided a directory called results
# with text files from the web analytics blogs.
# identify all of the file names 
my_directory = '/Users/northwestern/Desktop/000_clustering_jump_start'
file_names =  os.listdir(my_directory + '/results_for_clustering/')
nfiles = len(file_names)  # nfiles should be 295

# as we read individual documents we will asssociate the
# blog number with each document... metadata/document tag
blog = []  # initialize
documents = []  # initialize document collection

for ifile in range(len(file_names)):
    this_file_name = my_directory + '/results_for_clustering/' + file_names[ifile]
    with open(this_file_name, 'rt') as f:
        this_file_text = f.read()
        documents.append(this_file_text)
        blog.append(int(file_names[ifile][6:8]))

# define a simple TF-IDF vectorizer to measure number_of_features for each document
# the number of features per document can be modified to get different solutions
# as can other aspects of the vectorizer...
number_of_features = 20
vectorizer = sktext.TfidfVectorizer(max_df = 0.5, max_features = number_of_features, stop_words = 'english')
X = vectorizer.fit_transform(documents)

# set up for K-Means Clustering... try different values of for n_clusters, perhaps in a loop
number_of_clusters = 2
km = skcluster.KMeans(n_clusters = number_of_clusters, init = 'k-means++', max_iter = 100, n_init = 1)
km.fit(X) 
labels = np.array(blog)

print()
print("Number of Clusters: ", number_of_clusters)                              
print("Homogeneity: %0.3f" % sk.metrics.homogeneity_score(labels, km.labels_))
print("Completeness: %0.3f" % sk.metrics.completeness_score(labels, km.labels_))
print("V-measure: %0.3f" % sk.metrics.v_measure_score(labels, km.labels_))
print("Adjusted Rand-Index: %.3f" % sk.metrics.adjusted_rand_score(labels, km.labels_))
print("Silhouette Coefficient: %0.3f" % sk.metrics.silhouette_score(X, labels = km.labels_, sample_size=1000))
print()
df = pd.DataFrame({'Blog': np.array(blog), 'Cluster': km.labels_})
print(pd.crosstab(df['Blog'], df['Cluster']))

# Let's obtain information about the features being employed, 
# as these would be needed to interpret the clusters. 
# We need to examine the words used to distinguish one cluster 
# from another. This information would be needed in explaining 
# the meaning of clusters to management.
feature_names = np.asarray(vectorizer.get_feature_names())
print(feature_names)
            
print('RUN COMPLETE')                