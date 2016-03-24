#import regex
import re
import csv
import pprint
import nltk.classify
import oauth2

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)
#end

#start process_tweet
def processTweet(tweet):
    # process the tweets
    
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)    
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end 

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet, stopWords):
    featureVector = []  
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences 
        w = replaceTwoOrMore(w) 
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector    
#end

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end


#Read the tweets one by one and process it
inpTweets = csv.reader(open('data/full_training_dataset1.csv', 'rb'), delimiter=',', quotechar='"')
stopWords = getStopWordList('stopwords.txt')
count = 0;
featureList = []
tweets = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#end loop

#Read tweets for test
inpTweets1 = csv.reader(open('data/test/test_data.csv', 'rb'), delimiter=',', quotechar='"')
stopWords = getStopWordList('stopwords.txt')
count = 0;
featureList = []
test_tweets = []
for row in inpTweets1:
    sentiment = row[0]
    tweet = row[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    test_tweets.append((featureVector, sentiment));
#end loop


# Remove featureList duplicates
featureList = list(set(featureList))

 # Generate the training set
training_set = nltk.classify.util.apply_features(extract_features, tweets)
test_set = nltk.classify.util.apply_features(extract_features, test_tweets)
#traincutoff = len(training_set)*1/4
#testcutoff = len(training_set)*3/4
#train_set = training_set[:20]+training_set[-20:] 
#test_set = training_set[20:40]+training_set[-20:-40]

# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
print 'accuracy:', nltk.classify.util.accuracy(NBClassifier, test_set)
NBClassifier.show_most_informative_features(30)

# Test the classifier

while True:
    testTweet = raw_input("Enter sentence: ")
    processedTestTweet = processTweet(testTweet)
    sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
    print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)
    print "Do you want to continue(y/n)?"
    option = raw_input()
    if option.lower() == 'n':
        break
        
