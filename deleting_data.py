import sqlalchemy

def deleteRow(rows_num):
    while rows_num > 233:
        dele = sqlalchemy.text("DELETE FROM btcusdt WHERE open IN (SELECT open FROM btcusdt LIMIT 1)")
        engine.execute(dele)
        rows_num -= 1
        

#creating engine
engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\Michal\\Desktop\\Portfolio_Projects\\Trading_bot\\BTCUSDTsource.db')

# checking uf table exists and has enough rows to start deleting
if sqlalchemy.inspect(engine).has_table('btcusdt'):
    connection = engine.connect()
    my_query = sqlalchemy.select([sqlalchemy.func.count()]).select_from(sqlalchemy.text('btcusdt')) #COUNT rows
    rows_num = connection.execute(my_query).fetchall()[0][0]
    deleteRow(rows_num)

    # sql = sqlalchemy.text("SELECT * from btcusdt")
    
    # # Fetch all the records
    # result = engine.execute(sql).fetchall()
    
    # # View the records
    # for record in result:
    #     print("\n", record)

 
