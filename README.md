# DS4A_team-68_project

![Coronovirus_0_0](https://user-images.githubusercontent.com/92189294/160304123-219c9b35-80c1-4b1f-9505-3b3f0702b5e6.png)


The purpose of the app is to analyze tweeter data for the first 10 days of each variant. It provides 6 tabs: About, Dataframe, Sentiment, WordCloud, Heatmap, and Prediction. The About tab is an introduction page with the title and the description of the project. 

  The Dataframe tab displays the data through a criteria of filters (columns, variant, keyword, and date range). The component used for selecting columns is the function `st.multiselect()` where the user can select multiple values (columns) to click or unclick; `st.multiselect` is used instead of `st.selectbox` since a subset of the columns can exist in a dataframe. The variant also uses `st.mulitselect` since all variants exist in the dataframe. The date range utilizes a streamlit component called `st.date_input` on the column `created_at`; two `st.date_input` functions is used (one for start date and one for the end date where end date has to be larger than start date). The last component to address filter by keyword (text) is the `st.text_input`. Then, the text uses an SQL engine from the `SQLite3` module to extract rows where the `text` column contains the keyword. The next figure is a `st.selectbox` where the user can choose which visualization to display: correlation plot or scatterplot. If correlation plot is selected, a correlation heatmap is displayed from values -1 to 1. If the scatterplot is choosen, two `st.selectbox` components are generated where one represents the x-axis and the other one represents the y-axis for display of the 2D scatterplot. The list of columns to select from are `like_count`, `reply_count`, `retweet_count`, `followers_count`, `following_count`, `tweet_count`, `source`, `date`, `variant`, and `hour`.
  
  The Sentiment tab shows two figures. First is barplot across variant and sentiment. Second is a time series aggregated by a time interval the user can select.
  
  The WorldCloud tab displays the top n frequent words which the user can select. 

  The Heatmap tab visualizes a heatmap of the hour across the variant.
  
  The prediction tab allows the user to classify the input text as either positive, negative, or neutral. It requires the user to type in the text box and press enter. The module `vaderSentiment` is used to predict the sentiment score of the text. The module is tuned for social media analysis which can take into account for emojis, exclamations, stop words, etc. There are two results: a sentiment score and the sentiment. The sentiment score ranges from -1 to 1 which tells the user how strong the sentiment is on the text along with the sentiment. For clarity, the text was set a color to represent its sentiment: red for negative, green for positive, and gray for neutral. 
