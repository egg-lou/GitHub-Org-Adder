import csv
from urllib.parse import urlparse

def extract_username_from_url(github_url):

    parsed_url = urlparse(github_url)
    
    username = parsed_url.path.strip('/')

    return username

def process_csv(input_csv_file, output_csv_file):
    with open(input_csv_file, 'r') as infile, open(output_csv_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['username', 'role']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            github_link = row['github_link']
            role = row['role']

            username = extract_username_from_url(github_link)

            writer.writerow({'username': username, 'role': role})

            print(f'Processed {github_link} for {username} with role {role}')

if __name__ == "__main__":
    input_csv_file = "base.csv"
    output_csv_file = "done.csv"

    process_csv(input_csv_file, output_csv_file)
