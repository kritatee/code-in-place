import datetime
import os
import re
import requests
import arxiv
from pathlib import Path

def create_paper_folder(paper_title, timestamp):
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', paper_title)[:50]
    folder_name = f"{timestamp}-{safe_title}"
    folder_path = Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    citations_path = folder_path / "citations"
    citations_path.mkdir(exist_ok=True)
    return folder_path, citations_path

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

def extract_citations_from_text(text):
    arxiv_pattern = r'arXiv:(\d{4}\.\d{4,5})'
    
    arxiv_matches = re.findall(arxiv_pattern, text, re.IGNORECASE)
    
    citations = []
    for arxiv_id in arxiv_matches:
        citations.append(f"arXiv:{arxiv_id}")
    
    return citations

def download_citation_papers(citations, citations_folder):
    client = arxiv.Client()
    
    for citation in citations:
        if citation.startswith("arXiv:"):
            arxiv_id = citation.replace("arXiv:", "")
            try:
                search = arxiv.Search(id_list=[arxiv_id])
                results = list(client.results(search))
                
                if results:
                    paper = results[0]
                    safe_title = re.sub(r'[<>:"/\\|?*]', '_', paper.title)[:30]
                    pdf_filename = f"{arxiv_id}_{safe_title}.pdf"
                    pdf_path = citations_folder / pdf_filename
                    
                    print(f"  Downloading citation: {paper.title}")
                    if download_pdf(paper.pdf_url, pdf_path):
                        print(f"  ✓ Downloaded: {pdf_filename}")
                    else:
                        print(f"  ✗ Failed to download: {pdf_filename}")
                        
            except Exception as e:
                print(f"  Error downloading citation {citation}: {e}")

def main():
    
    # Initialize the arXiv client
    client = arxiv.Client()

    while True:
        
        # Get user input
        user_input = input("Enter a search term (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        
        # Make a request to the API
        try:
            search = arxiv.Search(
                query=user_input,
                max_results=1,
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
                
                # Create timestamp and folder structure
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                paper_folder, citations_folder = create_paper_folder(result.title, timestamp)
                
                # Download main paper PDF
                pdf_filename = f"{result.entry_id.split('/')[-1]}.pdf"
                pdf_path = paper_folder / pdf_filename
                
                print(f"   Creating folder: {paper_folder}")
                print("   Downloading main paper...")
                
                if download_pdf(result.pdf_url, pdf_path):
                    print(f"   ✓ Downloaded: {pdf_filename}")
                    
                    # Extract citations from summary and title (basic extraction)
                    full_text = result.title + " " + result.summary
                    citations = extract_citations_from_text(full_text)
                    
                    if citations:
                        print(f"   Found {len(citations)} citation(s): {citations}")
                        print(f"   Downloading citations to: {citations_folder}")
                        download_citation_papers(citations, citations_folder)
                    else:
                        print("   No arXiv citations found in abstract/title")
                else:
                    print("   ✗ Failed to download main paper")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
