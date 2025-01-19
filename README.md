# Episode Link Scraper

This repository provides a Python script that scrapes buzzheavier links uploaded by [SinFlix](https://rentry.co/sinflix) (with a known table structure) to extract links to episodes based on both **episode number** and **quality** (e.g. 540p, 720p, 1080p). The extracted links are then written to a user-specified text file. 

## Features

- **User Prompts**  
  - URL of the webpage containing the table of links.
  - Desired quality (e.g. `540p`, `720p`, or `1080p`).
  - Episode selection (e.g. `all`, `1`, `1-10`, or a comma-separated list like `1,2,3,7-10`).
  - Output filename (where the links will be saved).

- **Episode Filtering**  
  - Handles single episodes (e.g. `1`), ranges (`1-10`), multiple episodes/ranges combined (`1,2,3,7-10`), or **all** episodes.

- **Quality Filtering**  
  - Filters the scraped links to only those matching the chosen quality string.

- **Output**  
  - Writes one link per line into a specified text file.
  - Shows a success message if any matching links are found, or a message indicating no matches.

## How It Works

1. **Parse User Input**  
   The script prompts the user for:
   - **URL** – The page to scrape (e.g. `https://buzzheavier.com/p2pcpfjct7ty`).
   - **Quality** – The desired resolution (e.g. `540p`, `720p`, or `1080p`).
   - **Episode Selection**:
     - `all` (any case) → All episodes.
     - Single episode (e.g. `1`).
     - A range (e.g. `1-10`).
     - Multiple comma-separated values/ranges (e.g. `1,2,3,7-10`).
   - **Filename** – The name of the text file where matching URLs will be stored.

2. **Scrape the Page**  
   - Uses `requests` to fetch the HTML.
   - Parses the HTML with `BeautifulSoup`.
   - Searches for table rows (`<tr class="editable">`) within a specific table body (`<tbody id="tbody">`).

3. **Filter by Quality & Episode**  
   - Extracts the anchor text from each table row and checks if it contains the quality string (case-insensitive).
   - Finds the episode number in the filename using a regex pattern (`r"[Ee](\d+)"`).
   - Compares the episode number against the user’s requested episodes.

4. **Write to File**  
   - If any links match, they are written (one per line) to the chosen text file.
   - If none match, a corresponding message is displayed.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

Install dependencies with:
```
pip install -r requirements.txt
```
Run script with:
```
python buzz.py
```