import sys
import os

class DBmanager():
    def __init__(self):
        try:
            import mysql.connector
            from mysql.connector import Error
            from dotenv import load_dotenv
        except ImportError:
            print("Error: could not import required modules")
            sys.exit(1)
        
        try:
            load_dotenv(os.path.join('usr', '.env'))
            
            print("Connecting to MySQL database...")
            
            database = mysql.connector.connect(host=os.environ.get('HOST'),
                                            port=os.environ.get('PORT'),
                                            database=os.environ.get('DATABASE'),
                                            user=os.environ.get('USERNAME'),
                                            password=os.environ.get('PASSWORD')
                                            )
            
            if database.is_connected():
                db_Info = database.get_server_info()
                print("Connected to MySQL Server version:", db_Info)
                
                cursor = database.cursor()
                cursor.execute("select database();")
                
                record = cursor.fetchone()
                print("Connected to database:", record[0])
        
        except Error as e:
            print("Error while connecting to MySQL!\n", e)
            sys.exit(1)
            
        self.database = database
        
    def cursor(self):
        return self.database.cursor()
    
    def getImage(self, id):
        sql = "SELECT * FROM images WHERE id = %s"
        img = (id,)
        
        cursor = self.cursor()
        cursor.execute(sql, img)
        
        return cursor.fetchone()