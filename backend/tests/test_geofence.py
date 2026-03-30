from app.services.geofence import point_in_polygon, find_zone


def test_point_inside_polygon():
    polygon = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
    assert point_in_polygon(5.0, 5.0, polygon) is True


def test_point_outside_polygon():
    polygon = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
    assert point_in_polygon(15.0, 5.0, polygon) is False


def test_point_on_edge():
    polygon = [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
    assert point_in_polygon(0.0, 5.0, polygon) is True


def test_find_zone_for_point():
    zones = [
        {"id": "zone-a", "polygon": [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]},
        {"id": "zone-b", "polygon": [[20, 20], [30, 20], [30, 30], [20, 30], [20, 20]]},
    ]
    assert find_zone(5.0, 5.0, zones) == "zone-a"
    assert find_zone(25.0, 25.0, zones) == "zone-b"
    assert find_zone(15.0, 15.0, zones) is None
