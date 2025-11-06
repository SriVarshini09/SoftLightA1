# Figma to HTML/CSS Converter

A comprehensive system that converts Figma design files into HTML and CSS using the Figma REST API. The system aims to produce pixel-perfect representations of Figma designs, handling layout, typography, colors, borders, gradients, effects, and more.

## Features

### Layout & Positioning
- ✅ **Auto-layout** (Flexbox) support with horizontal/vertical layout modes
- ✅ **Absolute positioning** for non-auto-layout frames
- ✅ **Size constraints** (fixed, fill, hug content)
- ✅ **Padding and spacing** (item spacing, gap)
- ✅ **Alignment** (primary and counter axis alignment)
- ✅ **Overflow** handling (clipsContent)

### Visual Styling
- ✅ **Solid colors** with opacity
- ✅ **Linear gradients** with angle calculation
- ✅ **Radial gradients**
- ✅ **Conic/Angular gradients**
- ✅ **Multiple fills** support
- ✅ **Border radius** (uniform and individual corners)
- ✅ **Borders/Strokes** with different alignments (inside, outside, center)
- ✅ **Individual stroke weights**
- ✅ **Gradient borders** using border-image

### Typography
- ✅ **Font family**, size, and weight
- ✅ **Line height** (px and percent)
- ✅ **Letter spacing**
- ✅ **Text alignment** (horizontal and vertical)
- ✅ **Text decoration** (underline, strikethrough)
- ✅ **Text transform** (uppercase, lowercase, capitalize)
- ✅ **Line breaks** preserved

### Effects
- ✅ **Drop shadows**
- ✅ **Inner shadows**
- ✅ **Layer blur**
- ✅ **Background blur** (backdrop-filter)
- ✅ **Opacity**
- ✅ **Blend modes** (multiply, screen, overlay, etc.)

