import requests
from bs4 import BeautifulSoup
import re

def parse_episode_input(episode_input):
    """
    Parse the episode input string into a set of valid episode numbers.
    Examples of valid input:
       - "all"
       - "1"
       - "1-10"
       - "1,2,3,7-10"
    Returns:
       - 'all' (string) if user wants all episodes
       - or a set of integers representing episodes.
    """
    if episode_input.lower() == "all":
        return "all"

    episodes = set()
    parts = episode_input.split(",")
    for part in parts:
        part = part.strip()
        # If it's a range like "1-5"
        if "-" in part:
            start, end = part.split("-")
            try:
                start = int(start.strip())
                end = int(end.strip())
                if start <= end:
                    episodes.update(range(start, end + 1))
                else:
                    # If reversed range, swap them or skip.
                    episodes.update(range(end, start + 1))
            except ValueError:
                # ignore if invalid
                pass
        else:
            # It's a single episode number
            try:
                num = int(part)
                episodes.add(num)
            except ValueError:
                # ignore if invalid
                pass

    return episodes

def scrape_links():
    # Step 1: Ask the user for inputs
    url = input("Enter the URL: ").strip()
    quality = input("Enter the desired quality (e.g. 540p, 720p, 1080p): ").strip()
    episode_input = input('Enter episode selection ("all", "1", "1-10", "1,2,3,7-10", etc.): ').strip()
    filename = input("Enter the name of the text file to save links (e.g. links.txt): ").strip()

    # Parse episode input
    requested_episodes = parse_episode_input(episode_input)

    try:
        # Step 2: Send a GET request to the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request was unsuccessful

        # Step 3: Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table body that contains the rows
        tbody = soup.find("tbody", {"id": "tbody"})
        if not tbody:
            print("Could not find the expected table body with id='tbody'.")
            return

        rows = tbody.find_all("tr", {"class": "editable"})

        # Step 4: Extract links from each row that match the chosen quality and episode selection
        matched_links = []
        for row in rows:
            a_tag = row.find("a")
            if not a_tag:
                continue

            link_text = a_tag.text.strip()
            link = a_tag.get("href", "")

            # 1) Check if the link text contains the desired quality
            if quality.lower() not in link_text.lower():
                continue

            # 2) Extract the episode number from the filename using regex, e.g. E01 or E02, ignoring case
            #    This regex looks for "E" followed by one or more digits.
            match = re.search(r'[Ee](\d+)', link_text)
            if not match:
                continue

            episode_num = int(match.group(1))  # Convert capture group to integer

            # 3) Check if the user wants "all" episodes or if the episode number is in the user's requested set
            if requested_episodes == "all" or episode_num in requested_episodes:
                # Convert to absolute URL if needed
                if link.startswith("/"):
                    # Replace 'https://buzzheavier.com' with the domain if different
                    link = "https://buzzheavier.com" + link

                matched_links.append(link)

        # Step 5: Write the links to the specified text file
        if matched_links:
            with open(filename, "w", encoding="utf-8") as f:
                for link in matched_links:
                    f.write(link + "\n")
            print(f"Successfully wrote {len(matched_links)} link(s) to {filename}.")
        else:
            print("No matching links found for the specified quality/episode selection.")

    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)

if __name__ == "__main__":
    scrape_links()
