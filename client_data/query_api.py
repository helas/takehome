import requests
from datetime import datetime
from datetime import timedelta


class TakeHomeApiClient:

    # Calculate result of task 4a
    def highest_average_temperature_since_2000(self):
        # first, using the params bellow, we ask our API for the highest temperatures per city since 2000
        now = datetime.now()
        params = {'start_date': '2000-01-01',
                  'end_date': now.strftime('%Y-%m-%d'), 'aggregation': 'max',
                  'n_results': '1'}
        response = requests.get('http://web-service:8000/land_temperatures/', params=params)

        # then, if the request worked, we filter out the highest temperature.
        max_record = {}
        if response.status_code == 200:
            results = response.json()
            for result in results:
                avg_temp = result.get('avg_temp', None)
                if max_record == {} or (avg_temp is not None and avg_temp > max_record['avg_temp']):
                    max_record = result

            # at this point, either we have a max_record, either the response was empty.
            if max_record:
                print(f'Max temp of {max_record["avg_temp"]} in city {max_record["city_name"]}')
            else:
                print(f'No records are available in that period')
            return max_record

        return None

    # Calculate result of task 4b
    def create_new_entry_for_record_city(self, max_record):
        # first we findout which month was last month and compose the data that we want to create
        now = datetime.now()
        last_month = now - timedelta(days=30)
        max_record['date'] = f'{last_month.year}-{last_month.month}-01'
        max_record['avg_temp'] += 0.1

        # we issue the request and return the new record
        response = requests.post('http://web-service:8000/land_temperatures/', data=max_record)
        if response.status_code == 201:
            print(f'Created new record with max temp {max_record["avg_temp"]} in month {max_record["date"]}')
            return response.json()
        elif response.status_code == 400:
            print('The request is not well formed. Cannot continue.')
        return None

    # Calculate result of task 4c
    def create_update_entry_for_record_city(self, wrong_record):
        params = {'city_name': wrong_record['city_name'], 'date': wrong_record['date']}
        data = {'avg_temp': wrong_record['avg_temp'] - 2.5}

        response = requests.put(f'http://web-service:8000/land_temperature/{params["city_name"]}/{params["date"]}',
                                data=data)
        if response.status_code == 200:
            print(f'Successfully updated the record. The new avg_temp is {data["avg_temp"]}')
        else:
            print(f'There was an issue: {response.status_code}')

    def run_exercises(self):
        max_avg_record = self.highest_average_temperature_since_2000()
        if max_avg_record:
            wrong_record = self.create_new_entry_for_record_city(max_avg_record)
            if wrong_record:
                self.create_update_entry_for_record_city(wrong_record)


if __name__ == '__main__':
    client = TakeHomeApiClient()
    client.run_exercises()

