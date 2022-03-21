import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
import seaborn as sns
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
import nltk
#from nltk.probability import FreqDist


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sklearn.feature_extraction.text import CountVectorizer 

#load clean data
tweets = pd.read_csv('tweets_EDA_clean.csv', encoding='utf-8', index_col=0)

tweets['date'] = pd.to_datetime(tweets['date'])
tweets['created_at'] = pd.to_datetime(tweets['created_at'])

def app():
    
    sentimentAnalyser = SentimentIntensityAnalyzer()
    
    
    def calculate_sentiment(text):
        # Run VADER on the text
        scores = sentimentAnalyser.polarity_scores(text)
        # Extract the compound score
        compound_score = scores['compound']
        # Return compound score
        return compound_score
    
    
    
    # function that will categorize the 'sentiment_score' column by Postive, Negative, or Neutral 
    def getCategory(score):
        if score > 0.05:
            return 'Postive'
        elif score < -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    
    #######################################
    
    def clean_text(tweet):
    # function to clean tweets
    
        temp = tweet.lower()
        temp = re.sub(r'\\n'," ", temp) # removing \n -newline, replacing with a space
        temp = re.sub(r'&\S+',"  ", temp) #remove &amp, &gt
        temp = re.sub("@[a-z0-9_]+"," ", temp)
        temp = re.sub("#[a-z0-9_]+","  ", temp)
        temp = re.sub(r'http\S+', "  ", temp) # 
        temp = re.sub(r'covid19|covid-19|coronavirus|virus', "covid", temp) 
        temp = re.sub(r'vaccine|vaccination|vaccines|vaccinations',"vaccine", temp)
        temp = re.sub(r'covid\s+vaccine',"vaccine", temp)
        temp = re.sub('[()!?]', '  ', temp)
        temp = re.sub('\[.*?\]','  ', temp)
        temp = re.sub("[^a-z0-9]", "  ", temp)  #remove \ - _
    
    # Remove stop words from the twitter texts 
        stop_words = stopwords.words('english')
        temp = temp.split()
        temp = [w for w in temp if not w in stop_words]
        temp = " ".join(word for word in temp)
        return temp
    
    # Clean data
    tweets['pre_cleaned_text'] = tweets['text'].apply(clean_text)
    
    wordnet_lemmatizer = WordNetLemmatizer()
    tweets['cleaned_text'] = tweets['pre_cleaned_text'].apply(lambda x: " ".join(wordnet_lemmatizer.lemmatize(word, pos='v') for word in x.split()))
    
    
    ##########################################
    tweets['sentiment_score'] = tweets['text'].apply(calculate_sentiment)
    tweets['analysis'] = tweets['sentiment_score'].apply(getCategory)
    
    #use groupby on hour and variant to aggregate the sentiment score
    tweets['variant'] = tweets['variant'].astype('category')
    
    
    #subset of texts
    #words = nltk.word_tokenize(''.join([tweet for tweet in tweets['cleaned_text']]))
    
    vect = CountVectorizer(ngram_range=(1, 3))
    vect.fit(tweets['cleaned_text'])
    
    # Transform the review column
    X_text = vect.transform(tweets['cleaned_text'])
    
    X_text = X_text.toarray().sum(axis=0)
    #cols = vect.get_feature_names()
    
    ####################
    words1 = []
    tagged = nltk.pos_tag(vect.get_feature_names())
    for (word, tag) in tagged:
        if tag == 'NNP': # If the word is a proper noun
            words1.append(word)
    
    #wf = FreqDist(words)
    
    X_df = pd.DataFrame(X_text, index=vect.get_feature_names(), columns=['number'])
    X_df = X_df.sort_values(by=['number'], ascending=False)
    top_words = list(X_df.index[:500])
    
    #########################
    
  #  with open('style.css') as f:
 #       st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    ###########
    
    title1 = '<p style="color:Blue; font-size: 40px;">Covid-19 Sentiment on Twitter</p>'
    st.markdown(title1, unsafe_allow_html=True)
    
    title2 = '<p> This figure displays a heatmap of the average <code>sentiment_score</code> across <code>hour</code>\
                (x-axis) and <code>variant</code> (y-axis). The user can decide whether to see an entire aggregate of text\
                (Yes) or the top 500 words (No) using the radio buttons. </p>'
    
    st.markdown(title2, unsafe_allow_html=True)
    
    #st.markdown("This figure displays a heatmap of the average `sentiment_score` across `hour` (x-axis)\
       #         and `variant` (y-axis). The user can decide whether to see an entire aggregate of text (Yes) or \
      #          the top 500 words (No) using the radio buttons")
    
    #st.header("Heatmap:")
    title3 = '<p style="color:Blue; font-size: 32px;">Heatmap:</p>'
    #title2 = '<p style="color:Blue; font-size: 40px;">Heatmap:</p>'
    st.markdown(title3, unsafe_allow_html=True)
    
    
    select_all = st.radio("Select All:", ["Yes", "No"])
    
    if select_all == "No":
        temp_tweets = pd.DataFrame()
        select_text = st.selectbox('input text:', top_words)
    
        for idx in range(len(tweets)):
            if select_text in tweets.loc[idx, 'cleaned_text']:
                temp_tweets = temp_tweets.append(tweets.loc[idx,])
        
    else:
        temp_tweets = tweets.copy()
    
    temp_tweets['hour'] = temp_tweets['hour'].astype('int8')
    
    heat_df = temp_tweets.groupby(['hour', 'variant'])['sentiment_score'].mean().reset_index()
    heat_pivot = heat_df.pivot('variant', 'hour', 'sentiment_score')
    
    plt.figure(figsize=(20, 10))
    sns.heatmap(heat_pivot, cmap="icefire", linewidths=.7, annot=True)
    plt.tight_layout()
    plt.show()
    
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
    #"YlGnBu"