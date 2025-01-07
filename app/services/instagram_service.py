import instaloader
from typing import Dict, Optional
import re

class InstagramService:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        
    def login(self, username: str, password: str):
        """Optional: Login to access private content"""
        try:
            self.loader.login(username, password)
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def parse_recipe_from_post(self, post: instaloader.Post) -> Dict:
        """Extract recipe information from an Instagram post"""
        caption = post.caption or ""
        
        # Basic recipe structure
        recipe = {
            "title": self._extract_title(caption),
            "ingredients": self._extract_ingredients(caption),
            "instructions": self._extract_instructions(caption),
            "source_type": "instagram",
            "source_url": f"https://www.instagram.com/p/{post.shortcode}/",
            "video_url": post.video_url if post.is_video else None,
            "image_urls": [node.display_url for node in post.get_sidecar_nodes()] if post.typename == "GraphSidecar" else [post.url],
            "metadata": {
                "likes": post.likes,
                "caption": caption,
                "timestamp": post.date_utc.isoformat(),
                "location": post.location if post.location else None
            }
        }
        return recipe

    def get_post_by_url(self, url: str) -> Optional[Dict]:
        """Get recipe from Instagram post URL"""
        try:
            shortcode = self._extract_shortcode(url)
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            return self.parse_recipe_from_post(post)
        except Exception as e:
            print(f"Error fetching post: {e}")
            return None

    def _extract_shortcode(self, url: str) -> str:
        """Extract shortcode from Instagram URL"""
        match = re.search(r'instagram.com/p/([^/]+)', url)
        if not match:
            raise ValueError("Invalid Instagram URL")
        return match.group(1)

    def _extract_ingredients(self, caption: str) -> list:
        """Extract ingredients with flexible section handling"""
        ingredients = []
        current_section = ""
        
        lines = caption.split('\n')
        in_ingredient_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for section headers that typically precede ingredients
            if line.endswith(':') or (line.isupper() and len(line.split()) <= 3):
                current_section = line.rstrip(':')
                # Check if this looks like an ingredient section
                in_ingredient_section = any(word in current_section.lower() for word 
                                        in ['ingredient', 'rice', 'chicken', 'salad', 'sauce', 
                                            'dressing', 'garnish', 'topping'])
                continue
                
            # Skip likely non-ingredient lines
            if (line.startswith('#') or 
                line.startswith('@') or 
                'follow' in line.lower() or
                any(word in line.lower() for word in ['preheat', 'bake', 'cook', 'mix', 'blend'])):
                continue
                
            # Look for lines that appear to be ingredients
            if (in_ingredient_section or
                any(unit in line.lower() for unit in ['cup', 'tbsp', 'tb', 'tsp', 'oz', 'pound', 'lb', 'clove', 'bunch']) or
                any(char.isdigit() for char in line)):
                
                # Try to parse amount and unit
                parts = line.replace(',', '').split(None, 2)
                amount = None
                unit = None
                item = line
                
                if len(parts) >= 2:
                    try:
                        # Handle fractions and decimals
                        amount_str = parts[0]
                        if '/' in amount_str:
                            num, denom = amount_str.split('/')
                            amount = float(num) / float(denom)
                        else:
                            amount = float(amount_str)
                            
                        # Normalize common unit abbreviations
                        unit = parts[1].lower()
                        unit_map = {
                            'tb': 'tbsp',
                            'tbs': 'tbsp',
                            'pound': 'lb',
                            'pounds': 'lb',
                            'ounce': 'oz',
                            'ounces': 'oz'
                        }
                        unit = unit_map.get(unit, unit)
                        
                        item = parts[2] if len(parts) > 2 else ''
                    except (ValueError, IndexError):
                        pass
                
                ingredients.append({
                    "item": item.strip(),
                    "amount": amount,
                    "unit": unit,
                    "notes": f"Section: {current_section}" if current_section else None
                })
        
        return ingredients

    def _extract_instructions(self, caption: str) -> list:
        """Extract instructions with more flexible parsing"""
        instructions = []
        in_instruction_section = False
        
        lines = caption.split('\n')
        instruction_text = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('@'):
                continue
                
            # Look for the start of instructions
            if ('instructions:' in line.lower() or
                'directions:' in line.lower() or
                'method:' in line.lower() or
                'first' in line.lower() or
                'preheat' in line.lower() or
                any(word in line.lower() for word in ['bake', 'cook', 'mix', 'blend', 'prepare'])):
                in_instruction_section = True
                if any(char.isdigit() for char in line):  # Skip if it's an ingredient line
                    continue
                instruction_text.append(line)
            elif in_instruction_section:
                instruction_text.append(line)
        
        # Clean up and format instructions
        full_text = ' '.join(instruction_text)
        # Split on common sentence endings or numbered steps
        steps = [s.strip() for s in full_text.split('.') if s.strip()]
        
        return [step + '.' for step in steps if not step.startswith('#')]

    def _extract_title(self, caption: str) -> str:
        """Extract recipe title with more flexible parsing"""
        lines = caption.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('#', '@')) and not line.endswith(':'):
                # Clean up common social media phrases
                title = line
                for phrase in ['follow', 'bookmark', 'save this recipe', 'like and save']:
                    if phrase in title.lower():
                        title = title.split(phrase)[0].strip()
                # Remove excessive emojis (keep up to 3)
                words = title.split()
                emoji_count = sum(1 for word in words if any(char > '\u1F300' for char in word))
                if emoji_count > 3:
                    title = ' '.join(word for word in words 
                                  if not any(char > '\u1F300' for char in word))
                return title.strip()
        return "Untitled Recipe"