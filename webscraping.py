"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Petr Hlisnikovský

email: hlisnikovskyp@gmail.com

discord: bG.#6985

"""

import requests
from bs4 import BeautifulSoup as bs
import csv
import sys


def retrieve_municipalities(url):
    """
    Retrieves the code, name, and URL for each municipality
    from the URL provided when the program is run.

    :param url: URL of the selected district
    :return: List of data for all municipalities
    """
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    all_tables = soup.find_all('table', class_='table')
    mun_results = []

    for table in all_tables:
        for row in table.find_all('tr')[2:]:  # Skip the header
            cols = row.find_all('td')

            try:
                detail_url = cols[0].find('a')['href']

            except (TypeError):
                continue

            mun_result = {
                'code': cols[0].text.strip(),  # Municipality code
                'municipality': cols[1].text.strip(),  # Municipality name
                'detail_url': detail_url,  # URL to detailed municipality results
                }
            mun_results.append(mun_result)

    return mun_results

# Function to retrieve election results for a specific municipality
def retrieve_municipality_results(detail_url):
    base_url = 'https://www.volby.cz/pls/ps2017nss/'
    full_url = base_url + detail_url  # Full url for municipality detail results
    response = requests.get(full_url)
    soup = bs(response.text, 'html.parser')

    all_tables = soup.find_all('table', class_='table')

    general_data = {}
    party_results = {}

    for table in all_tables:
        rows = table.find_all('tr')[2:]  # Skip the header
        if table.get('id') == 'ps311_t1':
            general_data.update({
                'registered': rows[0].find_all('td')[3].text.strip(),
                'envelopes': rows[0].find_all('td')[4].text.strip(),
                'valid': rows[0].find_all('td')[7].text.strip(),
            })
        else:
            party_results.update({
                tds[1].text.strip(): tds[2].text.strip()
                for row in rows if (tds := row.find_all('td'))
            })

    # Combination of general results and party results into one dictionary
    combined_data = {**general_data, **party_results}
    return combined_data

def process_municipalities(url):
    """
    Retrieves and processes election results
    for all municipalities from the given URL.

    :param url: URL of the selected district
    :return: List of data for all municipalities
    """

    # Retrieving the list of municipalities
    munis = retrieve_municipalities(url)

    # Creating a list for all data
    all_data = []

    # Processing input data for each municipality (code, name, URL)
    for muni in munis:
        code = muni['code']
        municipality = muni['municipality']
        detail_url = muni['detail_url']

        # Informing about data retrieval
        # The longest municipality name in the Czech Republic has 33 characters
        print(f"\rRetrieving results for the municipality: {municipality:^33} "
        f"(code: {code})", end='', flush=True)


        # Retrieving election results for a specific municipality
        results_munis = retrieve_municipality_results(detail_url)

        # Storing all data into a single record
        muni_data = {
            'code': code,
            'municipality': municipality,
            'registered': results_munis.get('registered'),
            'envelopes': results_munis.get('envelopes'),
            'valid': results_munis.get('valid'),
            **{party: votes for party, votes in results_munis.items()
            }
        }
              
        # Adding the record to the all_data list
        all_data.append(muni_data)

    # Creating an empty string to remove the last output
    print(f"\r" + " " * 90 + "\r", end='', flush=True)
    print(f"\rData for the selected district has been successfully downloaded.")

    return all_data

# Exporting data to CSV
def export_to_csv(all_data, output_filename):
    """
    Exports the retrieved data to a CSV file.

    :param all_data: List of data for export
    :param output_filename: Output filename
    """
    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        # Creating the header from the keys of the first record
        fieldnames = all_data[0].keys() if all_data else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Writing the header
        writer.writeheader()

        # Writing the data
        writer.writerows(all_data)

    print(f"Data has been successfully exported to the file {output_filename}.")

# Function for checking the entered URL
def connection_test(url):
    test_url = 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj='

    # Checking if the provided URL starts with test_url
    if not url.startswith(test_url):
        print(f"ERROR: The specified address is not valid.")
        sys.exit()

    conn_check = requests.get(url)
    if conn_check.status_code != 200:
        print(f"The specified address is not accessible. \
        Error code {conn_check.status_code}")
        sys.exit()
    else:
        print(f"Connection was successful.\n", end='', flush=False)

# main function to run the program
def main_program(url, output_filename):

    connection_test(url)
    all_data = process_municipalities(url)
    export_to_csv(all_data, output_filename)

if __name__ == "__main__":

    url = sys.argv[1]  # First argument as URL of the selected district
    output_filename = sys.argv[2]  # Second argument as the output filename

    # Checking the number of arguments (1 script + 2 arguments)
    if len(sys.argv) != 3:
        print("USE: python webscraping.py <url> <output_filename>")
        sys.exit(1)

    # Checking the order of arguments and the output file format
    if not output_filename.lower().endswith('.csv'):
        print("ERROR: Swapped arguments or CSV format is not specified \
        for the output file.")
        print("USE: python webscraping.py <url> <output_filename>")
        sys.exit(1)

    main_program(url, output_filename)


