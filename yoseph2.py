# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import seaborn as sns

import matplotlib.pyplot as plt 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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
    
    tweets['sentiment_score'] = tweets['text'].apply(calculate_sentiment)
    tweets['analysis'] = tweets['sentiment_score'].apply(getCategory)
    
    ########################################################################
    
    
  #  with open('style.css') as f:
 #       st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)    

    title1 = '<p style="color:Blue; font-size: 40px;">Covid-19 Sentiment on Twitter</p>'
    st.markdown(title1, unsafe_allow_html=True)    
    
    text1 = '<p> The figure below is a barplot of the sentiment across variant. The values of the \
                barplot can be normalized such that the sum is 1 for each variant by selecting \
                <code>yes</code> radio button under <code>normalize</code> while count by\
                selecting <code>no</code> radio button. </p>'
    
    st.markdown(text1, unsafe_allow_html=True)
    
    #st.markdown("The figure below is a barplot of the sentiment across variant. The values of the \
     #           barplot can be normalized such that the sum is 1 for each variant by selecting \
    #            `yes` radio button under `normalize` while count by selecting `no` radio button.")
    
    
    title1 = '<p style="color:Blue; font-size: 32px;">Sentiment:</p>'
    st.markdown(title1, unsafe_allow_html=True)
    
    #st.header("Sentiment:")
    
    select_normalize = st.radio("normalize:", ['Yes', 'No'])
    dict_norm = {'Yes':(True, 'Frequency'), 'No':(False, 'Count')}
    
    
    
    byVariant = tweets.groupby('variant')['analysis'].value_counts(normalize=dict_norm[select_normalize][0])
    byVariant = byVariant.rename('number').reset_index()
    #plt.figure(figsize=(10,4))
    #byVariant.plot.bar(color=['green', 'green', 'green', 'yellow', 'yellow', 'yellow', 'red', 'red', 'red'])
    
    #byVariant.rename('number').reset_index().pipe((sns.catplot, 'data'), x='variant',y='number',hue='analysis', kind='bar')
    sns.catplot(x='variant', y='number', data=byVariant, hue='analysis', kind='bar',\
                height=5, aspect=2)
    
    plt.xlabel("Variant")
    plt.ylabel(dict_norm[select_normalize][1] + " of each Category")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
        
    text2 = '<p> The next figure is a time series of <code>sentiment score</code>. The select box \
                <code>select variant</code> picks the selected variant of first 10 days. The default length of time\
                to aggregate is 15 minutes which can be changed by the select box called <code>time interval</code>. </p>'
    
    st.markdown(text2, unsafe_allow_html=True)
    
   # st.markdown("The next figure is a time series of `sentiment score`. The select box `select variant` \
    #            picks the selected variant of first 10 days. The default time interval\
     #           to aggregate is 15 minutes which can be changed by the select box called `time interval`.\
      #          ")
    
    select_var = st.selectbox("select variant:", ['beta', 'delta', 'omicron'])
    color_dict = {'beta':'blue', 'delta':'orange', 'omicron':'green'}
    
    select_timeinterval = st.selectbox("time interval:", ['15 minutes', '30 minutes', '45 minutes', '1 hour', '2 hours'])
    time_dict = {'15 minutes':'15min', '30 minutes':'30min', '45 minutes':'45min', '1 hour':'H', '2 hours':'2H'}
    
    tweets.loc[tweets['variant']==select_var].set_index('created_at')['sentiment_score'].resample(time_dict[select_timeinterval]).mean().plot(figsize = (10,4), color=color_dict[select_var])
    plt.title("Sentiment Scores on first 10 days " + select_var +  " Variant (Variant of Concern)")
    plt.ylabel("Sentiment Score")
    plt.xlabel("Date")
    plt.ylim([-1,1])
    plt.tight_layout()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
