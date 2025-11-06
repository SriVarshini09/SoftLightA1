from typing import Dict, Any, List

class LayoutConverter:
    """Converts Figma layout properties to CSS"""
    
    @staticmethod
    def get_position_styles(node: Dict[str, Any], parent: Dict[str, Any] = None) -> List[str]:
        """Extract positioning styles from a node"""
        styles = []
        
        # Get absolute bounding box
        abs_box = node.get('absoluteBoundingBox', {})
        x = abs_box.get('x', 0)
        y = abs_box.get('y', 0)
        
        # If we have a parent, calculate relative position
        if parent and 'absoluteBoundingBox' in parent:
            parent_box = parent['absoluteBoundingBox']
            x = x - parent_box.get('x', 0)
            y = y - parent_box.get('y', 0)
        
        # Check layout mode for parent
        if parent:
            layout_mode = parent.get('layoutMode')
            
            # If parent uses auto-layout, don't use absolute positioning
            if layout_mode in ['HORIZONTAL', 'VERTICAL']:
                # Child is positioned by flexbox
                return styles
        
        # Use absolute positioning for most cases
        styles.append("position: absolute;")
        styles.append(f"left: {x}px;")
        styles.append(f"top: {y}px;")
        
        return styles
    
    @staticmethod
    def get_size_styles(node: Dict[str, Any]) -> List[str]:
        """Extract size styles from a node"""
        styles = []
        
        # Get absolute bounding box for size
        abs_box = node.get('absoluteBoundingBox', {})
        width = abs_box.get('width', 0)
        height = abs_box.get('height', 0)
        
        # Check for layout sizing constraints
        layout_sizing_h = node.get('layoutSizingHorizontal')
        layout_sizing_v = node.get('layoutSizingVertical')
        
        # Handle width
        if layout_sizing_h == 'FILL':
            styles.append("width: 100%;")
        elif layout_sizing_h == 'HUG':
            styles.append("width: fit-content;")
        else:
            if width > 0:
                styles.append(f"width: {width}px;")
        
        # Handle height
        if layout_sizing_v == 'FILL':
            styles.append("height: 100%;")
        elif layout_sizing_v == 'HUG':
            styles.append("height: fit-content;")
        else:
            if height > 0:
                styles.append(f"height: {height}px;")
        
        return styles
    
    @staticmethod
    def get_auto_layout_styles(node: Dict[str, Any]) -> List[str]:
        """Extract auto-layout (flexbox) styles from a node"""
        styles = []
        
        layout_mode = node.get('layoutMode')
        
        if not layout_mode or layout_mode == 'NONE':
            return styles
        
        # Enable flexbox
        styles.append("display: flex;")
        
        # Set flex direction
        if layout_mode == 'HORIZONTAL':
            styles.append("flex-direction: row;")
        elif layout_mode == 'VERTICAL':
            styles.append("flex-direction: column;")
        
        # Primary axis alignment
        primary_align = node.get('primaryAxisAlignItems', 'MIN')
        if layout_mode == 'HORIZONTAL':
            if primary_align == 'MIN':
                styles.append("justify-content: flex-start;")
            elif primary_align == 'CENTER':
                styles.append("justify-content: center;")
            elif primary_align == 'MAX':
                styles.append("justify-content: flex-end;")
            elif primary_align == 'SPACE_BETWEEN':
                styles.append("justify-content: space-between;")
        else:  # VERTICAL
            if primary_align == 'MIN':
                styles.append("justify-content: flex-start;")
            elif primary_align == 'CENTER':
                styles.append("justify-content: center;")
            elif primary_align == 'MAX':
                styles.append("justify-content: flex-end;")
            elif primary_align == 'SPACE_BETWEEN':
                styles.append("justify-content: space-between;")
        
        # Counter axis alignment
        counter_align = node.get('counterAxisAlignItems', 'MIN')
        if counter_align == 'MIN':
            styles.append("align-items: flex-start;")
        elif counter_align == 'CENTER':
            styles.append("align-items: center;")
        elif counter_align == 'MAX':
            styles.append("align-items: flex-end;")
        elif counter_align == 'BASELINE':
            styles.append("align-items: baseline;")
        
        # Item spacing (gap)
        item_spacing = node.get('itemSpacing', 0)
        if item_spacing > 0:
            styles.append(f"gap: {item_spacing}px;")
        
        # Padding
        padding_left = node.get('paddingLeft', 0)
        padding_right = node.get('paddingRight', 0)
        padding_top = node.get('paddingTop', 0)
        padding_bottom = node.get('paddingBottom', 0)
        
        if padding_left == padding_right == padding_top == padding_bottom:
            if padding_left > 0:
                styles.append(f"padding: {padding_left}px;")
        else:
            if padding_top > 0 or padding_right > 0 or padding_bottom > 0 or padding_left > 0:
                styles.append(f"padding: {padding_top}px {padding_right}px {padding_bottom}px {padding_left}px;")
        
        # Flex wrap
        layout_wrap = node.get('layoutWrap', 'NO_WRAP')
        if layout_wrap == 'WRAP':
            styles.append("flex-wrap: wrap;")
        
        return styles
    
    @staticmethod
    def get_constraints_styles(node: Dict[str, Any]) -> List[str]:
        """Extract constraint styles from a node"""
        styles = []
        
        constraints = node.get('constraints', {})
        
        # Horizontal constraints
        h_constraint = constraints.get('horizontal')
        if h_constraint == 'LEFT_RIGHT':
            styles.append("left: 0;")
            styles.append("right: 0;")
        elif h_constraint == 'RIGHT':
            styles.append("right: 0;")
        elif h_constraint == 'CENTER':
            styles.append("left: 50%;")
            styles.append("transform: translateX(-50%);")
        elif h_constraint == 'SCALE':
            styles.append("width: 100%;")
        
        # Vertical constraints
        v_constraint = constraints.get('vertical')
        if v_constraint == 'TOP_BOTTOM':
            styles.append("top: 0;")
            styles.append("bottom: 0;")
        elif v_constraint == 'BOTTOM':
            styles.append("bottom: 0;")
        elif v_constraint == 'CENTER':
            styles.append("top: 50%;")
            styles.append("transform: translateY(-50%);")
        elif v_constraint == 'SCALE':
            styles.append("height: 100%;")
        
        return styles
    
    @staticmethod
    def get_overflow_styles(node: Dict[str, Any]) -> List[str]:
        """Extract overflow/clipping styles"""
        styles = []
        
        # Check if clipping is enabled
        clips_content = node.get('clipsContent', False)
        if clips_content:
            styles.append("overflow: hidden;")
        
        return styles
    
    @staticmethod
    def get_transform_styles(node: Dict[str, Any]) -> List[str]:
        """Extract transformation styles (rotation, etc.)"""
        styles = []
        
        # Rotation
        rotation = node.get('rotation')
        if rotation and rotation != 0:
            styles.append(f"transform: rotate({rotation}deg);")
        
        # Relative transform (for more complex transforms)
        relative_transform = node.get('relativeTransform')
        if relative_transform and isinstance(relative_transform, list) and len(relative_transform) >= 2:
            # This is a 2D transformation matrix
            # [[a, b, tx], [c, d, ty]]
            # For now, we'll handle simple cases
            pass
        
        return styles
    
    @staticmethod
    def should_use_relative_position(parent: Dict[str, Any]) -> bool:
        """Determine if children should use relative positioning"""
        if not parent:
            return False
        
        layout_mode = parent.get('layoutMode')
        return layout_mode in ['HORIZONTAL', 'VERTICAL']