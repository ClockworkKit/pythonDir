import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Define base URL for the spells list page
base_url = "https://www.d20srd.org/indexes/spells.htm"  # Replace with actual URL of spell list page

# Connect to SQLite database (it will create if it doesn't exist)
conn = sqlite3.connect('dnd_3.5e_spells.db')
cursor = conn.cursor()

# Create a table for spells
cursor.execute('''
CREATE TABLE IF NOT EXISTS spells (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    level TEXT NOT NULL,
    school TEXT NOT NULL,
    range TEXT NOT NULL,
    duration TEXT NOT NULL,
    description TEXT NOT NULL
)
''')

# Function to extract data from each spell page
def extract_spell_data(spell_url):
    response = requests.get(spell_url)
    spell_soup = BeautifulSoup(response.content, "html.parser")

    # Example extraction (selectors will vary based on site structure)
    spell_name = spell_soup.find("h1").get_text()
    level = spell_soup.find("div", class_="level").get_text()
    school = spell_soup.find("div", class_="school").get_text()
    range_ = spell_soup.find("div", class_="range").get_text()
    duration = spell_soup.find("div", class_="duration").get_text()
    description = spell_soup.find("div", class_="description").get_text()

    # Insert data into the database
    cursor.execute('''
    INSERT INTO spells (name, level, school, range, duration, description)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (spell_name, level, school, range_, duration, description))
    
    conn.commit()  # Commit the changes to the database

# Main function to retrieve spell URLs and scrape data
def main():
    response = requests.get(f"{base_url}/spells")
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all links to individual spells
    spell_links = soup.find_all("a", class_="spell-link")  # Adjust selector as needed

    for link in spell_links:
        spell_url = base_url + link.get("href")
        extract_spell_data(spell_url)
        time.sleep(1)  # Be respectful of the server

# Run the crawler
if __name__ == "__main__":
    main()

# Close the database connection after all spells have been added
conn.close()
