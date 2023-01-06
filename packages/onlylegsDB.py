import time
import sys
import os

class DBmanager():
    def __init__(self):
        try:
            import mysql.connector
            from mysql.connector import Error
            from dotenv import load_dotenv
        except ImportError:
            print("Error: could not import required packages")
            sys.exit(1)
        
        try:
            env_path = os.path.join('usr', '.env')
            
            if not os.path.exists(env_path):
                print("Error: could not find .env file")
                print("Exiting...")
                sys.exit(1)
            
            load_dotenv(env_path)
            print("### OnlyLegs Database Manager ###")
            print("Connecting to database...")
            
            database = mysql.connector.connect(host=os.environ.get('DB_HOST'),
                                            port=os.environ.get('DB_PORT'),
                                            database=os.environ.get('DB_NAME'),
                                            user=os.environ.get('DB_USER'),
                                            password=os.environ.get('DB_PASS')
                                            )
            
            if database.is_connected():
                db_Info = database.get_server_info()
                print("Connected to MySQL Server version:", db_Info)
                
                cursor = database.cursor()
                cursor.execute("select database();")
                
                record = cursor.fetchone()
                print("Connected to database:", record[0])
                
                print("Done!\n")
        
        except Error as e:
            print("Error while connecting to Database!\nFull error:", e)
            print("Exiting...")
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