from lxml.etree import HTML
from requests import get
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

base_url = "https://www.krepsinis.net/"
response = get(base_url)
tree = HTML(response.text)
# print(page.status_code)

def extract_articles_data(base_url: str, time_limit: int = 60):
    """
    Extracts a list of articles from https://www.krepsinis.net/ webpage with scrolling.

    Args:
        base_url (str): The base URL used to construct complete URLs.
        time_limit (int): The maximum time in seconds allowed for the function to run.

    Returns:
        List[Dict[str, Union[str, List[str]]]]: A list of dictionaries where each dictionary represents an article.
            Each dictionary has "title" as a string and "url" as a list of strings.

    Raises:
        ValueError: If there is an issue extracting the data or if the time limit is exceeded.
    """
    # Set up a headless browser with Selenium
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:
        start_time = time.time()

        driver.get(base_url)
        def scroll_down(driver):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        while time.time() - start_time < time_limit:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            scroll_down(driver)

        page_source = driver.page_source
        tree = HTML(page_source)

        articles = tree.xpath("//a[@class='a-text']")
        article_data = []

        for article in articles:
            title_list = article.xpath("text()")
            title = ' '.join(title.strip() for title in title_list) if title_list else None

            url = [base_url + str(article.xpath("@href") if article.xpath("@href") else None).replace("['/", "").replace("']", "")]

            if title and url:
                article_data.append({"title": title, "url": url})
            else:
                raise ValueError("Error extracting title or URL for an article.")

        return article_data

    except Exception as e:
        raise ValueError(f"Error during extraction: {e}")

    finally:
        driver.quit()

def search_in_articles(data, target_word):
    matching_articles = []

    for article in data:
        title = article.get("title", "").lower()
        if target_word.lower() in title:
            matching_articles.append(article)

    return matching_articles

def write_data_to_csv(data: dict, filename: str) -> None:
    """
       Write a list of dictionaries to a CSV file.

       Args:
           data (List[Dict[str, str]]): A list of dictionaries where each dictionary represents a data row.
                                        The keys are the field names, and the values are the corresponding values.
           filename (str): The name of the CSV file to be created.

       Returns:
           None: This function does not return a value.

       Raises:
           ValueError: If the 'data' list is empty.
       """
    if not data:
        raise ValueError("No data to write.")

    csv_file = filename + ".csv"
    fieldnames = list(data[0].keys())

    with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


#scoreboard_data = basketball_results(tree)
#article_data = extract_articles_data (tree, base_url)
#search_results = search_in_articles(article_data, 'ryt')
#write_data_to_csv(article_data, "articles")
#write_data_to_csv(scoreboard_data, "results3")
#write_data_to_csv(search_results, "search")
time_limit_seconds = 10
articles_data = extract_articles_data(base_url, time_limit_seconds)
write_data_to_csv(articles_data, 'articles1')

