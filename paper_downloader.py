import requests
import json
import os
from urllib.parse import quote
import time

def download_exam_papers(years):
    # Base URL and headers
    base_url = 'https://www.reading.ac.uk/repol/default.aspx/?action=getPapers'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.reading.ac.uk',
        'Referer': 'https://www.reading.ac.uk/repol/'
    }

    for year in years:
        # Create directory for PDFs
        pdf_dir = f"ExamenesPDFs_{year}"
        os.makedirs(pdf_dir, exist_ok=True)

        # Perform POST request
        data = f'filterYear={year}&filterModule='
        response = requests.post(base_url, headers=headers, data=data)
        
        if response.status_code != 200:
            print(f"Failed to retrieve data for year {year}. Status code: {response.status_code}")
            continue

        # Parse JSON response
        try:
            papers = json.loads(response.text)['pastpapers']
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for year {year}")
            continue
        except KeyError:
            print(f"Expected 'pastpapers' key not found in JSON response for year {year}")
            continue

        # Download PDFs
        pdf_base_url = f"https://www.reading.ac.uk/repol/papers/ExamPapers{year-1}/"
        for paper in papers:
            paper_code = paper['paper_code']
            encoded_paper_code = quote(paper_code)
            pdf_url = f"{pdf_base_url}{encoded_paper_code}.pdf"
            pdf_filename = os.path.join(pdf_dir, f"{paper_code}.pdf")

            print(f"Downloading: {pdf_url}")
            pdf_response = requests.get(pdf_url)
            
            if pdf_response.status_code == 200:
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"Successfully downloaded: {pdf_filename}")
            else:
                print(f"Failed to download {paper_code} for year {year}. Status code: {pdf_response.status_code}")

            # Add a small delay to avoid overwhelming the server
            time.sleep(0.5)

        print(f"Finished downloading papers for year {year}")
        # Add a longer delay between years
        time.sleep(2)

if __name__ == "__main__":
    years_to_download = [2022, 2023]
    download_exam_papers(years_to_download)
