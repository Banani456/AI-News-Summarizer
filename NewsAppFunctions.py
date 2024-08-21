import os
from newsapi import NewsApiClient
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import date
import pypdf
import pdfkit

def news_api_url_extraction(content, lang):
    load_dotenv()
    #news api key authentication
    newsApi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
    
    #date settings for NEWSAPI request
    today_DATE = date.today()

    if today_DATE.month != 1:
        month, year = today_DATE.month-1, today_DATE.year
    else:
        month, year = 12, today_DATE.year-1

    last_month_DATE = today_DATE.replace(month=month, year=year)

    today = today_DATE.strftime('%Y-%m-%d')
    last_month = last_month_DATE.strftime('%Y-%m-%d')

    #making requests to news api to get news urls!! GETTING USER INPUT HERE
    #d = newsApi.get_everything(q=content, language = lang, from_param = last_month, to = today, sort_by= "relevancy")
    d = newsApi.get_everything(q=content, language = lang, sort_by= "relevancy")
    #q for topic, set language to whatever you like
    
    api_url_list = []
    n_of_articles = int(d['totalResults'])
    if n_of_articles>100: n_of_articles = 100

    for i in range (n_of_articles):
        api_url_list.append(d['articles'][i]['url'])

    #api_url_list.reverse()

    url_list = []
    if len(api_url_list)<5:
        url_list = api_url_list
    else:
        for i in range(5):
            url_list.append(api_url_list[i])
    
    return url_list

#pdf creation
def pdf_maker(url):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url(url, "return.pdf", configuration=config)
    os.replace("./return.pdf", "./pdfs/return.pdf")

#SUMMARIZER
def summarizer(url_list):
    BIGSTRING = ""

    #google api key authentication
    load_dotenv()
    genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    #Set a string which holds summary
    for i in range(len(url_list)):
        #Set a string which holds summary
        summary = ""
        response = model.generate_content([url_list[i], "Can you summarize this document as a bulleted list? Then add another bullet with sentiment analysis of the text provided."])
        summary = str(response.text)
        BIGSTRING = BIGSTRING + "Article " + str(i+1) + "\n" +  summary + "\nHere is the link: " + url_list[i] + "\n\n"
    return BIGSTRING

def news_app(x, y):
    urls = news_api_url_extraction(x, y)
    # Specify the path
    path = './output'
    file = 'news_summary.txt'
    
    # Creating a file at specified location
    with open(os.path.join(path, file), 'w') as fp:
        pass
    insert = open('./output/news_summary.txt', 'w')
    x = summarizer(urls)
    insert.write(x)

#news_app("BTS", "en")