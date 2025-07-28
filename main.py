import os
import re
import fitz  # PyMuPDF
import spacy
import json
from typing import Dict, List, Tuple

class PDFStructureExtractor:
    def __init__(self):
        # Load spaCy model for text analysis
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_structure(self, pdf_path: str) -> Dict:
        """Extract document structure from a PDF file."""
        doc = fitz.open(pdf_path)
        structure = {
            "title": "",
            "outline": []  # Changed from headings to outline
        }
        
        # Enhanced title detection from first page
        if len(doc) > 0:
            first_page = doc[0]
            blocks = first_page.get_text("dict")["blocks"]
            title_candidates = []
            
            # Analyze first 1/3 of the page
            max_y = first_page.rect.height / 3
            
            for block in blocks:
                if "lines" not in block:
                    continue
                
                for line in block["lines"]:
                    if not line["spans"]:
                        continue
                        
                    # Only look at content in top third of first page
                    if line["bbox"][1] > max_y:
                        continue
                        
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text or len(text) < 3:
                            continue
                            
                        # Score this span as a title candidate
                        score = 0
                        
                        # Size scoring (0-40 points)
                        font_size = span["size"]
                        if font_size >= 14:
                            score += 40
                        elif font_size >= 12:
                            score += 30
                        elif font_size >= 10:
                            score += 20
                            
                        # Position scoring (0-20 points)
                        y_pos = line["bbox"][1]
                        if y_pos < max_y * 0.3:  # In first 30% of allowed area
                            score += 20
                        elif y_pos < max_y * 0.6:  # In first 60% of allowed area
                            score += 10
                            
                        # Format scoring (0-20 points)
                        is_bold = bool(span.get("flags", 0) & 2)
                        if is_bold:
                            score += 10
                        if "bold" in span.get("font", "").lower():
                            score += 10
                            
                        # Content scoring (0-20 points)
                        words = text.split()
                        if 2 <= len(words) <= 10:  # Good title length
                            score += 10
                        if all(w[0].isupper() for w in words if w and w[0].isalpha()):
                            score += 10
                            
                        # Filter out obvious non-titles
                        skip_patterns = [
                            r'^\d+$',  # Just numbers
                            r'^page\s+\d+$',  # Page numbers
                            r'^chapter\s+\d+$',  # Chapter markers
                            r'^\s*$',  # Empty strings
                            r'^[•\-\*]\s',  # Bullet points
                            r'^\d+\.\s',  # Numbered lists
                            r'^(?:http|www)',  # URLs
                            r'^[@#]',  # Social media tags
                            r'^\([a-z]\)',  # List markers
                            r'^fig\.',  # Figure references
                            r'^table\s',  # Table references
                        ]
                        
                        if any(re.match(pattern, text.lower()) for pattern in skip_patterns):
                            continue
                            
                        # Store candidate with its score
                        title_candidates.append({
                            'text': text,
                            'score': score,
                            'size': font_size,
                            'y_pos': y_pos,
                            'is_bold': is_bold
                        })
            
            # Sort candidates by score and select the best one
            if title_candidates:
                best_candidate = max(title_candidates, key=lambda x: (x['score'], x['size'], -x['y_pos']))
                structure["title"] = best_candidate['text']
            else:
                structure["title"] = ""  # No good title found

        # Extract headings from all pages
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" not in block:
                    continue
                    
                for line in block["lines"]:
                    if not line["spans"]:
                        continue
                        
                    span = line["spans"][0]
                    text = span["text"].strip()
                    
                    # Skip empty lines
                    if not text:
                        continue
                        
                    # Determine heading level based on font properties
                    font_size = span["size"]
                    font_flags = span["flags"]  # Contains bold/italic info
                    
                    # Enhanced heading detection
                    is_bold = bool(font_flags & 2)  # Check for bold text
                    
                    # Skip if we've already used this text as title
                    if text == structure["title"]:
                        continue
                        
                    # More nuanced heading level detection with string levels
                    if font_size >= 18:
                        level = "H1"
                    elif font_size >= 16 or (font_size >= 14 and is_bold):
                        level = "H2"
                    elif font_size >= 14 or (font_size >= 12 and is_bold):
                        level = "H3"
                    else:
                        continue  # Not a heading
                        
                    structure["outline"].append({
                        "text": text,
                        "level": level,
                        "page": page_num + 1  # Page numbers start from 1
                    })
        
        doc.close()
        return structure

    def process_directory(self, input_dir: str, output_dir: str):
        """Process all PDFs in input directory and save results to output directory."""
        os.makedirs(output_dir, exist_ok=True)
        
        for filename in os.listdir(input_dir):
            if not filename.lower().endswith('.pdf'):
                continue
                
            pdf_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, 
                os.path.splitext(filename)[0] + '.json'
            )
            
            try:
                structure = self.extract_structure(pdf_path)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(structure, f, ensure_ascii=False, indent=2)
                    
                print(f"Successfully processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

def main():
    extractor = PDFStructureExtractor()
    input_dir = os.path.join(os.getcwd(), "input")
    output_dir = os.path.join(os.getcwd(), "output")
    extractor.process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()
