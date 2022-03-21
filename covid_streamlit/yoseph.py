# -*- coding: utf-8 -*-

import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def app():
    #st.title("*Covid-19 Sentiment on Twitter*")
    
  #  with open('style.css') as f:
 #       st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    title1 = '<p style="color:Blue; font-size: 40px;">Covid-19 Sentiment on Twitter</p>'
    st.markdown(title1, unsafe_allow_html=True)
 
    text1 = '<p> The user inputs a text. Then, the text is processed into the <code>vaderSentiment</code> module\
                to calculate the sentiment score and classification. Note: the sentiment score ranges\
                from -1 to 1. These scores are used to label sentiment as follows\
                <em id = "neutralSent">Neutral</em> ([-0.5, 0.5]), \
                <em id = "positiveSent">Positive</em> ((0.5, 1]), and \
                <em id = "negativeSent">Negative</em> ([-1, -0.5)). </p>'
        

    
    st.markdown(text1, unsafe_allow_html=True)
    
    
    
    #st.markdown("The user inputs a text. Then, the text is processed into the `vaderSentiment` module\
   #             to calculate the sentiment score and classification. Note: the sentiment score ranges\
  #              from -1 to 1. These scores are used to label sentiment as follows\
 #               `Neutral` ([-0.5, 0.5]), `Positive` ((0.5, 1]), and `Negative` ([-1, -0.5)). ")
    
    #st.header("Prediction:")
    
    title2 = '<p style="color:Blue; font-size: 32px;">Prediction:</p>'
    st.markdown(title2, unsafe_allow_html=True)
    
    
    
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
        return 'Positive'
      elif score < -0.05:
        return 'Negative'
      else:
        return 'Neutral'
    
    dict_sentiment = {'Negative':'negativeSent', 'Positive':'positiveSent', 'Neutral':'neutralSent'}
    
    text = st.text_input("input:")
    output = calculate_sentiment(text)
    #output = SentimentIntensityAnalyzer(text)
    st.caption("output:")
    #st.markdown('output:')
    #st.caption(output)
    
    title3 = '<p>  <em id = {}>{}</em>     </p>'.format(dict_sentiment[getCategory(output)], output)
    st.markdown(title3, unsafe_allow_html=True)
    
    title4 = '<p> <em id = {}>{}</em>    </p>'.format(dict_sentiment[getCategory(output)], getCategory(output))
    st.caption("classification:")
    #st.caption(getCategory(output))
    st.markdown(title4, unsafe_allow_html=True)

