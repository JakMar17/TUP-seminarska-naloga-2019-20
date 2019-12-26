import pyodbc 

mssql_connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};\
    SERVER=tcp:localhost,7201;\
    DATABASE=master;\
    UID=sa;\
    PWD=root_ROOT'
)
mssql_cursor = mssql_connection.cursor()

print(cursor)