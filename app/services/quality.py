import pandas as pd
import re


class DataQualityAnalyzer:

    @staticmethod
    def analyze(df):

        total_cells = df.shape[0] * df.shape[1]

        # NULLS

        total_nulls = df.isnull().sum().sum()

        completeness = round(

            (1 - (total_nulls / total_cells)) * 100,

            2
        )

        # DUPLICATES

        duplicates = df.duplicated().sum()

        uniqueness = round(

            (1 - (duplicates / len(df))) * 100,

            2
        )

        # EMAILS

        invalid_emails = 0

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        for column in df.columns:

            if 'email' in column.lower():

                invalid_emails += df[column].apply(

                    lambda x:

                    not bool(
                        re.match(email_pattern, str(x))
                    )

                    if pd.notna(x)

                    else False

                ).sum()

        validity = round(

            (
                1 -
                (
                    invalid_emails /
                    max(len(df), 1)
                )
            ) * 100,

            2
        )

        # SCORE FINAL

        final_score = round(

            (
                completeness * 0.4 +

                uniqueness * 0.3 +

                validity * 0.3
            ),

            2
        )

        return {

            'completeness': completeness,

            'uniqueness': uniqueness,

            'validity': validity,

            'duplicates': int(duplicates),

            'nulls': int(total_nulls),

            'invalid_emails': int(invalid_emails),

            'score': final_score
        }