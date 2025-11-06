from typing import Dict, Any, List, Optional
from style_converter import StyleConverter
from layout_converter import LayoutConverter
import html

class HTMLGenerator:
    """Generates HTML and CSS from Figma nodes"""
    
    def __init__(self):
        self.css_classes = {}
        self.class_counter = 0
        self.style_converter = StyleConverter()
        self.layout_converter = LayoutConverter()
    
    def generate_html_css(self, figma_data: Dict[str, Any]) -> tuple[str, str]:
        """
        Generate HTML and CSS from Figma file data.
        
        Args:
            figma_data: The Figma file data from the API
            
        Returns:
            Tuple of (html_string, css_string)
        """
        document = figma_data.get('document', {})
        
        # Find the first page/canvas
        children = document.get('children', [])
        if not children:
            return "<div>No content</div>", ""
        
        # Process the first page
        page = children[0]
        
        # Generate HTML for the page
        html_content = self._generate_node_html(page, None)
        
        # Generate CSS
        css_content = self._generate_css()
        
        # Wrap in complete HTML document
        full_html = self._wrap_html(html_content)
        
        return full_html, css_content
    
    def _generate_node_html(self, node: Dict[str, Any], parent: Dict[str, Any] = None, depth: int = 0) -> str:
        """
        Recursively generate HTML for a Figma node and its children.
        
        Args:
            node: The Figma node
            parent: The parent node
            depth: Current depth in the tree
            
        Returns:
            HTML string
        """
        node_type = node.get('type')
        node_name = node.get('name', 'unnamed')
        
        # Skip certain node types
        if node_type in ['DOCUMENT', 'CANVAS']:
            # Just process children
            html_parts = []
            for child in node.get('children', []):
                child_html = self._generate_node_html(child, node, depth)
                if child_html:
                    html_parts.append(child_html)
            return '\n'.join(html_parts)
        
        # Check if node is visible
        if not node.get('visible', True):
            return ''
        
        # Generate CSS class for this node
        class_name = self._generate_class_name(node)
        
        # Collect all styles for this node
        styles = self._collect_styles(node, parent)
        
        # Store styles in CSS classes
        self.css_classes[class_name] = styles
        
        # Generate HTML based on node type
        if node_type == 'TEXT':
            return self._generate_text_html(node, class_name)
        elif node_type == 'FRAME' or node_type == 'GROUP' or node_type == 'COMPONENT' or node_type == 'INSTANCE':
            return self._generate_container_html(node, class_name, parent, depth)
        elif node_type == 'RECTANGLE' or node_type == 'ELLIPSE' or node_type == 'VECTOR' or node_type == 'STAR' or node_type == 'POLYGON':
            return self._generate_shape_html(node, class_name, parent, depth)
        else:
            # Default: treat as container
            return self._generate_container_html(node, class_name, parent, depth)
    
    def _generate_text_html(self, node: Dict[str, Any], class_name: str) -> str:
        """Generate HTML for a text node"""
        text_content = node.get('characters', '')
        # Escape HTML special characters
        text_content = html.escape(text_content)
        # Preserve line breaks
        text_content = text_content.replace('\n', '<br>')
        
        return f'<div class="{class_name}">{text_content}</div>'
    
    def _generate_container_html(self, node: Dict[str, Any], class_name: str, parent: Dict[str, Any], depth: int) -> str:
        """Generate HTML for a container node (frame, group, etc.)"""
        children = node.get('children', [])
        
        # Generate HTML for children
        children_html = []
        for child in children:
            child_html = self._generate_node_html(child, node, depth + 1)
            if child_html:
                children_html.append(child_html)
        
        children_content = '\n'.join(children_html)
        
        return f'<div class="{class_name}">\n{children_content}\n</div>'
    
    def _generate_shape_html(self, node: Dict[str, Any], class_name: str, parent: Dict[str, Any], depth: int) -> str:
        """Generate HTML for a shape node"""
        # Check if it has children (unlikely for shapes, but possible)
        children = node.get('children', [])
        
        if children:
            children_html = []
            for child in children:
                child_html = self._generate_node_html(child, node, depth + 1)
                if child_html:
                    children_html.append(child_html)
            children_content = '\n'.join(children_html)
            return f'<div class="{class_name}">\n{children_content}\n</div>'
        else:
            return f'<div class="{class_name}"></div>'
    
    def _collect_styles(self, node: Dict[str, Any], parent: Dict[str, Any] = None) -> List[str]:
        """Collect all CSS styles for a node"""
        styles = []
        
        # Layout styles
        styles.extend(self.layout_converter.get_auto_layout_styles(node))
        styles.extend(self.layout_converter.get_position_styles(node, parent))
        styles.extend(self.layout_converter.get_size_styles(node))
        styles.extend(self.layout_converter.get_overflow_styles(node))
        styles.extend(self.layout_converter.get_transform_styles(node))
        
        # Visual styles
        styles.extend(self.style_converter.get_background_styles(node))
        styles.extend(self.style_converter.get_border_styles(node))
        styles.extend(self.style_converter.get_border_radius(node))
        styles.extend(self.style_converter.get_effect_styles(node))
        styles.extend(self.style_converter.get_opacity(node))
        styles.extend(self.style_converter.get_blend_mode(node))
        
        # Text styles (if it's a text node)
        if node.get('type') == 'TEXT':
            styles.extend(self.style_converter.get_text_styles(node))
            # Add text-specific display properties
            if 'display: flex;' not in styles:
                styles.append('display: flex;')
            styles.append('align-items: center;')
        
        return styles
    
    def _generate_class_name(self, node: Dict[str, Any]) -> str:
        """Generate a unique CSS class name for a node"""
        node_id = node.get('id', '')
        node_name = node.get('name', 'element')
        
        # Sanitize name for use in CSS class
        safe_name = ''.join(c if c.isalnum() or c == '-' else '_' for c in node_name.lower())
        safe_name = safe_name[:30]  # Limit length
        
        # Create unique class name
        self.class_counter += 1
        return f"figma-{safe_name}-{self.class_counter}"
    
    def _generate_css(self) -> str:
        """Generate CSS from collected styles"""
        css_parts = []
        
        # Add reset and base styles
        css_parts.append("""/* Base styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
}

/* Figma styles */""")
        
        # Add each class
        for class_name, styles in self.css_classes.items():
            if styles:
                css_parts.append(f".{class_name} {{")
                for style in styles:
                    css_parts.append(f"    {style}")
                css_parts.append("}\n")
        
        return '\n'.join(css_parts)
    
    def _wrap_html(self, content: str) -> str:
        """Wrap content in a complete HTML document"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma to HTML</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
{content}
</body>
</html>"""
    
    def save_to_files(self, html: str, css: str, output_dir: str = "output"):
        """Save HTML and CSS to files"""
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write HTML file
        html_path = os.path.join(output_dir, "index.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Write CSS file
        css_path = os.path.join(output_dir, "styles.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
        
        print(f"HTML saved to: {html_path}")
        print(f"CSS saved to: {css_path}")