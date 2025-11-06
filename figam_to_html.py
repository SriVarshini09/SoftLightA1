#!/usr/bin/env python3
"""
Figma to HTML/CSS Converter

Converts Figma design files to HTML and CSS using the Figma REST API.

Usage:
    python figam_to_html.py <figma_file_key> [--output OUTPUT_DIR] [--token TOKEN]
    
Example:
    python figam_to_html.py abc123xyz --output ./output --token your_api_token
"""

import argparse
import os
import sys
from dotenv import load_dotenv
from figma_client import FigmaClient
from html_generator import HTMLGenerator
import json

def extract_file_key(figma_url_or_key: str) -> str:
    """
    Extract the file key from a Figma URL or return the key if already provided.
    
    Args:
        figma_url_or_key: Either a full Figma URL or just the file key
        
    Returns:
        The Figma file key
    """
    # If it looks like a URL, extract the key
    if 'figma.com' in figma_url_or_key:
        # Format: https://www.figma.com/file/<file_key>/...
        parts = figma_url_or_key.split('/file/')
        if len(parts) > 1:
            # Get the part after /file/ and before the next /
            key_part = parts[1].split('/')[0].split('?')[0]
            return key_part
    
    # Otherwise, assume it's already a file key
    return figma_url_or_key

def main():
    """Main function to run the Figma to HTML/CSS converter"""
    
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Convert Figma designs to HTML/CSS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python figam_to_html.py abc123xyz
  python figam_to_html.py https://www.figma.com/file/abc123xyz/MyDesign
  python figam_to_html.py abc123xyz --output ./my_output
  python figam_to_html.py abc123xyz --token figd_abc123...
        """
    )
    
    parser.add_argument(
        'figma_file',
        help='Figma file key or full Figma file URL'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='output',
        help='Output directory for HTML/CSS files (default: output)'
    )
    
    parser.add_argument(
        '--token', '-t',
        help='Figma API token (or set FIGMA_API_TOKEN env variable)'
    )
    
    parser.add_argument(
        '--save-json',
        action='store_true',
        help='Save the raw Figma API response as JSON for debugging'
    )
    
    parser.add_argument(
        '--page',
        type=int,
        default=0,
        help='Page index to convert (default: 0, first page)'
    )
    
    args = parser.parse_args()
    
    # Get API token
    api_token = args.token or os.getenv('FIGMA_API_TOKEN')
    
    if not api_token:
        print("Error: Figma API token is required.")
        print("Provide it via --token argument or FIGMA_API_TOKEN environment variable.")
        print("\nTo get your API token:")
        print("1. Go to https://www.figma.com/")
        print("2. Click on your profile icon")
        print("3. Go to Settings")
        print("4. Scroll down to 'Personal Access Tokens'")
        print("5. Click 'Create new token'")
        sys.exit(1)
    
    # Extract file key
    file_key = extract_file_key(args.figma_file)
    print(f"Figma file key: {file_key}")
    
    try:
        # Initialize Figma client
        print("\nFetching Figma file...")
        client = FigmaClient(api_token)
        
        # Fetch the Figma file
        figma_data = client.get_file(file_key)
        
        # Save raw JSON if requested
        if args.save_json:
            json_path = os.path.join(args.output, 'figma_data.json')
            os.makedirs(args.output, exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(figma_data, f, indent=2)
            print(f"Saved raw Figma data to: {json_path}")
        
        # Generate HTML and CSS
        print("\nGenerating HTML and CSS...")
        generator = HTMLGenerator()
        html, css = generator.generate_html_css(figma_data)
        
        # Save to files
        print(f"\nSaving files to: {args.output}")
        generator.save_to_files(html, css, args.output)
        
        print("\n✓ Conversion complete!")
        print(f"\nOpen {os.path.join(args.output, 'index.html')} in your browser to view the result.")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()