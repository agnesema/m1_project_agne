from io import StringIO
from m1_project_agne import krepsinis


def crawl():
    base_url = "https://www.krepsinis.net"
    time_limit_seconds = 60
    query = "žalgir"

    try:
        articles_data = krepsinis.crawl_krepsinis(base_url, time_limit_seconds, query)
        krepsinis.write_data_to_csv(articles_data, "articles1")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    crawl()

# if __name__ == "__main__":
#     #scoreboard_data = basketball_results(tree)
#     #article_data = extract_articles_data (tree, base_url)
#     #search_results = search_in_articles(article_data, 'ryt')
#     #write_data_to_csv(article_data, "articles")
#     #write_data_to_csv(scoreboard_data, "results3")
#     #write_data_to_csv(search_results, "search")
#     time_limit_seconds = 5
#
#     articles_data = extract_articles_data(base_url, time_limit_seconds, "Žalgir")
#     #images_data = extract_article_images(webdriver.Chrome, articles_data)
#     write_data_to_csv(articles_data, "articles3")
#
#     #print(images_data)
