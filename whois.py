import requests
from datetime import datetime, timedelta
from urllib.parse import quote
import csv
import getpass
import os
import configparser
from concurrent.futures import ThreadPoolExecutor

CONFIG_FILE = 'config.ini'
CREDS_FILE = 'creds.txt'

def get_api_key():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'API' in config and 'key' in config['API']:
            return config['API']['key']

    api_key = getpass.getpass("Enter your API key: ")

    config['API'] = {'key': api_key}

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

    return api_key

def get_credentials():
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, 'r') as file:
            lines = file.readlines()
            if len(lines) == 2:
                return lines[0].strip(), lines[1].strip()

    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    with open(CREDS_FILE, 'w') as file:
        file.write(username + '\n')
        file.write(password + '\n')

    return username, password

def get_domain_info(domain_name, username, password, api_key):
    encoded_username = quote(username)
    encoded_password = quote(password)

    # Additional parameters
    ip_whois = 0
    check_proxy_data = 0
    thin_whois = 0
    ignore_raw_texts = 0
    output_format = 'JSON'
    parse = 0
    da = 0
    prefer_fresh = 0
    ip = 0

    api_url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={domain_name}&username={encoded_username}&password={encoded_password}&ipWhois={ip_whois}&checkProxyData={check_proxy_data}&thinWhois={thin_whois}&ignoreRawTexts={ignore_raw_texts}&outputFormat={output_format}&_parse={parse}&da={da}&preferFresh={prefer_fresh}&ip={ip}&apiKey={api_key}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()

        if 'WhoisRecord' in data:
            record = data['WhoisRecord']
            registrar = record.get('registrarName', 'N/A')
            expiration_date_str = record.get('registryData', {}).get('expiresDate', 'N/A')

            if expiration_date_str != 'N/A':
                expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%dT%H:%M:%SZ')
                days_until_expiration = (expiration_date - datetime.now()).days
            else:
                expiration_date = 'N/A'
                days_until_expiration = 'N/A'

            # Update Time of Lookup to the current time
            time_of_lookup = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            return registrar, expiration_date, days_until_expiration, time_of_lookup
        else:
            print(f"No 'WhoisRecord' key found in the API response")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching information for domain {domain_name}: {e}")
        return None

def export_all_to_csv(domain_info_list, csv_filename='output_info.csv'):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Domain', 'Registrar', 'Expiration Date', 'Days Until Expiration', 'Time of Lookup'])

        for domain_info in domain_info_list:
            writer.writerow(domain_info)

    print(f"All data exported to {csv_filename}\n")

def process_single_domain(domain_name, username, password, api_key):
    result = get_domain_info(domain_name, username, password, api_key)

    if result:
        registrar, expiration_date, days_until_expiration, time_of_lookup = result
        print(f"Domain: {domain_name}")
        print(f"Registrar: {registrar}")
        print(f"Expiration Date: {expiration_date}")
        print(f"Days Until Expiration: {days_until_expiration}")
        print(f"Time of Lookup: {time_of_lookup}\n")

        return [domain_name, registrar, expiration_date, days_until_expiration, time_of_lookup]
    else:
        print(f"Unable to fetch information for domain: {domain_name}\n")
        return None

def process_domains_from_file(username, password, api_key, file_path):
    domain_info_list = []

    while True:
        if not file_path:
            file_path = 'in.txt'

        if file_path.lower() == 'cancel':
            return

        if not os.path.exists(file_path):
            print(f"File not found at {file_path}. Please provide a valid file path.")
            file_path = input("Enter the path of the input file (press Enter for default 'in.txt') or 'cancel' to go back: ")
        else:
            break

    with open(file_path, 'r') as file:
        domain_names = [line.strip() for line in file]

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda domain_name: process_single_domain(domain_name, username, password, api_key), domain_names))

    for result in results:
        if result:
            domain_info_list.append(result)

    filename_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    csv_filename = f"{filename_without_extension}_bulk_{timestamp}.csv" if 'bulk' in file_path else f"{filename_without_extension}_{timestamp}.csv"

    export_all_to_csv(domain_info_list, csv_filename)

def main():
    api_key = get_api_key()
    username, password = get_credentials()

    while True:
        domain_or_bulk = input("Enter the domain name, 'bulk' for bulk check, or 'exit' to quit: ").lower()

        if domain_or_bulk == 'exit':
            break
        elif domain_or_bulk == 'bulk':
            in_file_path = input("Enter the path of the input file (press Enter for default 'in.txt'): ") or 'in.txt'
            process_domains_from_file(username, password, api_key, in_file_path)
        else:
            result = process_single_domain(domain_or_bulk, username, password, api_key)
            if result:
                export_all_to_csv([result])

if __name__ == "__main__":
    main()
