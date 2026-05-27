# 🛰️ GEO Satellite Dish Alignment Calculator

A lightweight, standalone Python tool that calculates the exact **Azimuth** and **Elevation** angles required to point a ground station dish at any Geostationary (GEO) satellite, such as **SES-8**.

## 🚀 Features
- **Live TLE Data:** Automatically pulls real-time orbital data from CelesTrak.
- **Dynamic Math Engine:** Utilizes the high-precision `skyfield` astronomy library.
- **Horizon Warning:** Alerts you if the target satellite is physically blocked by the Earth.

## 🛠️ How to Run Locally
1. Clone this repository or download the files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
