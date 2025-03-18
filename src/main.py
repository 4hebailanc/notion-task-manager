import argparse
from pathlib import Path
from notion.client import NotionClient
from document.processor import DocumentProcessor

def main():
    parser = argparse.ArgumentParser(description='Sync Notion pages to GitHub')
    parser.add_argument('--config', type=str, help='Path to credentials.yaml')
    parser.add_argument('--output-dir', type=str, help='Output directory for documents')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                      help='Output format for documents')
    args = parser.parse_args()

    # Initialize clients
    notion_client = NotionClient(config_path=args.config)
    doc_processor = DocumentProcessor(output_dir=args.output_dir)

    # Get all pages from the database
    pages = notion_client.get_database_pages()
    
    # Process each page
    for page in pages:
        # Get full page content
        page_content = notion_client.get_page_content(page['id'])
        
        # Process the page
        doc = doc_processor.process_page(page_content)
        
        # Save the document
        output_path = doc_processor.save_document(doc, format=args.format)
        print(f"Processed page '{doc['title']}' -> {output_path}")

if __name__ == '__main__':
    main() 