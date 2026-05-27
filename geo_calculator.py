import sys
import requests
from skyfield.api import load, wgs84, EarthSatellite
from datetime import datetime, timezone

def fetch_tle(norad_id):
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        tle_lines = response.text.strip().split('\n')
        if len(tle_lines) >= 3:
            return tle_lines[0].strip(), tle_lines[1].strip(), tle_lines[2].strip()
        else:
            print("❌ Error: Received invalid data format from CelesTrak.")
            sys.exit(1)
    except requests.RequestException as e:
        print(f"❌ Network Error fetching TLE data: {e}")
        sys.exit(1)

def main():
    print("=============================================")
    print("🛰️  GEO SATELLITE DISH ALIGNMENT CALCULATOR  🛰️")
    print("=============================================\n")

    norad_input = input("Enter NORAD ID [Press Enter for SES-8 (39460)]: ").strip()
    norad_id = norad_input if norad_input else "39460"
    
    name, line1, line2 = fetch_tle(norad_id)
    ts = load.timescale()
    satellite = EarthSatellite(line1, line2, name, ts)

    print(f"✅ Successfully loaded tracking engine for: {name}\n")

    print("Step 2: Enter Your Ground Station Coordinates")
    print("---------------------------------------------")
    try:
        user_lat = float(input("🌐 Enter your Latitude  (e.g., 28.61): "))
        user_lon = float(input("🌐 Enter your Longitude (e.g., 77.20): "))
    except ValueError:
        print("❌ Invalid input!")
        sys.exit(1)

    ground_station = wgs84.latlon(user_lat, user_lon)
    now = datetime.now(timezone.utc)
    t = ts.from_datetime(now)
    
    difference = satellite - ground_station
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    print("\n=============================================")
    print("🎯  CALCULATION RESULTS (TARGET ACQUIRED)   🎯")
    print("=============================================")
    print(f"📡 Target Satellite    : {name}")
    print(f"📏 Range to Target     : {distance.km:,.2f} km")
    print("---------------------------------------------")
    print(f"🧭 AZIMUTH (Compass)   : {az.degrees:.2f}°")
    print(f"📐 ELEVATION (Tilt)    : {alt.degrees:.2f}°")
    if alt.degrees < 0:
        print("\n⚠️  WARNING: The satellite is BELOW your local horizon.")
    print("=============================================\n")

if __name__ == "__main__":
    main()
