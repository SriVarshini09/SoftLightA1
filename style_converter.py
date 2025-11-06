from typing import Dict, Any, List, Optional
import math

class StyleConverter:
    """Converts Figma styles to CSS"""
    
    @staticmethod
    def rgba_to_css(color: Dict[str, float]) -> str:
        """Convert Figma RGBA color to CSS rgba string"""
        r = int(color.get('r', 0) * 255)
        g = int(color.get('g', 0) * 255)
        b = int(color.get('b', 0) * 255)
        a = color.get('a', 1)
        return f"rgba({r}, {g}, {b}, {a})"
    
    @staticmethod
    def get_background_styles(node: Dict[str, Any]) -> List[str]:
        """Extract background styles from a node"""
        styles = []
        fills = node.get('fills', [])
        
        if not fills or not isinstance(fills, list):
            return styles
        
        for fill in fills:
            if not fill.get('visible', True):
                continue
                
            fill_type = fill.get('type')
            opacity = fill.get('opacity', 1)
            
            if fill_type == 'SOLID':
                color = fill.get('color', {})
                rgba = StyleConverter.rgba_to_css(color)
                # Apply opacity to the color
                if opacity < 1:
                    parts = rgba.replace('rgba(', '').replace(')', '').split(',')
                    if len(parts) == 4:
                        parts[3] = str(float(parts[3].strip()) * opacity)
                        rgba = f"rgba({','.join(parts)})"
                styles.append(f"background-color: {rgba};")
            
            elif fill_type == 'GRADIENT_LINEAR':
                gradient = StyleConverter._convert_linear_gradient(fill)
                if gradient:
                    styles.append(f"background: {gradient};")
            
            elif fill_type == 'GRADIENT_RADIAL':
                gradient = StyleConverter._convert_radial_gradient(fill)
                if gradient:
                    styles.append(f"background: {gradient};")
            
            elif fill_type == 'GRADIENT_ANGULAR':
                gradient = StyleConverter._convert_angular_gradient(fill)
                if gradient:
                    styles.append(f"background: {gradient};")
            
            elif fill_type == 'IMAGE':
                # Handle image fills
                image_ref = fill.get('imageRef')
                if image_ref:
                    styles.append(f"/* background-image: requires image ref {image_ref} */")
        
        return styles
    
    @staticmethod
    def _convert_linear_gradient(fill: Dict[str, Any]) -> Optional[str]:
        """Convert Figma linear gradient to CSS"""
        gradient_stops = fill.get('gradientStops', [])
        if not gradient_stops:
            return None
        
        # Get gradient transform handles
        handles = fill.get('gradientHandlePositions', [])
        
        # Calculate angle from handles
        angle = 180  # Default angle
        if len(handles) >= 2:
            x1, y1 = handles[0].get('x', 0), handles[0].get('y', 0)
            x2, y2 = handles[1].get('x', 1), handles[1].get('y', 1)
            
            dx = x2 - x1
            dy = y2 - y1
            angle = math.degrees(math.atan2(dy, dx)) + 90
        
        # Build color stops
        stops = []
        for stop in gradient_stops:
            color = StyleConverter.rgba_to_css(stop.get('color', {}))
            position = stop.get('position', 0) * 100
            stops.append(f"{color} {position:.1f}%")
        
        return f"linear-gradient({angle:.1f}deg, {', '.join(stops)})"
    
    @staticmethod
    def _convert_radial_gradient(fill: Dict[str, Any]) -> Optional[str]:
        """Convert Figma radial gradient to CSS"""
        gradient_stops = fill.get('gradientStops', [])
        if not gradient_stops:
            return None
        
        stops = []
        for stop in gradient_stops:
            color = StyleConverter.rgba_to_css(stop.get('color', {}))
            position = stop.get('position', 0) * 100
            stops.append(f"{color} {position:.1f}%")
        
        return f"radial-gradient(circle, {', '.join(stops)})"
    
    @staticmethod
    def _convert_angular_gradient(fill: Dict[str, Any]) -> Optional[str]:
        """Convert Figma angular gradient to CSS (conic gradient)"""
        gradient_stops = fill.get('gradientStops', [])
        if not gradient_stops:
            return None
        
        stops = []
        for stop in gradient_stops:
            color = StyleConverter.rgba_to_css(stop.get('color', {}))
            position = stop.get('position', 0) * 360
            stops.append(f"{color} {position:.1f}deg")
        
        return f"conic-gradient({', '.join(stops)})"
    
    @staticmethod
    def get_border_styles(node: Dict[str, Any]) -> List[str]:
        """Extract border styles from a node"""
        styles = []
        strokes = node.get('strokes', [])
        stroke_weight = node.get('strokeWeight', 0)
        stroke_align = node.get('strokeAlign', 'INSIDE')
        
        if not strokes or stroke_weight == 0:
            return styles
        
        for stroke in strokes:
            if not stroke.get('visible', True):
                continue
            
            stroke_type = stroke.get('type')
            if stroke_type == 'SOLID':
                color = StyleConverter.rgba_to_css(stroke.get('color', {}))
                styles.append(f"border: {stroke_weight}px solid {color};")
                
                # Handle stroke alignment
                if stroke_align == 'OUTSIDE':
                    styles.append("box-sizing: content-box;")
                elif stroke_align == 'CENTER':
                    # CSS borders are centered by default
                    pass
            elif stroke_type == 'GRADIENT_LINEAR':
                # Gradient borders require border-image
                gradient = StyleConverter._convert_linear_gradient(stroke)
                if gradient:
                    styles.append(f"border: {stroke_weight}px solid;")
                    styles.append(f"border-image: {gradient} 1;")
        
        # Handle individual stroke weights
        if 'individualStrokeWeights' in node:
            weights = node['individualStrokeWeights']
            styles.append(f"border-top-width: {weights.get('top', stroke_weight)}px;")
            styles.append(f"border-right-width: {weights.get('right', stroke_weight)}px;")
            styles.append(f"border-bottom-width: {weights.get('bottom', stroke_weight)}px;")
            styles.append(f"border-left-width: {weights.get('left', stroke_weight)}px;")
        
        return styles
    
    @staticmethod
    def get_border_radius(node: Dict[str, Any]) -> List[str]:
        """Extract border radius styles"""
        styles = []
        
        # Check for uniform corner radius
        if 'cornerRadius' in node:
            radius = node['cornerRadius']
            if radius > 0:
                styles.append(f"border-radius: {radius}px;")
        
        # Check for individual corner radii
        if 'rectangleCornerRadii' in node:
            radii = node['rectangleCornerRadii']
            if len(radii) == 4:
                styles.append(f"border-radius: {radii[0]}px {radii[1]}px {radii[2]}px {radii[3]}px;")
        
        return styles
    
    @staticmethod
    def get_text_styles(node: Dict[str, Any]) -> List[str]:
        """Extract text/typography styles from a node"""
        styles = []
        
        style = node.get('style', {})
        
        # Font family
        if 'fontFamily' in style:
            font_family = style['fontFamily']
            styles.append(f"font-family: '{font_family}', sans-serif;")
        
        # Font size
        if 'fontSize' in style:
            styles.append(f"font-size: {style['fontSize']}px;")
        
        # Font weight
        if 'fontWeight' in style:
            styles.append(f"font-weight: {style['fontWeight']};")
        
        # Line height
        if 'lineHeightPx' in style:
            styles.append(f"line-height: {style['lineHeightPx']}px;")
        elif 'lineHeightPercent' in style:
            percent = style['lineHeightPercent']
            styles.append(f"line-height: {percent / 100};")
        elif 'lineHeightPercentFontSize' in style:
            percent = style['lineHeightPercentFontSize']
            styles.append(f"line-height: {percent / 100};")
        
        # Letter spacing
        if 'letterSpacing' in style:
            styles.append(f"letter-spacing: {style['letterSpacing']}px;")
        
        # Text alignment
        if 'textAlignHorizontal' in style:
            align = style['textAlignHorizontal'].lower()
            if align in ['left', 'right', 'center', 'justified']:
                align = 'justify' if align == 'justified' else align
                styles.append(f"text-align: {align};")
        
        # Vertical alignment
        if 'textAlignVertical' in style:
            v_align = style['textAlignVertical'].lower()
            if v_align == 'top':
                styles.append("align-items: flex-start;")
            elif v_align == 'center':
                styles.append("align-items: center;")
            elif v_align == 'bottom':
                styles.append("align-items: flex-end;")
        
        # Text decoration
        if 'textDecoration' in style:
            decoration = style['textDecoration'].lower()
            if decoration in ['underline', 'line-through', 'strikethrough']:
                decoration = 'line-through' if decoration == 'strikethrough' else decoration
                styles.append(f"text-decoration: {decoration};")
        
        # Text transform
        if 'textCase' in style:
            case = style['textCase']
            if case == 'UPPER':
                styles.append("text-transform: uppercase;")
            elif case == 'LOWER':
                styles.append("text-transform: lowercase;")
            elif case == 'TITLE':
                styles.append("text-transform: capitalize;")
        
        return styles
    
    @staticmethod
    def get_effect_styles(node: Dict[str, Any]) -> List[str]:
        """Extract effects (shadows, blur) from a node"""
        styles = []
        effects = node.get('effects', [])
        
        if not effects:
            return styles
        
        box_shadows = []
        
        for effect in effects:
            if not effect.get('visible', True):
                continue
            
            effect_type = effect.get('type')
            
            if effect_type == 'DROP_SHADOW':
                offset = effect.get('offset', {})
                x = offset.get('x', 0)
                y = offset.get('y', 0)
                radius = effect.get('radius', 0)
                color = StyleConverter.rgba_to_css(effect.get('color', {}))
                box_shadows.append(f"{x}px {y}px {radius}px {color}")
            
            elif effect_type == 'INNER_SHADOW':
                offset = effect.get('offset', {})
                x = offset.get('x', 0)
                y = offset.get('y', 0)
                radius = effect.get('radius', 0)
                color = StyleConverter.rgba_to_css(effect.get('color', {}))
                box_shadows.append(f"inset {x}px {y}px {radius}px {color}")
            
            elif effect_type == 'LAYER_BLUR':
                radius = effect.get('radius', 0)
                if radius > 0:
                    styles.append(f"filter: blur({radius}px);")
            
            elif effect_type == 'BACKGROUND_BLUR':
                radius = effect.get('radius', 0)
                if radius > 0:
                    styles.append(f"backdrop-filter: blur({radius}px);")
        
        if box_shadows:
            styles.append(f"box-shadow: {', '.join(box_shadows)};")
        
        return styles
    
    @staticmethod
    def get_opacity(node: Dict[str, Any]) -> List[str]:
        """Extract opacity style"""
        styles = []
        opacity = node.get('opacity', 1)
        if opacity < 1:
            styles.append(f"opacity: {opacity};")
        return styles
    
    @staticmethod
    def get_blend_mode(node: Dict[str, Any]) -> List[str]:
        """Extract blend mode style"""
        styles = []
        blend_mode = node.get('blendMode', 'PASS_THROUGH')
        
        # Map Figma blend modes to CSS
        blend_mode_map = {
            'NORMAL': 'normal',
            'DARKEN': 'darken',
            'MULTIPLY': 'multiply',
            'COLOR_BURN': 'color-burn',
            'LIGHTEN': 'lighten',
            'SCREEN': 'screen',
            'COLOR_DODGE': 'color-dodge',
            'OVERLAY': 'overlay',
            'SOFT_LIGHT': 'soft-light',
            'HARD_LIGHT': 'hard-light',
            'DIFFERENCE': 'difference',
            'EXCLUSION': 'exclusion',
            'HUE': 'hue',
            'SATURATION': 'saturation',
            'COLOR': 'color',
            'LUMINOSITY': 'luminosity',
        }
        
        if blend_mode in blend_mode_map:
            css_blend = blend_mode_map[blend_mode]
            styles.append(f"mix-blend-mode: {css_blend};")
        
        return styles