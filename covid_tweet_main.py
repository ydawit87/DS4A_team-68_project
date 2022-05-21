# -*- coding: utf-8 -*-
"""
The script contains the main page of the streamlit application and creates a directory of tabs which provide a certain function. There are 5 tabs other\
than the home page; the components/tabs are Dataframe, Sentiment, WordCloud, Heatmap, and Prediction
"""
#https://www.hackerearth.com/practice/
#https://amueller.github.io/word_cloud/auto_examples/colored_by_group.html

import yoseph
import funke
import arianna
import suzan_v2
import yoseph2
import home_page
import streamlit as st

#add home page

hide_menu = """
<style>
#MainMenu{
    visibility:hidden;
}

    
footer:before{
    content: 'Created by Team 68: Yoseph Dawit, Arianna Cooper, Funke Olaleye, Suzan Pham, and Jasiya Thompson';
    display: block;
    position:relative;
    color: white;
}
    
</style>
"""


pages = {'About':home_page, 'DataFrame':suzan_v2, 'Sentiment':yoseph2, 'WordCloud':funke, 'Heatmap':arianna, 'Prediction':yoseph}

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.sidebar.title('App Navigation')

selection = st.sidebar.selectbox('Options', list(pages.keys()))

page = pages[selection]
page.app()

st.markdown(hide_menu, unsafe_allow_html = True)
