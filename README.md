# 538 project (in progress)

In fall 2022 I participated in the Erdös Institute's data science boot camp.  Unfortunately I entered the boot camp 3 weeks late, then was very busy with teaching, so I didn't get much out of it, and in particulat, I didn't do a final project.  Then in February 2023 I decided to do a project by myself (during the boot camp the projects are meant to be done in groups), though I received a lot of help from the Erdös Institute staff.  I started this project in mid-March 2023, but had to put it on hold once April started, to work on another project.

## About the project

In this project I scraped data from the 500 most recent posts on the [fivethirtyeight.com features page](https://fivethirtyeight.com/features/): post type (article, video, or podcast), post title, url, author(s), date and time posted, tag(s), and number of comments.  The question I wanted to answer was, what kind of posts on 538 get the most comments?  See the ProblemStatement Jupyter notebook.

## What's in the files

All of the work I've done so far is in the DataExploration Jupyter notebook.  I thought it was getting too long, so I exported it as a .py file so I could import all the functions I defined into the DataExplorationII notebook.

The ProblemStatementOutputs folder contains the output files from each time I ran the scraping code in the ProblemStatement notebook.  When I was still debugging the scraping code I wanted to use some of the data I'd collected for exploratory analysis.  The 500_31-03-2023_11-01-50.csv file is the most recent file with all 500 posts.  It is dated 31 March.  When I get back to this project I may try scraping 1000 posts, then I will probably hide this folder in my .gitignore.  

The FirstAttempts folder contains all the files I used for my first attempt at a project, investigating the effects of drug use on mental health during the COVID-19 pandemic, using data from Kaggle.  I spent about 2 weeks on it and ultimately concluded the data was too low quality to do anything with.  However, I learned a lot of Python working on this and thought I should keep the progress I made.




