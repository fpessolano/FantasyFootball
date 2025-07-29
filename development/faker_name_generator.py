#!/usr/bin/env python3
"""
International Name Generator using Faker Library
Generates random names from various nationalities using online Faker library.
"""

import random
from faker import Faker
from faker.config import AVAILABLE_LOCALES

class InternationalNameGenerator:
    """
    Generates random names for various nationalities using the Faker library.
    
    Faker supports 100+ locales with authentic names for each region.
    """
    
    def __init__(self, seed=None):
        """Initialize with optional seed for reproducible results."""
        if seed:
            Faker.seed(seed)
            random.seed(seed)
        
        # Verified locales with working name data
        self.popular_locales = {
            'en_US': 'American',
            'en_GB': 'British', 
            'fr_FR': 'French',
            'de_DE': 'German',
            'it_IT': 'Italian',
            'es_ES': 'Spanish',
            'pt_PT': 'Portuguese',
            'pt_BR': 'Brazilian',
            'ru_RU': 'Russian',
            'pl_PL': 'Polish',
            'nl_NL': 'Dutch',
            'sv_SE': 'Swedish',
            'no_NO': 'Norwegian',
            'da_DK': 'Danish',
            'fi_FI': 'Finnish',
            'ja_JP': 'Japanese',
            'ko_KR': 'Korean',
            'zh_CN': 'Chinese',
            'hi_IN': 'Indian (Hindi)',
            'ar_SA': 'Arabic (Saudi)',
            'tr_TR': 'Turkish',
            'he_IL': 'Hebrew',
            'th_TH': 'Thai',
            'vi_VN': 'Vietnamese',
            'id_ID': 'Indonesian',
            'tl_PH': 'Filipino',
            'uk_UA': 'Ukrainian',
            'cs_CZ': 'Czech',
            'hu_HU': 'Hungarian',
            'ro_RO': 'Romanian',
            'bg_BG': 'Bulgarian',
            'hr_HR': 'Croatian',
            'sl_SI': 'Slovenian',
            'et_EE': 'Estonian',
            'lv_LV': 'Latvian',
            'lt_LT': 'Lithuanian',
            'sk_SK': 'Slovak',
            'el_GR': 'Greek',
            'is_IS': 'Icelandic',
            'ga_IE': 'Irish',
            'cy_GB': 'Welsh',
            'eu_ES': 'Basque',
            'ca_ES': 'Catalan',
            'fa_IR': 'Persian',
            'bn_BD': 'Bengali',
            'ne_NP': 'Nepali',
            'ka_GE': 'Georgian',
            'hy_AM': 'Armenian',
            'az_AZ': 'Azerbaijani'
        }
    
    def get_available_locales(self):
        """Get all available locales from Faker."""
        return list(AVAILABLE_LOCALES)
    
    def get_popular_locales(self):
        """Get dictionary of popular locales with descriptions."""
        return self.popular_locales
    
    def generate_name(self, locale='en_US'):
        """
        Generate a random name for specified locale.
        
        Args:
            locale (str): Locale code (e.g., 'en_US', 'fr_FR', 'ja_JP')
            
        Returns:
            dict: Contains 'full_name', 'first_name', 'last_name', 'locale', 'nationality'
        """
        try:
            fake = Faker(locale)
            
            return {
                'full_name': fake.name(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'locale': locale,
                'nationality': self.popular_locales.get(locale, locale)
            }
        except Exception as e:
            print(f"Error generating name for locale {locale}: {e}")
            # Fallback to English
            fake = Faker('en_US')
            return {
                'full_name': fake.name(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'locale': 'en_US',
                'nationality': 'American (fallback)'
            }
    
    def generate_random_name(self):
        """Generate a name from a random nationality."""
        locale = random.choice(list(self.popular_locales.keys()))
        return self.generate_name(locale)
    
    def generate_multiple_names(self, count=10, locale=None):
        """
        Generate multiple names.
        
        Args:
            count (int): Number of names to generate
            locale (str): Specific locale, or None for random
            
        Returns:
            list: List of name dictionaries
        """
        names = []
        for _ in range(count):
            if locale:
                names.append(self.generate_name(locale))
            else:
                names.append(self.generate_random_name())
        return names
    
    def generate_male_name(self, locale='en_US'):
        """Generate a male name for specified locale."""
        try:
            fake = Faker(locale)
            return {
                'full_name': fake.name_male(),
                'first_name': fake.first_name_male(),
                'last_name': fake.last_name(),
                'gender': 'male',
                'locale': locale,
                'nationality': self.popular_locales.get(locale, locale)
            }
        except:
            # Some locales don't have gender-specific methods
            return self.generate_name(locale)
    
    def generate_female_name(self, locale='en_US'):
        """Generate a female name for specified locale."""
        try:
            fake = Faker(locale)
            return {
                'full_name': fake.name_female(),
                'first_name': fake.first_name_female(),
                'last_name': fake.last_name(),
                'gender': 'female',
                'locale': locale,
                'nationality': self.popular_locales.get(locale, locale)
            }
        except:
            # Some locales don't have gender-specific methods
            return self.generate_name(locale)
    
    def search_locales(self, search_term):
        """Search for locales containing the search term."""
        search_term = search_term.lower()
        matching_locales = {}
        
        for locale, nationality in self.popular_locales.items():
            if (search_term in locale.lower() or 
                search_term in nationality.lower()):
                matching_locales[locale] = nationality
                
        return matching_locales

# Example usage and testing
def main():
    """Demonstrate the name generator functionality."""
    
    print("🌍 International Name Generator using Faker")
    print("=" * 50)
    
    # Initialize generator
    generator = InternationalNameGenerator(seed=42)  # Seed for reproducible results
    
    # Show available popular locales
    print("\n📍 Popular Locales Available:")
    locales = generator.get_popular_locales()
    for locale, nationality in list(locales.items())[:10]:  # Show first 10
        print(f"  {locale}: {nationality}")
    print(f"  ... and {len(locales)-10} more!")
    
    # Generate random names
    print("\n🎲 Random Names from Different Countries:")
    for i in range(5):
        name_data = generator.generate_random_name()
        print(f"  {name_data['full_name']} ({name_data['nationality']})")
    
    # Generate names from specific countries
    print("\n🇯🇵 Japanese Names:")
    for i in range(3):
        name_data = generator.generate_name('ja_JP')
        print(f"  {name_data['full_name']}")
    
    print("\n🇫🇷 French Names:")
    for i in range(3):
        name_data = generator.generate_name('fr_FR')
        print(f"  {name_data['full_name']}")
    
    print("\n🇮🇳 Indian Names:")
    for i in range(3):
        name_data = generator.generate_name('hi_IN')
        print(f"  {name_data['full_name']}")
    
    # Generate gender-specific names
    print("\n👨 Male Names (German):")
    for i in range(3):
        name_data = generator.generate_male_name('de_DE')
        print(f"  {name_data['full_name']}")
    
    print("\n👩 Female Names (Spanish):")
    for i in range(3):
        name_data = generator.generate_female_name('es_ES')
        print(f"  {name_data['full_name']}")
    
    # Search functionality
    print("\n🔍 Search for 'chinese' locales:")
    results = generator.search_locales('chinese')
    for locale, nationality in results.items():
        print(f"  {locale}: {nationality}")
    
    # Batch generation
    print("\n📦 Batch Generation (5 random names):")
    batch_names = generator.generate_multiple_names(5)
    for name_data in batch_names:
        print(f"  {name_data['full_name']} ({name_data['nationality']})")

if __name__ == "__main__":
    # Check if Faker is installed
    try:
        from faker import Faker
        print("✅ Faker library is installed and ready!")
        main()
    except ImportError:
        print("❌ Faker library not found!")
        print("📦 Install it with: pip install faker")
        print("\nAfter installation, run this script again.")