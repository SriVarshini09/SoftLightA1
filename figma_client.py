import requests
import json
from typing import Dict, Any, Optional

class FigmaClient:
    """Client for interacting with the Figma API"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": api_token
        }
    
    def get_file(self, file_key: str) -> Dict[str, Any]:
        """
        Fetch a Figma file by its key.
        
        Args:
            file_key: The Figma file key from the URL
            
        Returns:
            Dict containing the Figma file data
        """
        url = f"{self.base_url}/files/{file_key}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_images(self, file_key: str, node_ids: list, format: str = "png", scale: int = 2) -> Dict[str, str]:
        """
        Get image URLs for specific nodes.
        
        Args:
            file_key: The Figma file key
            node_ids: List of node IDs to render
            format: Image format (png, jpg, svg, pdf)
            scale: Scale factor for the images
            
        Returns:
            Dict mapping node IDs to image URLs
        """
        if not node_ids:
            return {}
        
        url = f"{self.base_url}/images/{file_key}"
        params = {
            "ids": ",".join(node_ids),
            "format": format,
            "scale": scale
        }
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json().get("images", {})