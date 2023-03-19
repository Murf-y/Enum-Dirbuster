"""
Create a Python script that can be run on a website to
discover subdomains (e.g. admin-test.domain.com), directories (e.g.
domain.com/for_admins_only/), and files (e.g. domain.com/user_passwords.txt). This
script will reveal hidden links that may lead to pages with vulnerabilities. Additionally,
two text files are provided, which you will use to read potential subdomains and
directories rather than generating them from scratch.
Your script should be executed from the terminal with the command "python
test_script.py" and should take an argument that represents the target website's URL.
The script must store the input file values and write the output to the following files:
● subdomains_output.bat
● directories_output.bat
● files_output.bat
"""


import os
import re
import sys
import requests

import concurrent.futures
import threading

def check_for_links(html):
    global directories_output

    """
    Check if the html contains any links
    href=...
    or 
    src=...
    or 
    url(...
    
    Save the links in a list and return it
    """
    html = str(html)
    # use lookbehind to check if the link is preceded by href=, src= or url(
    
    # stop at the first quote or parenthesis

    pattern = r"(?<=href=\")([^\"]+)|(?<=src=\")([^\"]+)|(?<=url\()([^\)]+)"
    links = re.findall(pattern, html)

    for sublist in links:
        for link in sublist:
            if link == "":
                continue
            if l.startswith("http") or l.startswith("www") or l.startswith("https") or l.startswith("ftp"):
                directories_output.add(link)

def is_valid_url(url):
    return True if re.match(r"^(http|https|ftp)://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$", url) else False

def check_subdomains(target_url, subdomain):
    global subdomains_output
    global directories_output

    if subdomain == "":
        return

    # Check if target url uses https
    if "https" in target_url:
        url = f"https://{subdomain}.{target_url[8:]}"
    else:
        url = f"http://{subdomain}.{target_url[7:]}"
    
    try:
        if not is_valid_url(url):
            return
        req = requests.head(url)
        # No 404 page
        if req.status_code == 200 and  "404" not in req.text:
            print(f"Found subdomain: {url}")
            subdomains_output.add(url)
            # # Check if the subdomain has any links
            # subdomain_links = check_for_links(req.content)
            # # Add the links to the directories_output set
            # for link in subdomain_links:
            #     if link == "":
            #         continue
                
            #     # Check if link is a subdomain or directory using regex
            #     # Link is a subdomain if it contains http or https then some text then a dot then the target url
            #     regex = r"(?:https?:\/\/)(?:\w+\.?)+(?:\.)" + target_url[7:]
                
            #     # Subdomain
            #     if re.search(regex, link):
            #         if link not in subdomains_output:
            #             subdomains_output.add(link)
            #             print(f"IN SUBDOMAIN: Found subdomain: {link}")
            #     elif link not in directories_output:
            #         directories_output.add(link)
            #         print(f"IN SUBDOMAIN: Found directory: {link}")
    # except all exceptions  
    except Exception as e:
        pass


def check_directories(target_url, directory):
    if directory == "":
        return

    # Check if target url uses https
    if "https" in target_url:
        url = f"https://{target_url[8:]}/{directory}"
    else:
        url = f"http://{target_url[7:]}/{directory}"
    try:
        if not is_valid_url(url):
            return
        req = requests.head(url)
        if req.status_code == 200 and "404" not in req.text:
            # if directory is a file, add it to the files_output set
            if "." in directory:
                print(f"Found file: {url}")
                files_output.add(url)
                
                # extra_links = check_for_links(req.content)
                # # Add the links to the directories_output set
                # for link in extra_links:
                #     if link == "" or link in directories_output:
                #         continue
                
                #     # Check if link is a subdomain or directory using regex
                #     # Link is a subdomain if it contains http or https then some text then a dot then the target url
                #     regex = r"(?:https?:\/\/)(?:\w+\.?)+(?:\.)" + target_url[7:]
                #     # Subdomain
                #     if re.search(regex, link):
                #         if link not in subdomains_output:
                #             subdomains_output.add(link)
                #             print(f"IN FILE: Found subdomain: {link}")
                #         elif link not in directories_output:
                #             directories_output.add(link)
                #             print(f"IN FILE: Found directory: {link}")
            else:
                print(f"Found directory: {url}")
                directories_output.add(url)                    
                # extra_links = check_for_links(req.content)
                # # Add the links to the directories_output set
                # for link in extra_links:
                #     if link == "" or link in directories_output:
                #         continue
                
                #     # Check if link is a subdomain or directory using regex
                #     # Link is a subdomain if it contains http or https then some text then a dot then the target url
                #     regex = r"(?:https?:\/\/)(?:\w+\.?)+(?:\.)" + target_url[7:]
                #     # Subdomain
                #     if re.search(regex, link):
                #         if link not in subdomains_output:
                #             subdomains_output.add(link)
                #             print(f"IN DIRECTORY: Found subdomain: {link}")
                #         elif link not in directories_output:
                #             directories_output.add(link)
                #             print(f"IN DIRECTORY: Found directory: {link}")
    except Exception as e:
        pass

