import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = 'https://www.basketball-reference.com/teams/OKC/draft.html'

# Send a GET request to fetch the raw HTML content
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page {url}")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table you want to scrape
table = soup.find('table', {'id': 'draft'})

if table is None:
    raise Exception("Could not find the draft table on the page.")

# Extract the table headers
headers = []
for th in table.find('thead').find_all('th'):
    headers.append(th.text.strip())

# Extract the table rows
rows = []
for tr in table.find('tbody').find_all('tr'):
    cells = []
    for td in tr.find_all(['td', 'th']):
        cells.append(td.text.strip())
    # Only add rows with the correct number of columns
    if len(cells) == len(headers):
        rows.append(cells)

# Create a DataFrame from the extracted data
df = pd.DataFrame(rows, columns=headers)

# Save the DataFrame to a CSV file
df.to_csv('draft_data.csv', index=False)

print("Data has been successfully scraped and saved to draft_data.csv")
