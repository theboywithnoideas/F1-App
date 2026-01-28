import fastf1

def load_session(year, gp, session_type):
    """Loads an F1 session and its telemetry."""
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session

def get_race_telemetry(session, driver_code):
    """Gets the fastest lap telemetry for a specific driver."""
    lap = session.laps.pick_driver(driver_code).pick_fastest()
    telemetry = lap.get_telemetry()
    return telemetry