def execute_subdomain_bruteforce(target_url, subdomains):
    for subdomain in subdomains:
        check_subdomains(target_url, subdomain)

def execute_directory_bruteforce(target_url, directories):
    for directory in directories:
        check_directories(target_url, directory)

def subdomain_worker_thread(target_url, subdomains):
    global number_of_threads_for_subdomain

    print("Starting subdomain worker thread...")

    chunk_size = int(len(subdomains)/number_of_threads_for_subdomain)

    print(f"Subdomains Chunk size: {chunk_size}")

    subdomains_chunks = [subdomains[i:i + chunk_size] for i in range(0, len(subdomains), chunk_size)]
    print(f"Generated {len(subdomains_chunks)} subdomains chunks")
    

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(subdomains_chunks)) as executor:
        for subdomain_chunk in subdomains_chunks:
            executor.submit(execute_subdomain_bruteforce, target_url, subdomain_chunk)
    

def directory_worker_thread(target_url, directories):
    global number_of_threads_for_directories
    print("Starting directory worker thread...")

    chunk_size = int(len(directories)/number_of_threads_for_directories)

    print(f"Directories Chunk size: {chunk_size}")
    directories_chunks = [directories[i:i + chunk_size] for i in range(0, len(directories), chunk_size)]
    print(f"Generated {len(directories_chunks)} directories chunks")

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(directories_chunks)) as executor:
        for directory_chunk in directories_chunks:
            executor.submit(execute_directory_bruteforce, target_url, directory_chunk)
    

