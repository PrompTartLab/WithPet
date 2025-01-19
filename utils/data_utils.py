import sqlite3
import pandas as pd
import os


def load_csv_to_sqlite(csv_files, db_path=":memory:"):
    conn = sqlite3.connect(db_path)

    print(os.getcwd())

    for file_path, table_name in csv_files.items():
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, index=False, if_exists="replace")
            print(f"Loaded {file_path} into table '{table_name}'.")
        except Exception as e:
            print(f"Error loading {file_path} into table '{table_name}': {e}")

    return conn


def filter_csv_with_sql(query: str, conn):
    try:
        # Execute the SQL query
        result = pd.read_sql_query(query, conn)
        return result
    except Exception as e:
        return f"Error executing query: {e}"


def format_docs_with_metadata(docs):
    formatted_docs = []
    for i, doc in enumerate(docs):
        metadata_str = "\n".join(
            [
                f"{key}: {value}"
                for key, value in doc.metadata.items()
                if pd.notnull(value)
            ]
        )
        formatted_docs.append(f"<Data {i+1}>\n{metadata_str}\n{doc.page_content}")
    return "\n\n".join(formatted_docs)


def format_dataframe(df, data_source):
    formatted_docs = []
    for i, row in df.iterrows():
        metadata_str = "\n".join(
            [
                f"{column}: {row[column]}"
                for column in df.columns
                if pd.notnull(row[column])
            ]
        )
        formatted_docs.append(f"<Data {i+1}>\n{metadata_str}")
    return "\n\n".join(formatted_docs)
