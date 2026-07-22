import logfire
from bs4 import BeautifulSoup

def parse_html(file_path: str):
    """
    Parses HTML content using BeautifulSoup.
    Cleans scripts, styles, and extracts readable text for RAG
    """
    
    with logfire.span("HTML Parsing", filename=file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content= f.read()
            soup= BeautifulSoup(content, "html.parser")
            
            ## remove Junks (Scripts, Styles, Metadata)
            for script in soup(["script","style","meta","noscipt"]):
                script.decompose()
                
            ## extract text--
            text= soup.get_text(separator="\n")
            
            ## clean whitespaces (collaspse  multiple newlines)
            lines= (line.strip() for line in text.splitlines())
            chunks= (phrase.strip() for line in lines for phrase in line.split(" "))
            clean_text= '\n'.join(chunk for chunk in chunks if chunk)
            
            return clean_text
        
        except Exception as e:
            logfire.error(f" HTML Parse Failed: {e}")
            raise e
        