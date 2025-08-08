from typing import List, Dict
import re


class ArticleTagger:
    """Tag articles based on keyword matching in title and body."""
    
    def __init__(self):
        # Define keyword mappings for different tags
        self.tag_keywords: Dict[str, List[str]] = {
            "elections": [
                "election", "vote", "voting", "poll", "polls", "campaign", 
                "candidate", "ballot", "electoral", "commission", "results"
            ],
            "health": [
                "health", "medical", "hospital", "doctor", "patient", "treatment",
                "disease", "vaccine", "vaccination", "covid", "mental health",
                "healthcare", "clinic", "medicine", "symptoms"
            ],
            "corruption": [
                "corruption", "bribe", "bribery", "scandal", "fraud", "embezzlement",
                "misappropriation", "irregularities", "audit", "investigation",
                "arrested", "charges", "suspended", "financial"
            ]
        }
    
    def tag_article(self, title: str, body: str) -> List[str]:
        """
        Tag an article based on keywords found in title and body.
        
        Args:
            title: Article title
            body: Article body text
            
        Returns:
            List of tags assigned to the article
        """
        # Combine title and body for keyword search
        content = f"{title} {body}".lower()
        
        # Find matching tags
        matched_tags = []
        
        for tag, keywords in self.tag_keywords.items():
            for keyword in keywords:
                # Use word boundary to avoid partial matches
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, content):
                    matched_tags.append(tag)
                    break  # Only need one keyword match per tag
        
        return matched_tags
    
    def get_available_tags(self) -> List[str]:
        """Get list of available tags."""
        return list(self.tag_keywords.keys())
    
    def get_keywords_for_tag(self, tag: str) -> List[str]:
        """Get keywords for a specific tag."""
        return self.tag_keywords.get(tag, []) 