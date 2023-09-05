import configparser
import os
import traceback

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

import logger


class DataProcessor:
    def __init__(self, file_path):
        logger.info('Reading the data file and converting data')
        self.data = pd.read_csv(file_path, delimiter=';')
        self.data['код'] = self.data['код'].astype(str)
        self.data = self.data.fillna('')
        self.years = self.data.columns[2:]
        self.new_data = pd.DataFrame(columns=['проект'] + list(self.years))

    def traverse_tree(self, code, project):
        logger.debug('Get all child vertices for a given code')
        children = self.data[self.data['код'].str.startswith(code + '.')]
        logger.debug('If there are no child nodes, record the project and values ​​by year')
        if children.empty:
            new_row = {'проект': project}
            for year in self.years:
                new_row[year] = self.data[self.data['код'] == code][year].values[0]
            self.new_data.loc[len(self.new_data)] = new_row
        else:
            logger.debug('If there are child vertices, traverse each vertex recursively')
            for i, row in children.iterrows():
                self.traverse_tree(row['код'], project + row['проект'])

    def process_data(self):
        logger.debug('Call the traverse_tree() function for each node in the tree')
        root_codes = self.data[self.data['код'].str.count('.') == 0]['код'].values
        for code in root_codes:
            self.traverse_tree(code, '')


class DatabaseConnector:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def create_table(self):
        logger.info('Create the table')
        conn = psycopg2.connect(
            database=self.database, user=self.user, password=self.password,
            host=self.host, port=self.port
            )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE projects (
                id SERIAL PRIMARY KEY,
                project VARCHAR(100),
                year_2022 FLOAT,
                year_2023 FLOAT,
                year_2024 FLOAT,
                year_2025 FLOAT
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

    def insert_data(self, new_data):
        logger.info('Entering data into a table')
        engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
        new_data = new_data.rename(columns={
            'проект': 'project', '2022': 'year_2022', '2023': 'year_2023',
            '2024': 'year_2024', '2025': 'year_2025'
            })
        new_data.to_sql('projects', engine, if_exists='append', index=False)


if __name__ == "__main__":
    currentdir = os.path.dirname(os.path.abspath(__file__))
    logger = logger.get_logger(__name__)
    config = configparser.ConfigParser()
    config.read(currentdir + "\\" + "settings.ini", encoding='utf-8')
    data_file = config.get("Data", "data_file")
    file_path = currentdir + '//' + data_file
    logger.info(f'data_file:{file_path}')
    database = config.get("DB", "database_name")
    user = config.get("DB", "user")
    password = config.get("DB", "password")
    host = config.get("DB", "host")
    port = config.get("DB", "port")
    logger.debug(f'database:{database}, host:{host}, port: {port}')

    try:
        data_processor = DataProcessor(file_path)
        data_processor.process_data()
        db_connector = DatabaseConnector(database, user, password, host, port)
        db_connector.create_table()
        db_connector.insert_data(data_processor.new_data)
    except Exception:
        logger.critical(traceback.format_exc())
        raise

    logger.info('Complete')
