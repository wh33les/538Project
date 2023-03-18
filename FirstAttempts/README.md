# First attempts

This folder contains the files for my first attempts at the project.  I used a data set from [Kaggle](https://www.kaggle.com/datasets/thedevastator/mental-health-in-drug-users-during-covid-19) on mental health in drug users during the COVID-19 pandemic.  The data consists of two files with the results of two surveys conducted in spring and summer of 2020.  Ultimately I didn't finish the project with this data, mainly because I could not find enough information about the data and how to interpret it.  However, since I still learned a lot while trying to work with this data, I decided keep the files in my repository.

The notebooks in this folder should be compiled in the following order:
1. ProblemStatementStakeholdersKPIs
2. CleaningI
3. CleaningII

The CleaningAndPreprocessing notebooks were my first attempt at cleaning the data, and they may not completely compile since they rely on results from the ProblemStatement... notebook that I've since changed.  I've included them in this folder anyway because they contain some interesting code that I didn't use in the Cleaning notebooks, most notably a loop that goes through the columns of the data and asks for user prompts to delete or rename each column.

The Cleaning notebooks are my second attempt at cleaning the data.  The data contains a lot of Spanish so in these notebooks I use a better translator API than Google translate (which was used in the CleaningAndPreprocessing notebooks), DeepL.  DeepL requires an authentication key which one can get for free by following the instructions [here](https://github.com/DeepLcom/deepl-python).  My key is in a file that is not in this remote repository, for security reasons, because DeepL only allows free translations of up to 500,000 characters per month.