def main():
    global subdomains_output
    global directories_output
    global files_output

    global subdomain_file_path
    global directory_file_path

    print("""\n\n                                                                                                  
EEEEEEEEEEEEEEEEEEEEEENNNNNNNN        NNNNNNNNUUUUUUUU     UUUUUUUUMMMMMMMM               MMMMMMMM
E::::::::::::::::::::EN:::::::N       N::::::NU::::::U     U::::::UM:::::::M             M:::::::M
E::::::::::::::::::::EN::::::::N      N::::::NU::::::U     U::::::UM::::::::M           M::::::::M
EE::::::EEEEEEEEE::::EN:::::::::N     N::::::NUU:::::U     U:::::UUM:::::::::M         M:::::::::M
  E:::::E       EEEEEEN::::::::::N    N::::::N U:::::U     U:::::U M::::::::::M       M::::::::::M
  E:::::E             N:::::::::::N   N::::::N U:::::D     D:::::U M:::::::::::M     M:::::::::::M
  E::::::EEEEEEEEEE   N:::::::N::::N  N::::::N U:::::D     D:::::U M:::::::M::::M   M::::M:::::::M
  E:::::::::::::::E   N::::::N N::::N N::::::N U:::::D     D:::::U M::::::M M::::M M::::M M::::::M
  E:::::::::::::::E   N::::::N  N::::N:::::::N U:::::D     D:::::U M::::::M  M::::M::::M  M::::::M
  E::::::EEEEEEEEEE   N::::::N   N:::::::::::N U:::::D     D:::::U M::::::M   M:::::::M   M::::::M
  E:::::E             N::::::N    N::::::::::N U:::::D     D:::::U M::::::M    M:::::M    M::::::M
  E:::::E       EEEEEEN::::::N     N:::::::::N U::::::U   U::::::U M::::::M     MMMMM     M::::::M
EE::::::EEEEEEEE:::::EN::::::N      N::::::::N U:::::::UUU:::::::U M::::::M               M::::::M
E::::::::::::::::::::EN::::::N       N:::::::N  UU:::::::::::::UU  M::::::M               M::::::M
E::::::::::::::::::::EN::::::N        N::::::N    UU:::::::::UU    M::::::M               M::::::M
EEEEEEEEEEEEEEEEEEEEEENNNNNNNN         NNNNNNN      UUUUUUUUU      MMMMMMMM               MMMMMMMM\n\n""")


    print("\n\nThis script can be used for malicious purposes. Use it at your own risk.\n\n")


    # Get the target website's URL from the user, passed as an argument
    args = sys.argv[1:] # Get the arguments from the command line

    if len(args) != 1: # Check if the user passed the correct number of arguments

        print("Error !!!")
        print("Usage: python enumerate.py <target_website_url>")
        sys.exit(1)
    
    target_url = args[0] # Get the target website's URL from the arguments

    print(f"Target website's URL: {target_url}")
    
    # Check if the target website's URL is valid using requests
    try:
        requests.get(target_url)
    except requests.exceptions.MissingSchema:
        print("Invalid URL. Please enter a valid URL.")
        sys.exit(1)

    print("Target website's URL is valid.")

    # Check if there is a input_files directory
    if "input_files" not in os.listdir("."):
        print("The input_files directory does not exist.")
        print("Please create the input_files directory and add input files.")
        sys.exit(1)
    
    # Read the subdomains and directories from the provided files

    subdomains = open(subdomain_file_path, "r").read().splitlines()
    directories = open(directory_file_path, "r").read().splitlines()

    print("Loaded subdomains from:" + subdomain_file_path)
    print("Loaded directories from:" + directory_file_path)

    print("\n\nEnumerating subdomains, directories and files...\n\n")

   
    print("Starting subdomain and directory worker threads concurrently...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(subdomain_worker_thread, target_url, subdomains)
        executor.submit(directory_worker_thread, target_url, directories)

    executor.shutdown(wait=True)

    print("Enumeration complete.")

     # Create the output_files directory if it does not exist

    if "output_files" not in os.listdir("."):
        os.mkdir("output_files")
    else:
        # Delete the contents of the output_files directory
        for file in os.listdir("./output_files"):
            os.remove(f"./output_files/{file}")

     # Write the subdomains_output set to a file
    with open("./output_files/subdomains_output.bat", "w") as f:
        for subdomain in subdomains_output:
            f.write(subdomain + "\n")
    
    with open("./output_files/directories_output.bat", "w") as f:
        for dir in directories_output:
            f.write(dir + "\n")
    
    with open("./output_files/files_output.bat", "w") as f:
        for file in files_output:
            f.write(file + "\n")

def brute_force_login(login_api):
    # Brute force the login API through a dictionary attack on POST requests

    # Read the passwords from the provided file
    passwords = open("./input_files/passwords_dictionary.bat", "r").read().splitlines()

    # Get the username from the user
    username = input("Enter the username: ")

    # Check if the username is valid
    if username == "":
        print("Invalid username.")
        sys.exit(1)
    
    # Loop through the passwords and try to login
    for password in passwords:
        if password == "":
            continue

        # Create the data to send in the POST request
        data = {
            "username": username,
            "password": password
        }

        print("Trying password: " + password)
        
        # Send the POST request
        req = requests.post(login_api, data=data)

        # Check if the login was successful
        if req.status_code == 200:
            print(f"Found password: {password}")
            return password


if __name__ == "__main__":
    subdomains_output = set()
    directories_output = set()
    files_output = set()

    subdomain_file_path = "./input_files/subdomains_tiny.bat"
    directory_file_path = "./input_files/dirs_small.bat"

    number_of_threads_for_subdomain = 10
    number_of_threads_for_directories = 10

    main()