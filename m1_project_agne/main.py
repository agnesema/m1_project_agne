from lxml.etree import HTML
from requests import get
import csv

base_url = "https://www.krepsinis.net/"
response = get(base_url)
tree = HTML(response.text)
# print(page.status_code)

def basketball_results(tree: HTML) -> list:
    scoreboard_data = []
    scoreboard_status = []
    leagues = []
    teams_home = []
    teams_away = []
    scores_home = []
    scores_away = []

    statuses_path = tree.xpath("//div[contains(@class, 'scoreboard-item-status')]/text()")
    leagues_path = tree.xpath("//div[contains(@class, 'scoreboard-item-info-league fl')]/text()")
    teams_home_path = tree.xpath("//div[contains(@class, 'scoreboard-item-info-team-name home')]/text()")
    teams_away_path = tree.xpath("//div[contains(@class, 'scoreboard-item-info-team-name away')]/text()")
    scores_home_path = tree.xpath("//div[contains(@class, 'scoreboard-item-info-team-score home')]/text()")
    scores_away_path = tree.xpath("//div[contains(@class, 'scoreboard-item-info-team-score away')]/text()")

    for status in statuses_path:
        scoreboard_status.append(status.replace("\n", ""))
    for league in leagues_path:
        leagues.append(league.replace("\n", ""))
    for team in teams_home_path:
        teams_home.append(team.replace("\n", ""))
    for team in teams_away_path:
        teams_away.append(team.replace("\n", ""))
    for score in scores_home_path:
        scores_home.append(score.replace("\n", ""))
    for score in scores_away_path:
        scores_away.append(score.replace("\n", ""))

    for i in range(len(scoreboard_status)):
        scoreboard_data.append({"Status": scoreboard_status[i], "League": leagues[i], "Team Home": teams_home[i],
                            "Score Home": scores_home[i], "Team Away": teams_away[i], "Score Away": scores_away[i]})
    return scoreboard_data




# def articles(data):
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

def extract_articles_data(tree: HTML, base_url: str):
    """
    Extracts a list of articles from https://www.krepsinis.net/ webpage.

    Args:
        tree (HTML): The HTML tree containing webpage information.
        base_url (str): The base URL used to construct complete URLs.

    Returns:
        List[Dict[str, Union[str, List[str]]]]: A list of dictionaries where each dictionary represents an article.
            Each dictionary has "title" as a string and "url" as a list of strings.

    Raises:
        ValueError: If there is an issue extracting the data.
    """
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

def search_in_articles(data, target_word):
    matching_articles = []

    for article in data:
        title = article.get("title", "").lower()
        if target_word.lower() in title:
            matching_articles.append(article)

    return matching_articles



#scoreboard_data = basketball_results(tree)
article_data = extract_articles_data (tree, base_url)
search_results = search_in_articles(article_data, 'ryt')
#write_data_to_csv(article_data, "articles9")
#write_data_to_csv(scoreboard_data, "results3")
write_data_to_csv(search_results, "search")


