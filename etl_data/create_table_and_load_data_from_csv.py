import psycopg2 as pg
from psycopg2 import extras
import sys
import csv


# Returns a connection to the database.
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


# Creates the table land_temperatures. Return True if success and False otherwise.
def create_land_temperatures_db():
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
                    "temp_uncertainty" double precision, 
                    "latitude" text NOT NULL, 
                    "longitude" text NOT NULL,
                    UNIQUE (city_name, date)
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


# replace eventual empty values from a csv row by nulls. Modifies the argument.
def convert_empty_to_null(csv_row_dict):
    for k, v in csv_row_dict.items():
        if v == '':
            csv_row_dict[k] = None


# inserts data from a DictReader populated with data from GlobalLandTemperaturesByCity.csv
# into land_temperature table.
# parameters are a cursor for accessing the database, the DictReader row
def insert_many_rows_into_land_temperature(db_connection_cursor, values):
    try:
        extras.execute_values(db_connection_cursor, """
                        INSERT INTO land_temperature (date, city_name, country_name, avg_temp, 
                                                      temp_uncertainty, latitude, longitude)
                        VALUES %s;
                    """, values, page_size=len(values))

    except Exception as error:
        print(error)


# reads from GlobalLandTemperaturesByCity.csv and loads data into table land_temperature. Field
# names are: dt,AverageTemperature,AverageTemperatureUncertainty,City,Country,Latitude,Longitude
def load_data_from_csv(csv_path, batch_size=100000):
    try:
        postgres_connection = get_postgres_connection()
        cursor = postgres_connection.cursor()
        values = []

        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if len(values) == batch_size:
                    insert_many_rows_into_land_temperature(cursor, values)
                    postgres_connection.commit()
                    values = []
                    print(f'Processing line: {reader.line_num}')

                convert_empty_to_null(row)
                values.append((row['dt'], row['City'],
                               row['Country'], row['AverageTemperature'],
                               row['AverageTemperatureUncertainty'],
                               row['Latitude'], row['Longitude'],))
            
            # in case the number of rows is not a multiple of batch_size, we must process the last rows
            if len(values) > 0:
                insert_many_rows_into_land_temperature(cursor, values)
                postgres_connection.commit()

        cursor.close()
        postgres_connection.close()
        print('Finished loading data from csv')

    except Exception as error:
        print('Error while loading data from csv')
        print(error)


def etl(csv_path):
    create_land_temperatures_db()
    load_data_from_csv(csv_path)


# this script expects an argument containing the path to the csv file
if __name__ == '__main__':
    try:
        etl(sys.argv[1])
    except IndexError as _:
        print("this script expects one argument containing the path to GlobalLandTemperaturesByCity csv file")


