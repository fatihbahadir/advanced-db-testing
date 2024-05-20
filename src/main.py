from core.application import App

def run():
    App().start()

def screen_test():

    from modules.screen.screen import Screen
    
    screen = Screen(
        app=None,
        geometry= "400x400",
        title="Form"
        )

    screen.start()

def database_test():
    
    from services.db_connector import DbConnector
    import pyodbc

    DbConnector.setup(
        dbname="AdventureWorks2012",
        user="fatih",
        password="123456",
        host="HPPOMEN\SQLEXPRESS"
    )


    conn, cursor = DbConnector.connect()

    cursor.execute("SELECT TOP 10 * FROM Person.Person")
    rows = cursor.fetchmany(10)
    for row in rows:
        print(row)
        
    DbConnector.disconnect(conn_data = (conn, cursor))
    

if __name__ == "__main__":
    run()
