from sqlalchemy import create_engine


class DataExporter:

    @staticmethod
    def csv(df, path):

        df.to_csv(
            path,
            index=False
        )

    @staticmethod
    def excel(df, path):

        df.to_excel(
            path,
            index=False
        )

    @staticmethod
    def parquet(df, path):

        parquet_df = df.copy()

        for column in parquet_df.columns:

            if parquet_df[column].dtype == 'object':

                parquet_df[column] = (
                    parquet_df[column]
                    .astype(str)
                )

        parquet_df.to_parquet(
            path,
            index=False
        )

    @staticmethod
    def sql(
        df,
        connection_string,
        table_name
    ):

        engine = create_engine(
            connection_string
        )

        df.to_sql(
            table_name,
            engine,
            if_exists='replace',
            index=False
        )

    @staticmethod
    def sql_file(
        df,
        path,
        table_name='cleaned_data'
    ):

        with open(
            path,
            'w',
            encoding='utf-8'
        ) as f:

            columns = ", ".join(df.columns)

            for _, row in df.iterrows():

                values = []

                for value in row:

                    if value is None:

                        values.append(
                            'NULL'
                        )

                    else:

                        safe_value = str(value)

                        safe_value = safe_value.replace(
                            "'",
                            "''"
                        )

                        values.append(
                            f"'{safe_value}'"
                        )

                values = ", ".join(values)

                f.write(

                    f"INSERT INTO "
                    f"{table_name} "
                    f"({columns}) "
                    f"VALUES ({values});\n"

                )