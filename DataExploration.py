#!/usr/bin/env python
# coding: utf-8

# # Exploratory data analysis and visualizations:  Average number of comments and pruning tags 
# 
# Since we gathered the data ourselves, the data seems pretty clean.  Now we try to interpret the data.  First we recreate the data frame from [ProblemStatement](ProblemStatement.ipynb).

# In[1]:


# For data frames
import pandas as pd

# Numerical calculations
import numpy as np

# PCA for data exploration
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Plotting
import matplotlib.pyplot as plt

# Load the data
raw_data = pd.read_csv("ProblemStatementOutputs/502_30-03-2023_10-42-28.csv")
#raw_data # for debugging


# ## Basic comments analysis
# 
# The first function that follows takes as input a feature and outputs its corresponding attribute (post type, author, or tag).  The other functions are used to take a list of features and create a data frame with the number of occurrences of that feature, the total number of comments, the average number of comments, and the median number of comments.

# In[2]:


# Input is a feature (under post type, author, or tag).
# Output is the attribute (Post type, Author(s), or Tags) for that feature.
def attr(feature):
    for column in raw_data.columns:
        #print("Column is "+str(column)+ ".") # for debugging
        for entry in raw_data[column]:
            with_commas = str(entry).split("; ")
            #print("Entry to check is "+str(with_commas)+".") # for debugging
            if feature in with_commas:
                attribute = column
                return attribute

# Input is one of the column titles "Post type", Author(s)", or "Tags" from the raw_data data frame.
# Output is an unordered list of the possible values for that attribute.
def attribute_features(attribute):
    all_features_with_repeats = []
    #print(raw_data[attribute]) # for debugging
    for feature_attr in raw_data[attribute]:
        #print(feature_attr) # for debugging
        with_commas = str(feature_attr).split("; ")
        for feature in with_commas:
            all_features_with_repeats.append(feature) 
    all_features_list = [*set(all_features_with_repeats)]
    return all_features_list

# Input is a list of features (with attributes Post type, Author(s), or Tags).
# Output is a data frame with the features and the frequency with which they occur in the data.
def frequency_of_features(features):
    frequency_list = []
    for i in range(len(features)):
        occurrences = 0
        for index, row in raw_data.iterrows():
            authors_in_row_list = str(row["Author(s)"]).split("; ")
            tags_in_row_list = str(row["Tags"]).split("; ")
            if (features[i] in row["Post type"]) or (features[i] in authors_in_row_list) or (features[i] in tags_in_row_list):
                occurrences = occurrences +1
        frequency_list.append(occurrences)
    dict = {
        "Features":features,
        "Frequency":frequency_list
    }    
    return pd.DataFrame(dict, columns=["Features", "Frequency"])    
                
# Input is one of the column titles "Post type", Author(s)", or "Tags" from the raw_data data frame.
# Output is a data frame containing the frequency, total number of comments, average number of comments, 
    # and median number of comments, sorted by the average number of comments, then the median.
def comments_analysis(attribute):
    all_features_list = attribute_features(attribute)
    attr_total_comments_list, attr_avg_no_of_comments_list, attr_median_no_of_comments_list = ([] for i in range(3))
    for i in range(len(all_features_list)):
        comments = 0
        comments_data_list = []
        for index, row in raw_data.iterrows():
            attr_in_row_list = str(row[attribute]).split("; ")
            if all_features_list[i] in attr_in_row_list:
                comments = comments + int(row["No. of comments"])
                comments_data_list.append(row["No. of comments"])
        #print("comments_data_list =", comments_data_list) # for debugging
        #print("Mean of comments_data_list is "+ str(np.mean(comments_data_list))+".") # for debugging  
        #print("Median of comments_data_list is "+ str(np.median(comments_data_list))+".") # for debugging
        attr_total_comments_list.append(comments) 
        attr_avg_no_of_comments_list.append(np.mean(comments_data_list))
        attr_median_no_of_comments_list.append(np.median(comments_data_list))
    attr_comments_info = frequency_of_features(all_features_list)
    attr_comments_info["Total no. of comments"] = attr_total_comments_list
    attr_comments_info["Avg no. of comments"] = attr_avg_no_of_comments_list
    attr_comments_info["Median no. of comments"] = attr_median_no_of_comments_list    
    return attr_comments_info.sort_values(by = ["Avg no. of comments", "Median no. of comments"], ascending = [False, False])


# We can visualize the comments analyses for each of Post type, Author(s), and Tags using bar graphs.

# In[3]:


# Post type comments analysis
post_type_comments = comments_analysis("Post type")
post_type_comments.sort_values(by = ["Avg no. of comments", 
                                     "Median no. of comments"]).plot.barh(x="Features", 
                                                                        y=["Median no. of comments", "Avg no. of comments"])


# In[4]:


# Authors comments analysis
authors_comments = comments_analysis("Author(s)")
number_of_top_authors = 20
print("Since there are "+str(len(authors_comments["Features"]))+" authors we take the top "+str(number_of_top_authors)+".\n")
top_authors = authors_comments.head(number_of_top_authors).sort_values(by=["Avg no. of comments", "Median no. of comments"])
top_authors.plot(kind="barh", figsize=(10,10), x="Features", y=["Median no. of comments", "Avg no. of comments"])


# In[5]:


# Tags comments analysis
tags_comments = comments_analysis("Tags")
number_of_top_tags = 20
print("Since there are "+str(len(tags_comments["Features"]))+" tags we take the top "+str(number_of_top_tags)+".\n")
top_tags = tags_comments.head(number_of_top_tags).sort_values(by=["Avg no. of comments", "Median no. of comments"])
top_tags.plot(kind="barh", figsize=(10,10), x="Features", y=["Median no. of comments", "Avg no. of comments"])


