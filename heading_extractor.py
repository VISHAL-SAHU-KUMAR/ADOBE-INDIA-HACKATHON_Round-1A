import re
from collections import Counter, defaultdict

class HeadingAnalyzer:
    def __init__(self):
        self.font_stats = defaultdict(int)
        self.bold_sizes = set()
        self.all_sizes = []
        self.size_thresholds = {}
        
    def analyze_fonts(self, spans):
        """Analyze font characteristics across the document."""
        for span in spans:
            size = span.get("size", 0)
            self.font_stats[size] += 1
            self.all_sizes.append(size)
            if span.get("flags", 0) & 2**4:  # Bold flag
                self.bold_sizes.add(size)
                
        # Calculate size thresholds
        if self.all_sizes:
            sorted_sizes = sorted(set(self.all_sizes))
            self.size_thresholds = {
                'max': max(sorted_sizes),
                'min': min(sorted_sizes),
                'median': sorted_sizes[len(sorted_sizes)//2],
                'q3': sorted_sizes[int(len(sorted_sizes)*0.75)],
                'q1': sorted_sizes[int(len(sorted_sizes)*0.25)]
            }
            
    def get_heading_level(self, text_props):
        """
        Determine heading level based on sophisticated analysis of text properties.
        
        Args:
            text_props (dict): Properties of the text including:
                - size: font size
                - bold: whether text is bold
                - x: x position
                - y: y position
                - text: actual text content
                - font: font name
                - spacing_above: space above the text
                
        Returns:
            str or None: "H1", "H2", "H3", "H4" or None if not a heading
        """
        # Initialize scoring system
        score = {
            "size": 0,        # Font size relative to document
            "style": 0,       # Bold, font family, etc.
            "position": 0,    # Location on page, indentation
            "format": 0,      # Text case, numbers, symbols
            "content": 0      # Length, word patterns
        }
        
        # Text analysis
        text = text_props["text"].strip()
        size = text_props.get("size", 0)
        
        # Skip invalid candidates
        if not text or len(text.split()) > 20:  # Too long for a heading
            return None
            
        # Size scoring (30% of total)
        if size >= self.size_thresholds['q3']:
            score["size"] = 30
        elif size >= self.size_thresholds['median']:
            score["size"] = 20
        elif size >= self.size_thresholds['q1']:
            score["size"] = 10
            
        # Style scoring (25% of total)
        if text_props.get("bold", False):
            score["style"] += 15
        if "bold" in text_props.get("font", "").lower():
            score["style"] += 10
            
        # Position scoring (15% of total)
        if text_props.get("y", 0) < 100:  # Near top of page
            score["position"] += 10
        if text_props.get("spacing_above", 0) > text_props.get("size", 10):
            score["position"] += 5
            
        # Format scoring (15% of total)
        words = text.split()
        if all(w[0].isupper() for w in words if w and w[0].isalpha()):
            score["format"] += 10
        if text.isupper() and len(text) > 3:
            score["format"] += 5
            
        # Content scoring (15% of total)
        if 2 <= len(words) <= 10:  # Ideal heading length
            score["content"] += 10
        if any(text.startswith(prefix) for prefix in [
            "Chapter", "Section", "Part", "Introduction", "Conclusion"
        ]):
            score["content"] += 5
            
        # Calculate total score (max 100)
        total_score = sum(score.values())
        
        # Determine level based on score and additional rules
        if total_score >= 80 and size >= self.size_thresholds['q3']:
            return "H1"
        elif total_score >= 65 and (size >= self.size_thresholds['median'] or text_props.get("bold", False)):
            return "H2"
        elif total_score >= 50:
            return "H3"
        elif total_score >= 35:
            return "H4"
            
        return None
        
    def clean_heading_text(self, text):
        """Clean and normalize heading text."""
        # Remove common prefixes
        text = re.sub(r'^(?:Chapter|Section|Part)\s*\d+[.:]\s*', '', text)
        # Remove trailing punctuation
        text = re.sub(r'[.:]$', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text
