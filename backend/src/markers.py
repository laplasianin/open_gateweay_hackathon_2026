"""Markers management module."""
from typing import List
from src.models import Marker

# Base markers coordinates
BASE_MARKERS = [
    {"lat": 41.37372, "lng": 2.14881, "label": "Main Stage", "role": "stage"},
    {"lat": 41.37306, "lng": 2.14941, "label": "Second Stage", "role": "stage"},
    {"lat": 41.37207, "lng": 2.15009, "label": "Third Stage", "role": "stage"},
    {"lat": 41.384, "lng": 2.172, "label": "Food & Drinks", "role": "food"},
    {"lat": 41.3858, "lng": 2.171, "label": "Info Point", "role": "info"},
    {"lat": 41.385, "lng": 2.169, "label": "Backstage HQ", "role": "support"},
    {"lat": 41.3835, "lng": 2.1705, "label": "Main Entrance", "role": "entry"},
]

# Simulated marker path - sequential coordinates
SIMULATED_MARKER_PATH = [
    {"lat": 41.37305, "lng": 2.15077},
    {"lat": 41.37509, "lng": 2.15117},
    {"lat": 41.37437, "lng": 2.14822},
    {"lat": 41.37397, "lng": 2.14874},
]

# Current markers (will be updated)
current_markers = [Marker(**m) for m in BASE_MARKERS]

# Path index for sequential updates
_path_index = 0


def get_current_markers() -> List[Marker]:
    """Get current markers."""
    return current_markers


def update_markers_with_variation() -> List[Marker]:
    """
    Update first marker with next coordinate from simulated path.
    Cycles through SIMULATED_MARKER_PATH sequentially.
    """
    global current_markers, _path_index

    # Get next coordinate from path
    path_coord = SIMULATED_MARKER_PATH[_path_index]

    # Update first marker with path coordinates
    updated = []
    for i, marker in enumerate(current_markers):
        if i == 0:
            # Update first marker with path coordinates
            new_marker = Marker(
                lat=path_coord["lat"],
                lng=path_coord["lng"],
                label=marker.label,
                role=marker.role,
            )
        else:
            # Keep other markers unchanged
            new_marker = marker
        updated.append(new_marker)

    # Move to next path coordinate
    _path_index = (_path_index + 1) % len(SIMULATED_MARKER_PATH)

    current_markers = updated
    return current_markers


def reset_markers() -> List[Marker]:
    """Reset markers to base coordinates."""
    global current_markers
    current_markers = [Marker(**m) for m in BASE_MARKERS]
    return current_markers

