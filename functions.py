from shapely.geometry import LineString, MultiLineString, Point, GeometryCollection
from shapely.ops import split

# Function to extract coordinates from LineString and MultiLineString
def extract_coords(geometry):
    if isinstance(geometry, LineString):
        return [(point[1], point[0]) for point in geometry.coords]  # Convert (x, y) to (lat, lon)
    elif isinstance(geometry, MultiLineString):
        return [[(point[1], point[0]) for point in line.coords] for line in geometry.geoms]  # Convert for each line
    return []


# Find road intersections
def find_intersections(roads):
    """Finds intersection points of road segments."""
    intersections = []
    
    # Iterate through all pairs of roads
    for i, road1 in enumerate(roads.geometry):
        for j, road2 in enumerate(roads.geometry):
            if i >= j:
                continue  # Avoid duplicate comparisons and self-intersections
            
            # Find the intersection between the two geometries
            inter = road1.intersection(road2)
            
            # If there is no intersection, skip
            if inter.is_empty:
                continue
            
            # Handle intersections
            if isinstance(inter, Point):  # Single Point intersection
                intersections.append(inter)
            elif isinstance(inter, GeometryCollection):  # Multiple intersections
                for geom in inter.geoms:
                    if isinstance(geom, Point):  # Only keep Points
                        intersections.append(geom)
    
    # Remove duplicate intersection points by converting to a set and back to a list
    unique_intersections = list({(point.x, point.y): point for point in intersections}.values())
    
    return unique_intersections


# Split roads into segments at intersections
def split_road_segments(road, intersection_points):
    """Splits a road into segments at given intersection points."""
    segments = [road]
    for point in intersection_points:
        print("Entered Loop")
        new_segments = []
        for segment in segments:
            if segment.intersects(point):
                split_segments = split(segment, point)
                if isinstance(split_segments, GeometryCollection):
                    # Extract individual geometries from GeometryCollection
                    new_segments.extend([geom for geom in split_segments.geoms])
                else:
                    new_segments.append(split_segments)
            else:
                new_segments.append(segment)
        segments = new_segments
    return segments



