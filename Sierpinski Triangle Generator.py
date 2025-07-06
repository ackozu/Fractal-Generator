import svgwrite
import math
import os

def sierpinski_triangle(dwg, p1, p2, p3, depth):
    """
    Recursively draws a Sierpinski triangle.

    Args:
        dwg (svgwrite.Drawing): The drawing object to add shapes to.
        p1 (tuple): Coordinates of the first vertex (x, y).
        p2 (tuple): Coordinates of the second vertex (x, y).
        p3 (tuple): Coordinates of the third vertex (x, y).
        depth (int): The current recursion depth.
    """
    if depth == 0:
        # Draw the triangle with a white fill and NO stroke
        dwg.add(dwg.polygon([p1, p2, p3], fill='white', stroke='none'))
    else:
        # Calculate midpoints
        mid12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        mid23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        mid31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)

        # Recursively call for the three outer triangles
        sierpinski_triangle(dwg, p1, mid12, mid31, depth - 1)
        sierpinski_triangle(dwg, mid12, p2, mid23, depth - 1)
        sierpinski_triangle(dwg, mid31, mid23, p3, depth - 1)

def create_fractal_svg(filename="sierpinski.svg", width=800, height=700, initial_depth=5):
    """
    Creates an SVG file of a Sierpinski triangle.

    Args:
        filename (str): The name of the SVG file to save.
        width (int): Width of the SVG canvas.
        height (int): Height of the SVG canvas.
        initial_depth (int): The maximum recursion depth for the fractal.
    """
    print(f"Attempting to create SVG file: {filename}")
    print(f"Current working directory: {os.getcwd()}")

    try:
        dwg = svgwrite.Drawing(filename, size=(width, height), profile='full')

        # Define the initial large triangle points
        side_length = min(width, height) * 0.7
        h = side_length * (math.sqrt(3) / 2)

        p_bl = (width / 2 - side_length / 2, height / 2 + h / 2)
        p_br = (width / 2 + side_length / 2, height / 2 + h / 2)
        p_top = (width / 2, height / 2 - h / 2)

        # Start the recursive drawing
        sierpinski_triangle(dwg, p_top, p_bl, p_br, initial_depth)

        dwg.save()
        print(f"SUCCESS: Fractal saved to {filename}")
    except Exception as e:
        print(f"ERROR: Failed to save SVG file. Details: {e}")
        print(f"Check if you have write permissions in {os.getcwd()}")

if __name__ == "__main__":
    # Get the directory of the current script to save the SVG next to it
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # *** Changed the output_file_name here ***
    output_file_name = "Sierpinski_Triangle.svg"
    output_path = os.path.join(script_dir, output_file_name)

    create_fractal_svg(filename=output_path, width=1000, height=900, initial_depth=8)