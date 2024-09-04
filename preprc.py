import pandas as pd

class PreProcessor:
    def __init__(self, file_name: str):
        self.model: pd.DataFrame = pd.read_csv(f'./res/{file_name}.csv')

    def remove_non_roman_character(self):
        for (_, row) in self.model.iterrows():
            content = row['content']
            for c in content:
                if not (c <= 'z' or c >= 'a') and not (c <= 'Z' or c >= 'A'):
                    content = content.replace(c, '')

    def remove_stop_words(self):
        pass

    def remove_html_tags(self):
        for (_, row) in self.model.iterrows():
            content = row['content']
            content = content.replace('<br>', '')
            content = content.replace('<br/>', '')
            content = content.replace('<br />', '')
        pass

    def remove_emojis(self):
        pass

    def remove_numbers(self):
        pass

    def remove_extra_spaces(self):
        pass

