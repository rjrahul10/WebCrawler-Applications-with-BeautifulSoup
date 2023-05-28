import requests
import csv
from bs4 import BeautifulSoup as BS

base_url = 'https://news.yahoo.com/'

# Send a GET request to the base URL
response = requests.get(base_url)
soup = BS(response.content, 'html5lib')

# Find all the news articles on the homepage
article = soup.find_all('div', class_='Ov(h) Pend(44px) Pstart(25px)')

# Prepare the data to be saved in the CSV file
dataset = [['Rank', 'Title', 'Description', 'News_Link']]
rank = 0

# parsing the html and generating the dataset
for row in article:
    rank += 1
    title = row.find('h3').text.strip()
    desc = row.find('p').text.strip()
    newslink = row.find('a')['href']
    dataset.append([str(rank), title, desc, newslink])

# Save the data to a CSV file
with open("yahoo_news_data.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(dataset)

print(f'Successfully saved the news articles to yahoo_news_data.csv.')

