class DataProfiler:

    @staticmethod
    def analyze(df):

        report = {

            'rows': len(df),

            'columns': len(df.columns),

            'duplicates': int(
                df.duplicated().sum()
            ),

            'nulls': df.isnull().sum().to_dict(),

            'types': df.dtypes.astype(str).to_dict(),

            'unique_values': {

                column: int(df[column].nunique())

                for column in df.columns
            }
        }

        return report