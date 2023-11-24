# Domain WHOIS Information Script

## Overview
WHOIS Domain Info is a script that fetches WHOIS data like Domain Name, Registrar, Expiration Date, and Days Till Expiry and organizes it in a spreadsheet. (Using the WhoisXMLAPI service) See it in action here!


https://github.com/davidinfosec/whois-domain-info/assets/87215831/c4a16389-671b-41a5-872a-b18da4228362


## Changelog - November 24, 2024

1. **Added Config File and Credential Storage:**
    - Introduced `config.ini` file for storing API key.
    - Introduced `creds.txt` file for storing username and password.
    - Functions `get_api_key()` and `get_credentials()` manage the retrieval and storage of API key and credentials.

2. **Refactored API Request and Response Handling:**
    - The API key is now included in the API request URL.
    - Improved handling of expiration date and days until expiration.
    - Added a new parameter, `time_of_lookup`, representing the time the domain information was retrieved.

3. **CSV Export Enhancements:**
    - Updated `export_all_to_csv()` to append data to an existing file if it already contains data.
    - Modified the CSV header to include 'Time of Lookup'.
    - Timestamp is now included in the CSV filename for unique identification.

4. **Concurrency for Bulk Processing:**
    - Introduced the `ThreadPoolExecutor` for concurrent processing of multiple domains in `process_domains_from_file()`.

5. **Improved Input Handling in Main Loop:**
    - Enhanced user input handling in the main loop (`main()`) to support bulk processing, individual domain lookup, and exit.

6. **Modularized Code:**
    - Broke down the code into functions for better modularity and readability.
    - Introduced a `process_single_domain()` function to handle individual domain requests.

7. **Time of Lookup Update:**
    - Introduced the `time_of_lookup` parameter in the domain information, indicating when the information was retrieved.

8. **Dynamic CSV Filename:**
    - The CSV filename is now dynamically generated based on the input file name, with a timestamp for uniqueness.
    - If the input file contains 'bulk', it is reflected in the CSV filename for bulk processing.

9. **Improved File Path Handling:**
    - Enhanced file path handling in `process_domains_from_file()` to check for file existence and prompt for a valid path.

10. **Enhanced User Interaction:**
    - Improved user prompts and messages for a more user-friendly experience.
   

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
- For more information on WhoisXMLAPI and available options, refer to the [official documentation](https://www.whoisxmlapi.com/).
- Script is sort of slow at the momentum, be patient if you have a large quantity of domain names. It can take a long time to query, but once the list is complete, the csv will be processed. I will look to optimize this shortly, but wanted to get this tool out there for those who want it in its early stages.
