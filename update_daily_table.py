from daily_charts import Daily_Table

def update_tables_daily():
   
   #avengers!
    table1 = Daily_Table('daily_tracks')
    table2 = Daily_Table('daily_artists')

    #assemble!
    table1.update_daily_table()
    table2.update_daily_table()

if __name__ == '__main__':
    update_tables_daily()
