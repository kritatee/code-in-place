import datetime
import re
import requests
import arxiv
from pathlib import Path


def create_paper_folder(paper_title, timestamp):
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', paper_title)[:50]
    folder_name = f"{timestamp}-{safe_title}"
    folder_path = Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    return folder_path


def download_pdf(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return False


def main():
    
    # Initialize the arXiv client
    client = arxiv.Client()

    while True:
        
        # Get user input
        search_term = input("Enter a search term (or 'exit' to quit): ")
        if search_term.lower() == 'exit':
            print("Exiting the program.")
            break

        num_results = int(input("Enter the number of results to fetch (default is 1): "))
        
        # Make a request to the API
        try:
            search = arxiv.Search(
                query=search_term,
                max_results=num_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = client.results(search)
            
            if not results:
                print("No results found.")
                continue
            
            # Display the results and process each paper
            for i, result in enumerate(results, start=1):
                print(f"\n{i}. {result.title} by {', '.join(author.name for author in result.authors)}")
                print(f"   Published on: {result.published}")
                print(f"   Summary: {result.summary[:200]}...")
                print(f"   PDF Link: {result.pdf_url}")
                print(f"   Journal Reference: {result.journal_ref}")  
                
                # Create timestamp and folder structure
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                paper_folder = create_paper_folder(result.title, timestamp)
                
                # Download main paper PDF
                pdf_filename = f"{result.entry_id.split('/')[-1]}.pdf"
                pdf_path = paper_folder / pdf_filename
                
                print(f"   Creating folder: {paper_folder}")
                print("   Downloading main paper...")
                
                if download_pdf(result.pdf_url, pdf_path):
                    print(f"   ✓ Downloaded: {pdf_filename}")
                else:
                    print("   ✗ Failed to download main paper")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
