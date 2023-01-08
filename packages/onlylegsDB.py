import datetime
now = datetime.datetime.now()
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
            print(f"{now.hour}:{now.minute}:{now.second} - Connecting to database...")
            
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
                
                print(f"{now.hour}:{now.minute}:{now.second} - Done!\n")
        
        except Error as e:
            print("Error while connecting to Database!\nFull error:", e)
            print("Exiting...")
            sys.exit(1)
            
        self.database = database
        
    def initialize(self):
        dir = os.path.join('packages', 'tables')
        
        if not os.path.exists(dir+'/generate.sql'):
            print("Error: could not find tables directory")
            print("Exiting...")
            sys.exit(1)
        else:
            print(f"{now.hour}:{now.minute}:{now.second} - Initializing tables...")
            
        with open(dir+'/generate.sql', 'r') as f:
            sql = f.read()
            
            cursor = self.database.cursor()
            query = cursor.execute(sql, multi=True)

            for res in query:
                #print("Running query...")
                print(f"Affected {res.rowcount} rows")
                
            self.database.commit()
            
        if not os.path.exists(dir+'/junctions.sql'):
            print("Error: could not find junctions directory")
            print("Exiting...")
            sys.exit(1)
        else:
            print(f"{now.hour}:{now.minute}:{now.second} - Initializing junctions...")
            
        with open(dir+'/junctions.sql', 'r') as f:
            sql = f.read()
            
            cursor = self.database.cursor()
            query = cursor.execute(sql, multi=True)

            for res in query:
                #print("Running query...")
                print(f"Affected {res.rowcount} rows")
                
            self.database.commit()
        
        print(f"{now.hour}:{now.minute}:{now.second} - Done!\n")
    
    def getImage(self, id):
        sql = "SELECT * FROM posts WHERE id = %s"
        img = (id,)
        
        cursor = self.database.cursor()
        cursor.execute(sql, img)
        
        return cursor.fetchone()