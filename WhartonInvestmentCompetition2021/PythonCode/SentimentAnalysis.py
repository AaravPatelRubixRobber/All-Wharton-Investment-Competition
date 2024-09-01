# Import libraries
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

# Get Data
finwiz_url = 'https://finviz.com/quote.ashx?t='

def getSentiment(ticker):
    url = finwiz_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
    resp = urlopen(req)
    html = BeautifulSoup(resp, features="lxml")
    news_table = html.find(id='news-table')

    parsed_news = []
    for x in news_table.findAll('tr'):
        text = x.a.get_text()
        date_scrape = x.td.text.split()

        ticker = ticker.split('_')[0]

        parsed_news.append([ticker, text])

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()


    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    print(news)

    dataframe = news.set_index('Ticker')


    sentiment_score = round(dataframe['compound'].mean(), 2)
    return sentiment_score
