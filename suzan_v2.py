# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
import sqlite3


tweets = pd.read_csv('./tweets_EDA_clean.csv', encoding='utf-8', index_col=0)


def app():


#  def load_tweets(nrows):
#        tweets = pd.read_csv('./tweets_EDA_clean.csv', encoding='utf-8', index_col=0, nrows=nrows)
#        tweets['date'] = pd.to_datetime(tweets['date'])
#        tweets['created_at'] = pd.to_datetime(tweets['created_at'])
#        return tweets


  tweets['id'] = tweets['id'].astype('category')
  tweets['conversation_id'] = tweets['conversation_id'].astype('category')
  tweets['author_id'] = tweets['author_id'].astype('category')
  tweets['date'] = pd.to_datetime(tweets['date']).dt.date

  conn = sqlite3.connect('tweets.db', check_same_thread=False)
  c = conn.cursor()
  c.execute("create table if not exists tweets" +
                 "(text)")
  tweets.to_sql('tweets', conn, if_exists ='replace', index=False)  
  
  #extract tweets and order them by latest date  
  def search_word(text):
        c.execute("SELECT * FROM tweets WHERE text LIKE '%{}%' GROUP BY text ORDER BY date DESC".format(text))
        data = c.fetchall()
        return data  
    
   
  title1 = '<p style="color:Blue; font-size: 40px;">Covid-19 Sentiment on Twitter</p>'
  st.markdown(title1, unsafe_allow_html=True)  
  
  title2 = '<p style="color:Blue; font-size: 32px;">Explore the Dataframe</p>'
  st.markdown(title2, unsafe_allow_html=True)  


  st.markdown('The dataframe tab displays the rows and columns of the covid tweets. There are a collection of filters to \
              narrow down the dataset. The first component the input text where the user can type a word and the tweets\
              associated to the word is dislay once the enter button is pressed. The second component is a multi-select box on the variant which lets the user \
              decide the variants to include in the dataframe. The third component is also a multi-select box but this \
              time it involves the columns the user wants to select. The next two components are date inputs: one for \
              start date and one for end date. This lets the user filters the dataframe by the start date and end date.\
              The enter button is used to modify the changes of the dataframe the user has made with the components.\
              Note: The changes in the components are saved but the modification of the dataframe is not made until \
              the enter button is pressed.')


  
  with st.form(key='searchform'):
      search = st.text_input('Type in one word')
      submitted = st.form_submit_button("Enter")    
      st.success("You searched for {}".format(search))
            
      if submitted:
          results = search_word(search)
          temp_tweets = pd.DataFrame(results, columns=tweets.columns)

      else:
          temp_tweets = tweets
  ##########
  #select variant
  variant = list(tweets['variant'].unique())
  variant_choice = st.multiselect("select variant(s):", variant, default = variant)

  #select columns
  columns = tweets.columns.tolist()
  selected_columns = st.multiselect("Choose columns to display:", columns, columns)

  #date range
  start = datetime.datetime.strptime('2020-12-01', '%Y-%m-%d')
  end = datetime.datetime.strptime('2021-12-31', '%Y-%m-%d')
      
  start_date = st.date_input('Start date', start)
  end_date = st.date_input('End date', end)
  if start_date < end_date:
      pass
  else:
      st.error('Error: End date must be after start date.')
      
  temp_tweets['date'] = pd.to_datetime(temp_tweets['date']).dt.date
  result_date = (temp_tweets['date'] > start_date) & (temp_tweets['date'] <= end_date)



  temp_tweets = temp_tweets.loc[temp_tweets['variant'].isin(variant_choice) & (result_date), selected_columns]

  #enter = st.button('Enter')

  #if enter == True:
  st.write(str(temp_tweets.shape[0]) + ' rows X ' + str(temp_tweets.shape[1]) + ' columns')
  st.write(temp_tweets)


  title3 = '<p style="color:Blue; font-size: 32px;">Data Visualizations</p>'
  st.markdown(title3, unsafe_allow_html=True)  

  st.markdown('The select box below provides the user two options of visualizations: a correlation plot or a scatter plot.\
              The correlation plot displays a correlation matrix of the numeric features of the dataframe; the \
              modifications of the dataframe also impacts the correlation plot if the observations/columns were filtered.\
              The scatter plot provides the user two features to choice for display.')

  #creating options for how the user would like to see the visualizations
  data_visual = st.selectbox('Select a Visualization',
              ("", 'Correlation Heatmap on Numerics Columns', 'Scatterplot Between Selected Variables'))

  #correlation heatmap for likes and counts
  if data_visual == 'Correlation Heatmap on Numerics Columns':
      #st.write('#### Correlation Heatmap')
      title4 = '<p style="color:Blue; font-size: 32px;">Correlation Heatmap</p>'
      st.markdown(title4, unsafe_allow_html=True) 
      fig, ax = plt.subplots(figsize = (6,4))
      sns.heatmap(temp_tweets[['like_count', 'reply_count', 'retweet_count', 'followers_count',
        'following_count', 'tweet_count']].corr(), annot=True, ax=ax)
      st.set_option('deprecation.showPyplotGlobalUse', False)
      st.pyplot(fig)

  #user can choose 2 variables containing numerical datatypes, with the exception of source, to see a scatterplot
  if data_visual == 'Scatterplot Between Selected Variables':
      tweets_numbers = temp_tweets[['like_count', 'reply_count', 'retweet_count', 'followers_count',
        'following_count', 'tweet_count', 'source', 'date', 'variant', 'hour']]
      selected_x = st.selectbox('X-Axis', tweets_numbers.columns)
      selected_y = st.selectbox('Y-Axis', tweets_numbers.columns)
      fig = px.scatter(tweets_numbers, x = tweets_numbers[selected_x], y = tweets_numbers[selected_y])
      st.set_option('deprecation.showPyplotGlobalUse', False)
      st.plotly_chart(fig)





