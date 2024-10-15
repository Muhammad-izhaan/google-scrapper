from flask import Flask, render_template, request
from googlesearch import search
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_google(query):
   
    search_results = []
    for result in search(query, num_results=5):
        search_results.append(result)

    scraped_content = []
   
    for url in search_results:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
         
            paragraphs = soup.find_all('p')
            content = '\n'.join([para.get_text() for para in paragraphs[:3]])
            scraped_content.append((url, content))
        except Exception as e:
            scraped_content.append((url, "Error fetching content"))

    return search_results, scraped_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        urls, scraped_results = scrape_google(query)
        return render_template('index.html', query=query, urls=urls, results=scraped_results)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
