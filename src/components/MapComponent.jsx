import React from "react";
import { Map, Marker } from "react-map-gl";

const MapComponent = ({ locations }) => {
  const MAPMYINDIA_API_KEY = "YOUR_MAPMYINDIA_API_KEY";

  return (
    <Map
      initialViewState={{
        latitude: 28.7041, // Default to New Delhi
        longitude: 77.1025,
        zoom: 10
      }}
      style={{ width: "100%", height: "400px" }}
      mapStyle="https://maps.mapmyindia.com/map_styles/default"
      mapboxAccessToken={MAPMYINDIA_API_KEY}
    >
      {locations.map((location, index) => (
        <Marker key={index} latitude={location.latitude} longitude={location.longitude}>
          <span>📍</span>
        </Marker>
      ))}
    </Map>
  );
};

export default MapComponent;
