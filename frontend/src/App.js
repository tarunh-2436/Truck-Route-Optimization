import React, { useState } from "react";
import axios from "axios";
import MapComponent from "./components/MapComponent";

function App() {
  const [addresses, setAddresses] = useState("");
  const [optimizedRoute, setOptimizedRoute] = useState([]);

  const handleOptimize = async () => {
    const addressList = addresses.split("\n").map(addr => addr.trim());
    const response = await axios.post("http://127.0.0.1:5000", { addresses: addressList });
    setOptimizedRoute(response.data.optimized_route);
  };

  return (
    <div>
      <h1>Delivery Route Optimizer</h1>
      <textarea
        rows="5"
        cols="50"
        placeholder="Enter addresses, one per line"
        value={addresses}
        onChange={(e) => setAddresses(e.target.value)}
      />
      <br />
      <button onClick={handleOptimize}>Optimize Route</button>
      {optimizedRoute.length > 0 && (
        <>
          <h2>Optimized Route:</h2>
          <ol>
            {optimizedRoute.map((addr, index) => (
              <li key={index}>{addr}</li>
            ))}
          </ol>
          <MapComponent locations={optimizedRoute} />
        </>
      )}
    </div>
  );
}

export default App;
