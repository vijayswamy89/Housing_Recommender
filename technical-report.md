# Technical Report - New York City Apartment Recommender

## Problem Statement

[Craigslist](https://newyork.craigslist.org/search/aap) is a platform where users post
available housing listings. My goal is to recommend apartment listings that a user
would be interested in moving into.

## Data Collection

Craigslist has an API for obtaining housing listings. The API has a python wrapper written above it. To access these listings, you will need to download the python library python-craigslist.

To install this on your machine, simply type pip install python-craigslist.

## Data Creation

The notebook Creating-Listings.ipynb is concerned with creating a document of listings posted on Craigslist. Each craigslist listing consists of several properties: bedrooms, bathrooms, price, image, url, id, geocode, and neighborhood. Each craigslist listing can be viewed in a Javascript On Notation(JSON) format.

After extracting the listings, we also find information about what amenities surround these listings. To do this, we use Yelp and Google Maps to seek the entertainment options and visualize our listings. To obtain access to both Yelp and Google Maps, we must create developer accounts with both Yelp and Google Maps. After creating these accounts, we can obtain the needed authorization keys and tokens to proceed.

We want to check if three pizza places, bagel shops, cocktail bars, and convenience stores are within a half mile radius of each apartment listing. To do this, we need Yelp’s API to obtain the nearby listings and calculate the haversine function to find the distances to check whether these conditions are true. In addition to finding out nearby shops and restaurants, we want to check if the apartments listings are less than one mile from an express subway train. To do this, we use Google Maps to find the latitude and longitude of all the express trains in New York City.

After performing these steps, I need to convert the listings into a format that can be readable by python’s pandas, a library equivalent in functionality to Microsoft Excel. To do this, I converted column values into a format such as string or integer or another data type that pandas can read.

Lastly, I need to find a way to simulate user behavior. I created a user that is a recent graduate from college and just landed his first job in New York City and is unable to afford rent greater than $2000 a month. To do this, I create conditional statements to simulate a user choosing an apartment listing if it is greater than 1000 and less than 2000 and is near an express train station. I also simulate a user choosing apartments slightly greater than 2000 if the listing happens to be near an express train station.

I also periodically change the location queried on Craigslist to create a dataset that consists of listings inside New York and outside New York. I choose some locations with similarities to New York such as proximity to many shops and restaurants but I also choose locations that aren’t within a one mile radius of many shops and restaurants. For this project, I chose to find listings in San Francisco, Los Angeles, Chicago, and in Houston.

I understood that simulating user behavior was a rather tedious process so I wrote an automated python script that ran remotely on Amazon Web Services and stored the apartment listings obtained there. This script would run once a day around 8 PM UTC time. I decide to run the script once a day as Yelp has a limit on how many searches can be done in one day. Once finished, I download the file from Amazon Web Services onto my local machine.

## Exploratory Data Analysis

After creating a dataset of approximately 20,000 listings, I now begin the data analysis and processing. First, I analyze the distribution of the data. I check if there are any duplicates and there definitely are. I delete these listings. I look to see if there are any missing values. After finding missing values, I vary my strategy for missing values depending on what columns contain missing values. If the geolocation is missing, I opt to eliminate such a listing. If the area of the apartment listing is missing, I fill the value with 242 square feet, the minimum value for an apartment listing. I also eliminate variables that play little role in housing such as the id of the listing.

After filling the missing values, I convert categorical variables into a numeric format that can be read by machine learning algorithms. For example, I convert neighborhoods such as Upper West Side into a numerical code.

### Imbalance of Data

![Useful dist] (https://github.com/vijayswamy89/Housing_Recommender/blob/master/images/unbalanced-data.png)

In the data above, 0 represents apartment listings the user is not interested in checking out and 1 represents the apartment listings the user is interested in looking at.

As you can see from the data above, the user is not interested in the vast majority of apartments on craigslist. This isn’t surprising as New York City is a very expensive city and finding housing within this user’s budget is difficult.



Why would the imbalance of the data above be an issue for the models? Since 99% of the data contains apartment listings the user is not interested in and 1% of the data contains apartment listings the user is interested in pursuing, the model will train well on the 99% of the data but ignore the 1% of data as noise.

How do I deal with this situation? I oversample the 1% of the data or the apartment listings the user wants to explore. To do this, I use python’s library Synthetic Minority Oversampling Technique (SMOTE). This process will create many more samples of interested listings for the model to explore.


### What features are most correlated with whether a user is interested in an apartment listing?

![Useful dist] (https://github.com/vijayswamy89/Housing_Recommender/blob/master/images/top-correlated-features.png)

## Modeling

### Preparation for Modeling

I need a baseline for how a model will perform before creating models. To do this, I calculate the roc_auc_score using the percent of the original data that apartment listings the user is interested in. I get a 0.5 score, and a model that scores above this would be considered an improvement.

I create a train-test split of the data given. That is, I split the data in such a way that the models are given 20% of the data but test on the 80% of the data that is unknown.

Since the project deals with a classification problem, I will focus on two classification models: Ridge classifier and Neural Network classifier.

The Ridge classifier assigns a penalty to the coefficients in the model to reduce their error due to variance and as a result reduces overfitting.

The Neural Network is a set of given inputs with associated weights connected to a series of hidden layers, and two outputs or the classification of a listing as interested or not interested. Using training data, the neural network calculates values for output nodes and compares the calculations with the given output and calculates an error term from these steps. A neural network performs these steps to adjust the weights in the hidden layers so that the output values are closer to the correct values.

Before fitting the models and scoring them, it is important to run a cross validation scoring of both models. Why? Cross validation scoring will provide a range of scores that one can expect with both models. If the model scores well outside the range provided, there is a possibility the model could be overfitting or under-fitting.

### Performance

#### Ridge Classifier Scores

R2 score on train dataset:  0.826
ROC score on train dataset:  0.912

R2 score on test dataset:  0.826
ROC score on test dataset:  0.912

#### Ridge Classifier ROC Curve

![Useful dist] (https://github.com/vijayswamy89/Housing_Recommender/blob/master/images/ridge-classifier-roc.png)

#### Ridge Classifier Confusion Matrix

![Useful dist] (https://github.com/vijayswamy89/Housing_Recommender/blob/master/images/ridge-classifier-confusion-matrix.png)


#### Neural Network

R2 score on train dataset:  0.99
ROC score on train dataset:  0.99

R2 score on test dataset:  0.98
ROC score on test dataset:  0.994

#### Neural Network ROC Curve

![Useful dist] (https://github.com/vijayswamy89/Housing_Recommender/blob/master/images/neural-network-roc-curve.png)

#### Neural Network Confusion Matrix

![Useful dist] (https://github.com/vijayswamy89/Housing_Recommender/blob/master/images/neural-network-classifier-matrix.pn)

### Recommendations

![Useful dist] (https://github.com/vijayswamy89/Housing_Recommender/blob/master/recommendations.html)

#### How my recommender performs in comparison to a user filtering apartment listings between $1000 and $2000

I decided to pull ten apartments from craigslist ranging from $1000 to $2000. Of the 10 displayed, the user would be interested in three of them.
My recommender system suggests four apartment listings for this user and the user is interested in three of them.

### Future Studies

- Create more types of users- users with larger budgets for rent and users with more varied interests
- Feature engineer distance from all three airports- JFK, LGA, and Newark
- Feature engineer distance from Central Park
- Add image classification of apartments
