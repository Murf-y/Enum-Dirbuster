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

def check_for_links(html):
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

    flattened_links = [link for sublist in links for link in sublist]
    return [l for l in flattened_links if l.startswith("http") or l.startswith("www") or l.startswith("https") or l.startswith("ftp")]

def main():
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

    # Check if there is a input_files directory
    if "input_files" not in os.listdir("."):
        print("The input_files directory does not exist.")
        print("Please create the input_files directory and add the subdomains_dictionary and dirs_dictionary.bat files.")
        sys.exit(1)
    
    # Read the subdomains and directories from the provided files
    subdomains = open("./input_files/subdomains_dictionary.bat", "r").read().splitlines()
    directories = open("./input_files/dirs_dictionary.bat", "r").read().splitlines()

    # Create a set so we dont have duplicate entries
    subdomains_output = set()
    directories_output = set()
    files_output = set()

    print("\n\nEnumerating subdomains, directories and files...\n\n")

    # Check for subdomains
    for subdomain in subdomains:
        if subdomain == "":
            continue

        # Check if target url uses https
        if "https" in target_url:
            url = f"https://{subdomain}.{target_url[8:]}"
        else:
            url = f"http://{subdomain}.{target_url[7:]}"
        
        try:
            req = requests.get(url)
            if req.status_code == 200:
                print(f"Found subdomain: {url}")
                subdomains_output.add(url)

                # Check if the subdomain has any links
                subdomain_links = check_for_links(req.content)

                # Add the links to the directories_output set
                for link in subdomain_links:
                    if link == "":
                        continue
                    
                    # Check if link is a subdomain or directory using regex
                    # Link is a subdomain if it contains http or https then some text then a dot then the target url

                    regex = r"(?:https?:\/\/)(?:\w+\.?)+(?:\.)" + target_url[7:]
                    
                    # Subdomain
                    if re.search(regex, link):
                        if link not in subdomains_output:
                            subdomains_output.add(link)
                            print(f"IN SUBDOMAIN: Found subdomain: {link}")
                    elif link not in directories_output:
                        directories_output.add(link)
                        print(f"IN SUBDOMAIN: Found directory: {link}")
                    
        except requests.exceptions.ConnectionError:
            pass
    
    # Check for directories
    for directory in directories:
        if directory == "":
            continue

        # Check if target url uses https
        if "https" in target_url:
            url = f"https://{target_url[8:]}/{directory}"
        else:
            url = f"http://{target_url[7:]}/{directory}"

        try:
            req = requests.get(url)
            if req.status_code == 200:
                # if directory is a file, add it to the files_output set
                if "." in directory:
                    print(f"Found file: {url}")
                    files_output.add(url)
                    
                    extra_links = check_for_links(req.content)

                    # Add the links to the directories_output set
                    for link in extra_links:
                        if link == "" or link in directories_output:
                            continue
                    
                        # Check if link is a subdomain or directory using regex
                        # Link is a subdomain if it contains http or https then some text then a dot then the target url

                        regex = r"(?:https?:\/\/)(?:\w+\.?)+(?:\.)" + target_url[7:]

                        # Subdomain
                        if re.search(regex, link):
                            if link not in subdomains_output:
                                subdomains_output.add(link)
                                print(f"IN FILE: Found subdomain: {link}")
                            elif link not in directories_output:
                                directories_output.add(link)
                                print(f"IN FILE: Found directory: {link}")
                else:
                    print(f"Found directory: {url}")
                    directories_output.add(url)                    

        except requests.exceptions.ConnectionError:
            pass
    
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

if __name__ == "__main__":
    main()