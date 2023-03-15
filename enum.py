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


import sys

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

    
if __name__ == "__main__":
    main()