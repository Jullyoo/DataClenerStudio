import pandas as pd
import re

from ftfy import fix_text
from unidecode import unidecode

from app.services.history import TransformationHistory


class DataCleaner:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

        self.snapshots = []

        self.history = TransformationHistory()

    def save_snapshot(self):

        self.snapshots.append(
            self.df.copy()
        )

    def undo(self):

        if self.snapshots:

            self.df = self.snapshots.pop()

        return self

    def clean_text(self):

        self.save_snapshot()

        before = self.df.shape

        def normalize(value):

            if pd.isna(value):

                return value

            value = str(value)

            value = fix_text(value)

            value = unidecode(value)

            value = value.strip()

            value = re.sub(
                r'\s+',
                ' ',
                value
            )

            value = re.sub(
                r'[^a-zA-Z0-9\s@.-]',
                '',
                value
            )

            return value

        for column in self.df.select_dtypes(include='object'):

            self.df[column] = self.df[column].apply(
                normalize
            )

        after = self.df.shape

        self.history.add_action(

            'clean_text',

            before,

            after
        )

        return self

    def clean_dates(self):

        self.save_snapshot()

        before = self.df.shape

        for column in self.df.columns:

            if any(keyword in column.lower() for keyword in [
                'data',
                'date'
            ]):

                self.df[column] = pd.to_datetime(
                    self.df[column],
                    errors='coerce'
                )

        after = self.df.shape

        self.history.add_action(

            'clean_dates',

            before,

            after
        )

        return self

    def clean_currency(self):

        self.save_snapshot()

        before = self.df.shape

        for column in self.df.columns:

            if any(keyword in column.lower() for keyword in [
                'valor',
                'preco',
                'salario',
                'renda',
                'custo',
                'price'
            ]):

                self.df[column] = (
                    self.df[column]
                    .astype(str)
                    .str.replace(',', '.', regex=False)
                    .str.replace(r'[^0-9.-]', '', regex=True)
                )

                self.df[column] = pd.to_numeric(
                    self.df[column],
                    errors='coerce'
                )

                self.df[column] = self.df[column].fillna(0)

        after = self.df.shape

        self.history.add_action(

            'clean_currency',

            before,

            after
        )

        return self

    def clean_nulls(self):

        self.save_snapshot()

        before = self.df.shape

        for column in self.df.columns:

            if pd.api.types.is_datetime64_any_dtype(
                self.df[column]
            ):

                self.df[column] = self.df[column].fillna(
                    pd.Timestamp("1970-01-01")
                )

            elif self.df[column].dtype == 'object':

                self.df[column] = self.df[column].fillna(
                    'Nao informado'
                )

            else:

                self.df[column] = self.df[column].fillna(0)

        after = self.df.shape

        self.history.add_action(

            'clean_nulls',

            before,

            after
        )

        return self

    def normalize_columns(self):

        self.save_snapshot()

        before = self.df.shape

        self.df.columns = [

            unidecode(col)
            .lower()
            .strip()
            .replace(' ', '_')

            for col in self.df.columns
        ]

        after = self.df.shape

        self.history.add_action(

            'normalize_columns',

            before,

            after
        )

        return self

    def validate_emails(self):

        self.save_snapshot()

        before = self.df.shape

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        for column in self.df.columns:

            if 'email' in column.lower():

                self.df[column] = self.df[column].apply(

                    lambda x:

                    x if pd.isna(x) or re.match(email_pattern, str(x))

                    else 'Email invalido'
                )

        after = self.df.shape

        self.history.add_action(

            'validate_emails',

            before,

            after
        )

        return self

    def remove_duplicates(self):

        self.save_snapshot()

        before = self.df.shape

        self.df = self.df.drop_duplicates()

        after = self.df.shape

        self.history.add_action(

            'remove_duplicates',

            before,

            after
        )

        return self

    def get_history(self):

        return self.history.get_history()

    def get_dataframe(self):

        return self.df