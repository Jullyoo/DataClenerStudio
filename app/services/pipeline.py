from app.services.cleaners import DataCleaner


class DataPipeline:

    def __init__(self, dataframe):

        self.cleaner = DataCleaner(
            dataframe
        )

    def execute(self):

        self.cleaner \
            .normalize_columns() \
            .clean_text() \
            .clean_dates() \
            .clean_currency() \
            .clean_nulls() \
            .validate_emails() \
            .remove_duplicates()

        return {

            'dataframe': self.cleaner.get_dataframe(),

            'history': self.cleaner.get_history()
        }