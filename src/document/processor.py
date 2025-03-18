from typing import Dict, List, Optional
from pathlib import Path
import json
import yaml
from datetime import datetime

class DocumentProcessor:
    def __init__(self, output_dir: Optional[str] = None):
        """Initialize the document processor.
        
        Args:
            output_dir: Directory to store processed documents. If None, uses docs/
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "docs"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_page(self, page_content: Dict) -> Dict:
        """Process a Notion page into a structured document.
        
        Args:
            page_content: Raw page content from Notion API
            
        Returns:
            Processed document content
        """
        # Extract basic page information
        doc = {
            'id': page_content['id'],
            'title': self._extract_title(page_content),
            'created_time': page_content['created_time'],
            'last_edited_time': page_content['last_edited_time'],
            'properties': page_content['properties'],
            'content': self._extract_content(page_content)
        }
        return doc
    
    def save_document(self, doc: Dict, format: str = 'markdown') -> Path:
        """Save a processed document to disk.
        
        Args:
            doc: Processed document content
            format: Output format ('markdown' or 'json')
            
        Returns:
            Path to the saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{doc['id']}_{timestamp}"
        
        if format == 'markdown':
            filepath = self.output_dir / f"{filename}.md"
            self._save_markdown(doc, filepath)
        else:
            filepath = self.output_dir / f"{filename}.json"
            self._save_json(doc, filepath)
        
        return filepath
    
    def _extract_title(self, page_content: Dict) -> str:
        """Extract the title from a page's properties."""
        for prop in page_content['properties'].values():
            if prop['type'] == 'title':
                return prop['title'][0]['plain_text'] if prop['title'] else "Untitled"
        return "Untitled"
    
    def _extract_content(self, page_content: Dict) -> List[Dict]:
        """Extract the main content from a page."""
        # This is a placeholder - actual implementation would need to handle
        # Notion's block structure and convert it to appropriate format
        return []
    
    def _save_markdown(self, doc: Dict, filepath: Path) -> None:
        """Save document as markdown."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {doc['title']}\n\n")
            f.write(f"Created: {doc['created_time']}\n")
            f.write(f"Last edited: {doc['last_edited_time']}\n\n")
            # Add content conversion logic here
    
    def _save_json(self, doc: Dict, filepath: Path) -> None:
        """Save document as JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(doc, f, indent=2, ensure_ascii=False) 