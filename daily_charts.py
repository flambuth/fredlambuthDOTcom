import sqlite3
from data_definition import make_insert_query, query_db
from data_definition import table_schemas, database

from fred_spotify import today_top_chart, JSON_to_listofDicts

class Daily_Table:
    def __init__(self, table):
        self.table = table
        self.latest_date = query_db(f'select MAX(date) from {self.table}')[0][0]
        self.col_names = [i[0] for i in  table_schemas[self.table]]
        #self.all_charts = query_db(f'select * from {table};')
        #self.art_names_in_charts = sorted(list(set([i[3] for i in self.all_charts])))

    def traffic_check(self, new_daily):
        '''
        Uses the tuple that comes from parse_daily_JSON, but with the * to unpack it
        '''
        if self.latest_date < new_daily[0][-1]:
            return True
        

    def insert_new_daily(self, new_daily):
        '''
        the new_daily should be a Spotifies.daily_insert.daily_book
        '''
        #new_date = new_daily[0]['date']
        query = make_insert_query(self.table, self.col_names)

        if self.traffic_check(new_daily):
            sqliteConnection = sqlite3.connect(database)
            cursor = sqliteConnection.cursor()
            #executemany takes a lists of lists, not the usualy dictionary of lists
            cursor.executemany(query, new_daily)
                
            sqliteConnection.commit()
            cursor.close()
            sqliteConnection.close()

        else:
            print('Failed Traffic Stop')

        print(f'{self.table} has been updated to {new_daily[0][-1]}')

    def update_daily_table(self):
        json_today = today_top_chart(self.table)
        dict_today = JSON_to_listofDicts(json_today, self.table)
        listo_for_db = [list(i.values()) for i in dict_today]
        self.insert_new_daily(listo_for_db)
