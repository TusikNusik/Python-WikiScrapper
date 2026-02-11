from scrapper import WikiScrapper
import re
from collections import Counter
import os
import pandas as pd
import json
from wiki_errors import BrokenContainerError
import time

class WikiController():
    def __init__(self, wiki_url):
        self.wiki_url = wiki_url
        self.scrapper = WikiScrapper(wiki_url)
        self.visited_phrases = set()

    def summary(self, phrase):
        self.scrapper.scrape(phrase=phrase)
        print(self.scrapper.get_summary())

    def table(self, phrase, number, first_row_header=False):
        self.scrapper.scrape(phrase=phrase)
        pandas_table = self.scrapper.get_table(number, first_row_header)
        
        filename = f"{phrase}.csv"
        pandas_table.to_csv(filename, encoding='utf-8')

        raw_data = pandas_table.iloc[:, 1:].to_numpy().flatten()
        series = pd.Series(raw_data)
        
      
        counts_table = series.value_counts().reset_index()
        counts_table.columns = ["Value", "Count"]
        
        print(counts_table)
        
    def count_words(self, phrase):
        self.scrapper.scrape(phrase=phrase)
        phrase_content = self.scrapper.get_words()
        phrase_content = phrase_content.lower()
        word_list = re.findall("\w+", phrase_content)
         
        current_counts = Counter(word_list)
        counts_path = "./word-counts.json"
        all_counts = Counter()

        if os.path.exists(counts_path):
            with open(counts_path) as f:
                data = json.load(f)
                all_counts = Counter(data)
           
        all_counts.update(current_counts)
        with open(counts_path, 'w') as f:
            json.dump(dict(all_counts), f, ensure_ascii=False, indent=2)
        
    def auto_count_words(self, current_phrase, n, t):
        print(current_phrase)
        self.scrapper.scrape(phrase=current_phrase)
        self.count_words(phrase=current_phrase)
        self.visited_phrases.add(current_phrase)
        time.sleep(t)

        if n > 0:   
            all_links_and_phrases = self.scrapper.get_all_links()

            for _, phrase in all_links_and_phrases:
                if phrase not in self.visited_phrases:
                    self.auto_count_words(phrase, n - 1, t)            
                    


if __name__ == "__main__":
    try:
        controller = WikiController("https://bulbapedia.bulbagarden.net/wiki")
        #controller.table("Type", 1, True)
        #controller.count_words("charizard")
        controller.auto_count_words("Chain breeding", 2, 5)
    except Exception as e:
        print(f"Błąd: {e}")