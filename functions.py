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
    for i, road1 in roads.iterrows():
        for j, road2 in roads.iterrows():
            if i >= j:
                continue  # Avoid self-comparison and duplicates
            inter = road1.geometry.intersection(road2.geometry)
            if inter.is_empty:
                continue
            # Handle both Point and GeometryCollection cases
            if isinstance(inter, Point):
                intersections.append(inter)
            elif isinstance(inter, GeometryCollection):
                for geom in inter.geoms:
                    if isinstance(geom, Point):
                        intersections.append(geom)
    return intersections

# Split roads into segments at intersections
def split_road_segments(road, intersection_points):
    """Splits a road into segments at given intersection points."""
    segments = [road]
    for point in intersection_points:
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



