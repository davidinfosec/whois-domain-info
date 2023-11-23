# Domain WHO.IS Information Script

## Overview
This Python script allows you to retrieve information about multiple domains using the WhoisXMLAPI service. It fetches details such as the registrar name, expiration date, and days until expiration for each specified domain.

## Dependencies
- [Python](https://www.python.org/downloads/) (Version 3.6 or higher)
- [Requests](https://docs.python-requests.org/en/latest/) library: Used for making HTTP requests.

Install:
``pip install requests``


## Getting Started
1. Obtain API Credentials:
 - Sign up for a free or premium account on [WhoisXMLAPI](https://www.whoisxmlapi.com/).
 - Generate API credentials (username and password) from your account dashboard.

2. Set Up the Script:
 - Copy the script provided in this repository.

3. Configure API Credentials:
 - Replace the `your_username` and `your_password` variables with your WhoisXMLAPI username and password.

4. Input Domain Names:
 - Create a text file (`in.txt`) containing one domain name per line.

5. Run the Script:
 - Execute the script using the following command:
   ```
   python whois.py
   ```

## Script Details

### `get_domain_info(domain_name, username, password)`
- **Parameters:**
- `domain_name` (str): The domain name for which information is to be retrieved.
- `username` (str): Your WhoisXMLAPI username.
- `password` (str): Your WhoisXMLAPI password.
- **Returns:**
- Tuple containing registrar name, expiration date (as a string), and days until expiration (as an integer).

### `export_all_to_csv(domain_info_list)`
- **Parameters:**
- `domain_info_list` (list): List of domain information retrieved by the script.
- **Action:**
- Exports all domain information to a CSV file named `output_info.csv`.

### `process_domains_from_file(file_path, username, password)`
- **Parameters:**
- `file_path` (str): Path to the text file containing domain names.
- `username` (str): Your WhoisXMLAPI username.
- `password` (str): Your WhoisXMLAPI password.
- **Action:**
- Fetches information for each domain from the input file and prints details to the console.
- Calls `export_all_to_csv` to export all data to a CSV file.

## Example Usage
```python
# Example usage
in_file_path = 'in.txt'
your_username = 'your_username'
your_password = 'your_password'
process_domains_from_file(in_file_path, your_username, your_password)
```

## Note

- Ensure that your API account has sufficient credits to perform the desired number of queries.
- For more information on WhoisXMLAPI and available options, refer to the [official documentation](https://www.whoisxmlapi.com/documentation/whois-api.php).
- Script is sort of slow at the momentum, be patient if you have a large quantity of domain names. It can take a long time to query, but once the list is complete, the csv will be processed. I will look to optimize this shortly, but wanted to get this tool out there for those who want it in its early stages.
