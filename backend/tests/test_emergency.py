from app.services.emergency import find_nearest_medic


def test_find_nearest_medic():
    staff = [
        {"id": "s1", "role": "security", "current_lat": 41.0, "current_lng": 2.0},
        {"id": "s2", "role": "medical", "current_lat": 41.001, "current_lng": 2.001},
        {"id": "s3", "role": "medical", "current_lat": 41.01, "current_lng": 2.01},
    ]
    medic = find_nearest_medic(staff, lat=41.0, lng=2.0)
    assert medic is not None
    assert medic["id"] == "s2"


def test_find_nearest_medic_no_medics():
    staff = [
        {"id": "s1", "role": "security", "current_lat": 41.0, "current_lng": 2.0},
    ]
    medic = find_nearest_medic(staff, lat=41.0, lng=2.0)
    assert medic is None