### Node Types
- ✅ **Frames** (with and without auto-layout)
- ✅ **Groups**
- ✅ **Components** and instances
- ✅ **Text** nodes
- ✅ **Shapes** (rectangles, ellipses, vectors, etc.)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Figma API token:**
   - Go to [Figma](https://www.figma.com/)
   - Click on your profile icon → Settings
   - Scroll to "Personal Access Tokens"
   - Click "Create new token" and copy it

4. **Set up your API token** (choose one method):
   
   **Option A: Environment variable (recommended)**
   ```bash
   # Create a .env file
   echo "FIGMA_API_TOKEN=your_token_here" > .env
   ```
   
   **Option B: Command line argument**
   ```bash
   python figam_to_html.py <file_key> --token your_token_here
   ```

## Usage

### Basic Usage

```bash
python figam_to_html.py <figma_file_key_or_url>
```

### Examples

**Using file key:**
```bash
python figam_to_html.py abc123xyz456
```

**Using full Figma URL:**
```bash
python figam_to_html.py https://www.figma.com/file/abc123xyz456/MyDesign
```

**Specify output directory:**
```bash
python figam_to_html.py abc123xyz456 --output ./my-output
```

**With API token:**
```bash
python figam_to_html.py abc123xyz456 --token figd_abc123...
```

**Save raw Figma JSON for debugging:**
```bash
python figam_to_html.py abc123xyz456 --save-json
```

### Command Line Options

```
usage: figam_to_html.py [-h] [--output OUTPUT] [--token TOKEN] 
                        [--save-json] [--page PAGE] figma_file

positional arguments:
  figma_file            Figma file key or full Figma file URL

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output directory for HTML/CSS files (default: output)
  --token TOKEN, -t TOKEN
                        Figma API token (or set FIGMA_API_TOKEN env variable)
  --save-json           Save the raw Figma API response as JSON for debugging
  --page PAGE           Page index to convert (default: 0, first page)
```

## Output

The converter generates two files in the output directory:

1. **`index.html`** - The HTML structure
2. **`styles.css`** - All CSS styles

Open `index.html` in any modern web browser to view the result.

## How It Works

### Architecture

The system consists of four main modules:

1. **`figma_client.py`** - Handles communication with Figma REST API
2. **`style_converter.py`** - Converts Figma visual styles to CSS
3. **`layout_converter.py`** - Converts Figma layout properties to CSS
4. **`html_generator.py`** - Orchestrates the conversion and generates HTML/CSS
5. **`figam_to_html.py`** - Main CLI script

### Conversion Process

1. **Fetch Figma file** using the REST API
2. **Traverse the node tree** recursively
3. **For each node:**
   - Generate a unique CSS class
   - Extract layout properties (position, size, flexbox)
   - Extract visual styles (colors, borders, effects)
   - Extract text styles (if text node)
4. **Generate HTML** with appropriate structure
5. **Generate CSS** with all collected styles
6. **Save** to files

### Key Design Decisions

- **Absolute positioning by default** for non-auto-layout frames
- **Flexbox** for auto-layout containers
- **Unique CSS classes** for each element (no inline styles)
- **Separate HTML and CSS files** for better maintainability
- **Preserves hierarchy** from Figma's node tree

## Known Limitations

### High Priority Limitations

1. **Image fills** - Images from Figma are not downloaded; only placeholders are generated
2. **Vector graphics** - Complex vector paths are rendered as divs, not SVGs
3. **Boolean operations** - Union, subtract, intersect operations on vectors are not supported
4. **Masks** - Clipping masks and layer masks have limited support
5. **Prototyping interactions** - Interactive elements and transitions are not converted

### Medium Priority Limitations

6. **Component variants** - Variant properties are not preserved
7. **Styles and variables** - Figma's reusable styles are not converted to CSS variables
8. **Grid layouts** - Auto-layout grid mode is not yet supported
9. **Advanced text features** - Text spans with different styles within a single text node
10. **Stroke caps and joins** - Detailed stroke properties are not fully supported
11. **Text overflow** - Text truncation and auto-resizing behaviors

### Low Priority Limitations

12. **Plugins** - Any plugin-generated content or data is not accessible
13. **Animations** - Figma smart animate and motion are not converted
14. **3D transforms** - Only 2D transforms are supported
15. **Responsive behavior** - Constraints work differently than Figma's responsive resize
16. **Advanced blend modes** - Some blend modes may render differently across browsers

## Improving the System

### To Handle Complex Designs

1. **Add SVG support** for vectors using the Figma images endpoint
2. **Download images** and embed them properly
3. **Handle components** by creating reusable CSS classes
4. **Add CSS variables** for colors and styles used multiple times
5. **Implement masks** using CSS clip-path

### To Improve Accuracy

1. **Better gradient angle calculation** for more accurate linear gradients
2. **Text overflow handling** for long text content
3. **More precise positioning** for complex nested structures
4. **Font loading** - import fonts from Google Fonts or other CDNs

### To Add Features

1. **Responsive CSS** - generate media queries for different screen sizes
2. **Semantic HTML** - use appropriate HTML tags (button, nav, header, etc.)
3. **Accessibility** - add ARIA labels and semantic structure
4. **Optimization** - minimize CSS, combine similar styles

## Testing

### Manual Testing

1. Copy a Figma file to your workspace
2. Get the file key from the URL
3. Run the converter:
   ```bash
   python figam_to_html.py <your_file_key> --save-json
   ```
4. Open `output/index.html` in a browser
5. Compare with the original Figma design

### Debugging

Use the `--save-json` flag to save the raw Figma API response:
```bash
python figam_to_html.py <file_key> --save-json
```

This creates `figma_data.json` in the output directory, which you can inspect to understand the Figma node structure.

## Example Figma File

The system has been tested with various Figma designs including:
- Simple layouts with text and shapes
- Auto-layout frames (horizontal and vertical)
- Gradients (linear, radial, angular)
- Shadows and blur effects
- Nested components
- Different border styles

## Contributing

To extend or improve this system:

1. **Add new style converters** in `style_converter.py`
2. **Enhance layout handling** in `layout_converter.py`
3. **Improve node type support** in `html_generator.py`
4. **Add new API endpoints** in `figma_client.py`

## Resources

- [Figma REST API Documentation](https://www.figma.com/developers/api)
- [Figma File Format](https://www.figma.com/developers/api#files)
- [CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)

## License

This project is provided as-is for educational and evaluation purposes.

## Author

Created for the Softlight Engineering Take-Home Assignment.