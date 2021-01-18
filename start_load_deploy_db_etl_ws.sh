# $1: csv_file_name
# $2: csv_file_path

export CSV_FILE_NAME=$1
export PATH_TO_CSV_FOLDER=$2

docker network create external-network
docker-compose up --build