from shapely.geometry import Point, Polygon


def point_in_polygon(lat: float, lng: float, polygon_coords: list[list[float]]) -> bool:
    """Check if a point (lat, lng) is inside a polygon.
    polygon_coords: list of [lng, lat] pairs (GeoJSON convention).
    """
    poly = Polygon(polygon_coords)
    point = Point(lng, lat)
    return poly.contains(point) or poly.boundary.contains(point)


def find_zone(lat: float, lng: float, zones: list[dict]) -> str | None:
    """Find which zone a point is in. Returns zone id or None."""
    for zone in zones:
        if point_in_polygon(lat, lng, zone["polygon"]):
            return zone["id"]
    return None