# ## PCA analysis and pruning features
# 
# Some of the features (authors and tags) appear so few times that they are not very helpful.  Also, some of the tags like "Politics Podcast" and "Video" don't really give any information about the content, and since they appear frequently they disrupt the analysis of the rest of the data.  The following functions give ways to prune the features a little bit.  

# In[6]:


# First input is a list of features, second input is a list of features to be removed.
# Output is the first list of features with those in the second list removed.  
def prune(all_features, remove_features):
    pruned_features = all_features
    for feature in remove_features:
        pruned_features.remove(feature)
    return pruned_features    

# Input is a list of features (authors and tags).  Needs raw_data, attr, and frequency_of_features. 
# Output is the list with features that appear less than 2% of the time removed.
def most_used(features):
    frequencies = frequency_of_features(features)
    relevant_rows_list_with_repeats = []
    for feature in features:
        attribute = attr(feature)
        for entries in raw_data[attribute]:
            with_commas = str(entries).split("; ")
            if feature in with_commas:
                relevant_rows_list_with_repeats.append(np.array(raw_data.loc[raw_data[attribute] == entries].values.tolist()).flatten().tolist())            
    #print("Type for relevant_rows_list_with_repeats is "+str(type(relevant_rows_list_with_repeats))+".") # for debugging
    #print("Type for an item in relevant_rows_list_with_repeats is "+str(type(relevant_rows_list_with_repeats[0]))+".") # for debugging        
    #print("Relevant rows list (with repeats) is "+str(relevant_rows_list_with_repeats)+".") # for debugging
    relevant_rows_list_no_repeats = []
    for list_item in relevant_rows_list_with_repeats:
        if list_item not in relevant_rows_list_no_repeats:
            relevant_rows_list_no_repeats.append(list_item)
    total_data_points = len(relevant_rows_list_no_repeats) 
    #print("Total number of data points = "+str(total_data_points)+", compared to "+str(len(raw_data.index))+".") # for debugging
    most_used = []
    for feature in features:
        #print("Feature is "+str(feature)+".") # for debugging
        #print("The row containing "+str(feature)+" is: "+str(frequencies.loc[frequencies["Features"]==feature])+".") # for debugging
        fraction_of_appearances = int(frequencies.loc[frequencies["Features"]==feature]["Frequency"])/total_data_points
        #print("Fraction of appearances is "+str(fraction_of_appearances)+".") # for debugging
        if fraction_of_appearances > 0.02:
            most_used.append(feature)
    return most_used 

# Most used tags
#most_used_tags = most_used(attribute_features("Tags")) # for debugging
#print(str(len(most_used_tags)) + " out of " +str(len(attribute_features("Tags")))+" tags selected.")


# It seems like many of the tags in particular tend to appear together, and maybe certain authors produce content with certain tags, or other features are correlated.  We can do a PCA (principal component analysis) to find ways to group features that are correlated.  The following function creates a posts v. features matrix.

# In[7]:


# Input is a list of any combination of features from post types, authors, or tags found in raw_data.
# Output is a data frame whose rows are the post titles and whose columns are the features.
    # (Must remove the labels when inputting data into PCA analysis.)
def PCA_input(features):
    matrix = [raw_data["Title"].values.tolist()]
    #print("Rows are:\n", matrix) # for debugging
    for feature in features:
        #print("Feature is "+feature+".\n") # for debugging
        occurrences_list = []
        for index, row in raw_data.iterrows():
            #print("Row for "+row["Title"]+":") # for debugging
            for attribute in raw_data.columns.values.tolist():
                #print("Attribute is "+attribute+".") # for debugging
                # Turn all values of an attribute into a list
                with_commas = str(row[attribute]).split("; ")
                if feature in with_commas:
                    #print(str(feature)+" is in "+str(row[attribute])+".") # for debugging
                    occurrences_list.append(1)
            #print("The length of the occurrences_list is "+str(len(occurrences_list))+".") # for debugging
            #print("The index is "+str(index)+".") # for debugging
            if len(occurrences_list) != index+1:
                occurrences_list.append(0) 
        #print("occurrences_list = ", occurrences_list, "\n") # for debugging       
        matrix.append(occurrences_list)      
    return pd.DataFrame(np.array(matrix).transpose(), columns = ["Post"]+features)               


# We first run a PCA on the tags, after they have been pruned.

# In[8]:


# Remove unuseful tags
#print("Initial tags are "+str(attribute_features("Tags"))+".") # for debugging
#print("There are "+str(len(attribute_features("Tags")))+" of them.") # for debugging
tags_pruned = prune(attribute_features("Tags"), ["Politics Podcast", 
                                                 "Video", "Featured video", "FiveThirtyEight Podcasts",
                                                "Slack Chat", "Do You Buy That"])
#print("tags_pruned =", tags_pruned) # for debugging
#print("Length of tags_pruned is "+str(len(tags_pruned))+".") # for debugging
final_tags = most_used(tags_pruned)
#print("Final tags are "+ str(final_tags)+".  There are "+str(len(final_tags))+" of them.") # for debugging
      
# Create the matrix for tags
posts_v_features_matrix = PCA_input(final_tags)
#print("Post v. features matrix is: \n", post_v_features_matrix) # for debugging

# Make the PCA objects
scaler = StandardScaler()
pca = PCA()

# Fit the PCA
features_scaled = scaler.fit_transform(posts_v_features_matrix[posts_v_features_matrix.columns[1:]])
pca.fit(features_scaled)

# Get the PCA components
component_vectors = pd.DataFrame(pca.components_.transpose(), index = posts_v_features_matrix.columns[1:])
component_vectors.sort_values(by = component_vectors.columns[0], ascending = False)

