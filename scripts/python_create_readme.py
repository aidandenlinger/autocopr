#!/bin/env python3

import pathlib

# Specify the directory path
dir_path = pathlib.Path(".")

# Use glob to retrieve a list of files
files = dir_path.glob("specs/**/*.spec")  # only match .spec files

# Sort the files by filename (natural sort)
sorted_files = sorted(files, key=lambda x: x.name)

# Array to store the name and URL pairs
name_url_pairs = []

# Process files and extract Name and URL
for file in sorted_files:
    name = None
    url = None
    with file.open("r", encoding="utf-8") as spec_file:
        for line in spec_file:
            if line.startswith("Name:"):
                name = line.split(":", 1)[1].strip()
            elif line.startswith("URL:"):
                url = line.split(":", 1)[1].strip()
            # Break the loop if both Name and URL are found
            if name and url:
                break
    if name and url:
        name_url_pairs.append((name, url))
        print(f"Processed: {file.name} -> Name: {name}, URL: {url}")

# Create markdown content for README.md
readme_content = """# Autocopr forked repo

## For any issues or questions related to python scripts, please go to upstream repo.

<details open>

<summary>Status badges on COPR builds</summary>
"""

for name, url in name_url_pairs:
    readme_content += f"""
### {name}

![{name} status](https://copr.fedorainfracloud.org/coprs/relativesure/all-packages/package/{name}/status_image/last_build.png)
[Upstream]({url})
"""

# Example of how to convert markdown content to HTML (optional, for further use)
# html_content = markdown.markdown(markdown_content)

# Write markdown content to README.md
readme_path = pathlib.Path("README.md")
with readme_path.open("w", encoding="utf-8") as readme_file:
    readme_file.write(readme_content)

print("README.md file created successfully!")

# Example of how to use the html_content (optional)
# with open("README.html", "w", encoding="utf-8") as html_file:
#     html_file.write(html_content)
