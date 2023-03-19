# Enum 📁

<p align="center">
<img src="./logo.png" width="350">
</p>

```
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
EEEEEEEEEEEEEEEEEEEEEENNNNNNNN         NNNNNNN      UUUUUUUUU      MMMMMMMM               MMMMMMMM

```

A simple DirBuster like tool to enumerate directories, files and subdomains built in python3.

<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">

## ⚠️ Disclaimer ⚠️

It is strictly prohibited to test the following code on public websites. You can
download Metasploit, which provides access to websites designed for hacking.

<hr>

## Features 📋

- Enumerate directories and files
- Enumerate subdomains
- Multithreading

<hr>

## Installation 📥

```bash
git clone https://github.com/Murf-y/Enum-Dirbuster.git

cd enum
```

<hr>

## Configuration 📝

In enum.py, you can change the number of threads for subdomains and directories.
And also the input files.

```python
    subdomain_file_path = "./input_files/subdomains_tiny.bat"
    directory_file_path = "./input_files/dirs_small.bat"

    number_of_threads_for_subdomain = 10
    number_of_threads_for_directories = 10
```

Currently, input files available are:

- Dirs:
  - small = 1578 (default)
  - medium = 3000
  - big = 5000

- Subdomains:
  - tiny =  5000 (default)
  - small = 70000
  - medium = 300000
  - big = 700000

<hr>

## Usage 📝

Make sure you have python3 installed.<br>
Pass the URL as an argument to the script.

```bash
python3 enum.py https://example.com
```

<hr>

## License 📜

Licensed under the [MIT License](./LICENSE.md)
