import gpxpy
import gpxpy.gpx
import polyline

def generate_gpx_file(polyline_code):

    coordinates = polyline.decode(polyline_code)

    if not coordinates:
        return None

    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for lat, lon in coordinates:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))

    return gpx