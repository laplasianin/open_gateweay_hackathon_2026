from app.services.simulation import interpolate_position


def test_interpolate_position_at_start():
    waypoints = [
        {"lat": 41.0, "lng": 2.0, "offset": 0},
        {"lat": 41.1, "lng": 2.1, "offset": 10},
    ]
    lat, lng = interpolate_position(waypoints, elapsed=0)
    assert lat == 41.0
    assert lng == 2.0


def test_interpolate_position_midway():
    waypoints = [
        {"lat": 41.0, "lng": 2.0, "offset": 0},
        {"lat": 42.0, "lng": 3.0, "offset": 10},
    ]
    lat, lng = interpolate_position(waypoints, elapsed=5)
    assert abs(lat - 41.5) < 0.01
    assert abs(lng - 2.5) < 0.01


def test_interpolate_position_past_end():
    waypoints = [
        {"lat": 41.0, "lng": 2.0, "offset": 0},
        {"lat": 42.0, "lng": 3.0, "offset": 10},
    ]
    lat, lng = interpolate_position(waypoints, elapsed=20)
    assert lat == 42.0
    assert lng == 3.0
