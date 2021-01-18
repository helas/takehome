# takehome

This system is composed of:
- A postgres database running in a container (database container)
- A django + django restful framework running in a container (web-service container)
    - Data related to the web-service is available in the ws_data folder
    - ws_data is also the root of djangos project
    - Can be accessed through localhost:8000 in the host machine 
    - A very simple version of the docs of the api can be accessed localhost:8000/docs
- A very simple etl script that loads data to the db from a csv (loader container)
    - Data related to the loader is available in the etl_data folder
- A client api that executes the queries defined in the statement of the exercise (client container)
    - Data related to the client is available in the client_data folder
    
Deploying the system and running:
- scripts:
    - start_load_deploy_db_etl_ws.sh:
        - expect parameters arg1: csv_file_name, arg2: csv_file_path
        - start all db, loader and web-service containers. Loads data from csv, runs migrations on django.
    - run_taskhome_tasks.sh:
        - Runs the queries specified in the statement
        - It is expected to be run after the first script.  
    - docker-compose and Dockerfiles:
        - A docker-compose file for database, web-service and loader is located at the root of this project
        - A docker-compose file for the client is located under client_data
        - A Dockerfile for the database is available at the root
        - A Dockerfile for the client is available at client_data
        - A Dockerfile for the loader is available at etl_data
        
Implementation:
- challenges: 
    - automatizing: 
        - Integrating the loader and client with the db and ws and allowing then to be started and executed by docker was more complicated than expected.
        - Making the doc generator of the API generate content related to query and data parameters
    - Django Restful Framework:
        - Instead of using plain Django, I decided to give it a try on Django Restful Framework. I think the result is nice, but it took longer than expected
    - Tests for the client: As time was ticking fast, I couldn't properly test TakeHomeApiClient.
    - More details about project decisions and steps are available in action-log.txt in the root.
    - Tasks 4a, 4b and 4c: 
        - 4a: Max temp of 38.531 in city Abadan
        - 4b: Created new record with max temp 38.631 in month 2020-12-01
        - 4c: The new avg_temp is 36.131
    - hours:
        - Between 12 and 14 hours.

    