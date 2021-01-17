import psycopg2 as pg


def get_postgres_connection():
    try:
        return pg.connect(
            database='takehome_ws_db',
            user='postgres',
            password='postgres',
            host='database'
        )
    except Exception as error:
        print('Error while connecting')
        print(error)


def create_schema():
    try:
        postgres_connection = get_postgres_connection()
        cursor = postgres_connection.cursor()
        cursor.execute("""                        
                CREATE TABLE IF NOT EXISTS land_temperature (
                    "id" serial NOT NULL PRIMARY KEY,
                    "date" date NOT NULL,
                    "city_name" text NOT NULL,
                    "country_name" text NOT NULL,
                    "avg_temp" double precision, 
                    "avg_uncertainty" double precision, 
                    "latitude" double precision NOT NULL, 
                    "longitude" double precision NOT NULL                
                );    
            """
                       )
        postgres_connection.commit()
        cursor.close()
        postgres_connection.close()
        print("Schema was created or it already exists")
        return True

    except Exception as error:
        print('Error while creating db')
        print(error)
        return False


def etl():
    create_schema()


if __name__ == '__main__':
    etl()


