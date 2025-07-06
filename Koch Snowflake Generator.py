import svgwrite
import math
import os

def get_koch_points(current_p1, current_p2, current_depth, all_points_list):
    """
    Recursively calculates points for a Koch curve segment and appends them to a list.
    """
    if current_depth == 0:
        all_points_list.append(current_p1)
    else:
        dx = current_p2[0] - current_p1[0]
        dy = current_p2[1] - current_p1[1]

        len_seg_third = math.sqrt(dx*dx + dy*dy) / 3
        angle_rad = math.atan2(dy, dx) # Angle of the line p1 -> p2

        A = (current_p1[0] + dx/3, current_p1[1] + dy/3)
        B = (current_p1[0] + 2*dx/3, current_p1[1] + 2*dy/3)

        # Point C (the peak of the triangle, rotated +60 degrees from vector AB)
        Cx = A[0] + (len_seg_third * math.cos(angle_rad - math.pi/3))
        Cy = A[1] + (len_seg_third * math.sin(angle_rad - math.pi/3))

        get_koch_points(current_p1, A, current_depth - 1, all_points_list)
        get_koch_points(A, (Cx, Cy), current_depth - 1, all_points_list)
        get_koch_points((Cx, Cy), B, current_depth - 1, all_points_list)
        get_koch_points(B, current_p2, current_depth - 1, all_points_list)


def create_koch_snowflake_svg(filename="Koch_Snowflake.svg", size=800, depth=4, stroke_color='black', fill_color='none'):
    """
    Creates an SVG file of a Koch Snowflake.
    """
    print(f"Attempting to create SVG file: {filename}")
    print(f"Current working directory: {os.getcwd()}")

    try:
        dwg = svgwrite.Drawing(filename, size=(size, size), profile='full')

        side_length = size * 0.7
        h = side_length * (math.sqrt(3) / 2)

        p1_x = (size / 2) - (side_length / 2)
        p1_y = (size / 2) + (h / 2)

        p2_x = (size / 2) + (side_length / 2)
        p2_y = (size / 2) + (h / 2)

        p3_x = (size / 2)
        p3_y = (size / 2) - (h / 2)

        p1 = (p1_x, p1_y)
        p2 = (p2_x, p2_y)
        p3 = (p3_x, p3_y)

        all_snowflake_points = []

        get_koch_points(p1, p2, depth, all_snowflake_points)
        get_koch_points(p2, p3, depth, all_snowflake_points)
        get_koch_points(p3, p1, depth, all_snowflake_points)

        all_snowflake_points.append(all_snowflake_points[0])

        dwg.add(dwg.polyline(all_snowflake_points, stroke=stroke_color, fill=fill_color, stroke_width=1))

        dwg.save()
        print(f"SUCCESS: Koch Snowflake saved to {filename}")

    except Exception as e:
        print(f"ERROR: Failed to save SVG file. Details: {e}")
        print(f"Check if you have write permissions in {os.getcwd()}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = "Koch_Snowflake.svg"
    output_path = os.path.join(script_dir, output_filename)

    # --- MODIFICATION HERE ---
    # Increased depth to 7 (from 6) for even more detail
    create_koch_snowflake_svg(filename=output_path, size=1000, depth=7, stroke_color='none', fill_color='white')
    # Warning: Depth 7 will be VERY large and complex.
    # It generates 49,152 segments (3 * 4^7 / 3). This is 4 times the segments of depth 6.
    # Be prepared for very long generation times and a file that may struggle to open.
    # Future increases will result in astronomical file sizes.