import unittest
from unittest.mock import patch
import pandas as pd
from m1_project_agne import krepsinis
from m1_project_agne import main

class TestCrawlKrepsinis(unittest.TestCase):
    @patch('m1_project_agne.krepsinis.webdriver.Chrome')
    def test_crawl_krepsinis_no_search_word(self, mock_driver):
        mock_instance = mock_driver.return_value
        # Providing HTML content based on the expected structure
        mock_instance.page_source = """
             <html>
                 <body>
                     <a class='a-text' href='article1.html'>Title 1</a>
                     <a class='a-text' href='article2.html'>Title 2</a>
                 </body>
             </html>
         """

        result = krepsinis.crawl_krepsinis(base_url="https://www.example.com", time_limit=5)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty, "The DataFrame should not be empty.")

        expected_columns = ["title", "url", "image"]
        for column in expected_columns:
            self.assertIn(column, result.columns, f"Column '{column}' not found in DataFrame columns: {result.columns}")

    @patch('m1_project_agne.krepsinis.webdriver.Chrome')
    def test_crawl_krepsinis_with_search_word(self, mock_driver):
        mock_instance = mock_driver.return_value
        # Providing HTML content based on the expected structure
        mock_instance.page_source = """
               <html>
                   <body>
                       <a class='a-text' href='article1.html'>Title with search word</a>
                       <a class='a-text' href='article2.html'>Title without search word</a>
                       <a class='a-text' href='article3.html'>Another title with search word</a>
                   </body>
               </html>
           """

        search_word = "search"

        result = krepsinis.crawl_krepsinis(base_url="https://www.example.com", time_limit=5, search_word=search_word)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)

        for title in result['title']:
            self.assertIn(search_word, title.lower(),
                          f"Search word '{search_word}' not found in article title: {title}")
    @patch('m1_project_agne.krepsinis.crawl_krepsinis')
    def test_crawl_function(self, mock_crawl_krepsinis):
        # Set up mock data for crawl_krepsinis
        mock_data = pd.DataFrame({
            'title': ['Article 1', 'Article 2', 'Article 3'],
            'url': ['https://example.com/1', 'https://example.com/2', 'https://example.com/3'],
            'image': ['https://example.com/img1.jpg', 'https://example.com/img2.jpg',
                          'https://example.com/img3.jpg']
        })


        mock_crawl_krepsinis.return_value = mock_data


        result_csv = main.crawl(source='krepsinis', return_format='csv')
        result_df = main.crawl(source='krepsinis', return_format='df')
        result_records = main.crawl(source='krepsinis', return_format='records')


        self.assertIsInstance(result_csv, str)
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIsInstance(result_records, list)


        expected_columns = ['title', 'url', 'image']
        self.assertListEqual(list(result_df.columns), expected_columns)

        for record in result_records:
            self.assertIsInstance(record, dict)
            self.assertSetEqual(set(record.keys()), set(expected_columns))


if __name__ == '__main__':
    unittest.main()