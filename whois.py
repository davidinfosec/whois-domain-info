import requests
from datetime import datetime, timedelta
from urllib.parse import quote
import csv

def get_domain_info(domain_name, username, password):
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

    api_url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={domain_name}&username={encoded_username}&password={encoded_password}&ipWhois={ip_whois}&checkProxyData={check_proxy_data}&thinWhois={thin_whois}&ignoreRawTexts={ignore_raw_texts}&outputFormat={output_format}&_parse={parse}&da={da}&preferFresh={prefer_fresh}&ip={ip}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx status codes)

        data = response.json()

        if 'WhoisRecord' in data:
            record = data['WhoisRecord']
            registrar = record.get('registrarName', 'N/A')
            expiration_date_str = record.get('registryData', {}).get('expiresDate', 'N/A')

            # Convert expiration date string to datetime object
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%dT%H:%M:%SZ')

            # Calculate days until expiration
            days_until_expiration = (expiration_date - datetime.now()).days

            return registrar, expiration_date_str, days_until_expiration
        else:
            print(f"No 'WhoisRecord' key found in the API response")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching information for domain {domain_name}: {e}")
        return None

def export_all_to_csv(domain_info_list):
    csv_filename = 'output_info.csv'

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Domain Name', 'Registrar', 'Expiration Date', 'Days Until Expiration'])

        for domain_info in domain_info_list:
            writer.writerow(domain_info)

    print(f"All data exported to {csv_filename}\n")

def process_domains_from_file(file_path, username, password):
    domain_info_list = []

    with open(file_path, 'r') as file:
        domain_names = [line.strip() for line in file]

    for domain_name in domain_names:
        result = get_domain_info(domain_name, username, password)

        if result:
            registrar, expiration_date, days_until_expiration = result
            print(f"Domain: {domain_name}")
            print(f"Registrar: {registrar}")
            print(f"Expiration Date: {expiration_date}")
            print(f"Days Until Expiration: {days_until_expiration}\n")

            domain_info_list.append([domain_name, registrar, expiration_date, days_until_expiration])
        else:
            print(f"Unable to fetch information for domain: {domain_name}\n")

    export_all_to_csv(domain_info_list)
# Example usage
in_file_path = 'in.txt' #create in.txt in the file path of the script with your domain list
your_username = 'enter username here' #enter username in this field
your_password = 'enter password here' #enter password in this field
process_domains_from_file(in_file_path, your_username, your_password)
