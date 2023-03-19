# Enum 📁

A simple DirBuster like tool to enumerate directories, files and subdomains.

## ⚠️ Disclaimer ⚠️

It is strictly prohibited to test the following code on public websites. You can
download Metasploit, which provides access to websites designed for hacking.

## Installation 📥

```bash
git clone https://github.com/Murf-y/Enum-Dirbuster.git

cd enum
```

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

## Usage 📝

Make sure you have python3 installed.<br>
Pass the URL as an argument to the script.

```bash
python3 enum.py https://example.com
```

## License 📜

Licensed under the [MIT License](./LICENSE.md)
