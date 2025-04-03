import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

// Fix for default marker icons in Leaflet with webpack
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend);

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapVisualization = ({ data }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [countryStats, setCountryStats] = useState({});
  const [mapMode, setMapMode] = useState('heatmap'); // 'heatmap' or 'markers'

  // Process data to get country statistics
  useEffect(() => {
    if (data && data.length > 0) {
      const stats = {};
      
      data.forEach(location => {
        const country = location.location.split(',').pop().trim();
        if (!stats[country]) {
          stats[country] = {
            userCount: 0,
            locations: []
          };
        }
        
        stats[country].userCount += location.userCount;
        stats[country].locations.push(location);
      });
      
      setCountryStats(stats);
    }
  }, [data]);

  useEffect(() => {
    // Initialize map if it doesn't exist yet
    if (!mapInstanceRef.current && mapRef.current) {
      // Create map centered on Turkey
      mapInstanceRef.current = L.map(mapRef.current).setView([39.0, 35.0], 6);

      // Add OpenStreetMap tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(mapInstanceRef.current);
    }

    // Add markers if map exists and data is available
    if (mapInstanceRef.current && data && data.length > 0) {
      // Clear existing markers
      mapInstanceRef.current.eachLayer(layer => {
        if (layer instanceof L.Marker || layer instanceof L.Circle) {
          mapInstanceRef.current.removeLayer(layer);
        }
      });

      // Filter data if a country is selected
      const locationsToShow = selectedCountry 
        ? countryStats[selectedCountry]?.locations || []
        : data;

      // Add new markers based on map mode
      if (mapMode === 'heatmap') {
        // Create heat map style visualization with circles
        locationsToShow.forEach(location => {
          if (location.latitude && location.longitude) {
            // Create circle marker with size based on user count
            const radius = Math.sqrt(location.userCount) * 5000;
            
            const circle = L.circle([location.latitude, location.longitude], {
              color: '#1DA1F2',
              fillColor: '#1DA1F2',
              fillOpacity: 0.5,
              radius: radius
            }).addTo(mapInstanceRef.current);

            // Add popup with location info
            circle.bindPopup(`
              <strong>${location.location}</strong><br>
              Katılımcı Sayısı: ${location.userCount}
            `);
          }
        });
      } else {
        // Create standard markers with clustering
        locationsToShow.forEach(location => {
          if (location.latitude && location.longitude) {
            const marker = L.marker([location.latitude, location.longitude])
              .addTo(mapInstanceRef.current);
              
            // Add popup with location info
            marker.bindPopup(`
              <strong>${location.location}</strong><br>
              Katılımcı Sayısı: ${location.userCount}
            `);
          }
        });
      }

      // Adjust map view to fit all markers if there are any
      if (locationsToShow.length > 0) {
        const bounds = [];
        locationsToShow.forEach(location => {
          if (location.latitude && location.longitude) {
            bounds.push([location.latitude, location.longitude]);
          }
        });
        
        if (bounds.length > 0) {
          mapInstanceRef.current.fitBounds(bounds);
        }
      }
    }

    // Cleanup function
    return () => {
      if (mapInstanceRef.current) {
        // We don't destroy the map here to prevent re-creation on every render
        // Just clean up markers if needed
      }
    };
  }, [data, selectedCountry, mapMode, countryStats]);

  // Cleanup map on component unmount
  useEffect(() => {
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Prepare data for country distribution pie chart
  const prepareCountryChartData = () => {
    const labels = Object.keys(countryStats);
    const values = labels.map(country => countryStats[country].userCount);
    
    return {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: [
            'rgba(75, 192, 192, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)',
            'rgba(255, 99, 132, 0.6)',
            'rgba(255, 206, 86, 0.6)',
          ],
          borderColor: [
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(255, 159, 64)',
            'rgb(255, 99, 132)',
            'rgb(255, 206, 86)',
          ],
          borderWidth: 1,
        },
      ],
    };
  };

  if (!data || data.length === 0) {
    return <div className="no-data">Konum verisi bulunamadı</div>;
  }

  return (
    <div className="map-visualization">
      <h3>Katılımcıların Coğrafi Dağılımı</h3>
      
      <div className="map-controls">
        <div className="map-mode-selector">
          <label>
            <input 
              type="radio" 
              name="mapMode" 
              value="heatmap" 
              checked={mapMode === 'heatmap'} 
              onChange={() => setMapMode('heatmap')} 
            />
            Isı Haritası
          </label>
          <label>
            <input 
              type="radio" 
              name="mapMode" 
              value="markers" 
              checked={mapMode === 'markers'} 
              onChange={() => setMapMode('markers')} 
            />
            İşaretçiler
          </label>
        </div>
        
        <div className="country-filter">
          <label htmlFor="country-select">Ülke Filtresi:</label>
          <select 
            id="country-select"
            value={selectedCountry || ''}
            onChange={(e) => setSelectedCountry(e.target.value || null)}
          >
            <option value="">Tüm Ülkeler</option>
            {Object.keys(countryStats).map(country => (
              <option key={country} value={country}>
                {country} ({countryStats[country].userCount} katılımcı)
              </option>
            ))}
          </select>
        </div>
      </div>
      
      <div className="map-container" ref={mapRef} style={{ height: '500px', width: '100%' }}></div>
      
      <div className="map-stats">
        <div className="country-distribution">
          <h4>Ülkelere Göre Dağılım</h4>
          <div className="chart-container" style={{ height: '300px', width: '300px', margin: '0 auto' }}>
            <Pie data={prepareCountryChartData()} />
          </div>
        </div>
        
        <div className="location-stats">
          <h4>En Çok Katılımcı Olan Konumlar</h4>
          <ul>
            {data
              .sort((a, b) => b.userCount - a.userCount)
              .slice(0, 10)
              .map((location, index) => (
                <li key={index}>
                  <strong>{location.location}</strong>: {location.userCount} katılımcı
                </li>
              ))}
          </ul>
        </div>
      </div>
      
      <div className="map-legend">
        <h4>Harita Açıklaması</h4>
        <p>
          Bu harita, hashtag'i kullanan katılımcıların coğrafi dağılımını göstermektedir.
          {mapMode === 'heatmap' ? (
            <span>
              Daireler, o konumdaki katılımcı sayısını temsil eder - daire ne kadar büyükse, 
              o kadar çok katılımcı var demektir.
            </span>
          ) : (
            <span>
              Her işaretçi, katılımcıların bulunduğu bir konumu temsil eder.
            </span>
          )}
        </p>
        <p>
          {mapMode === 'heatmap' ? 'Dairelere' : 'İşaretçilere'} tıklayarak o konumdaki katılımcı sayısını görebilirsiniz.
        </p>
        <p>
          Ülke filtresini kullanarak belirli bir ülkedeki dağılımı daha detaylı inceleyebilirsiniz.
        </p>
      </div>
    </div>
  );
};

export default MapVisualization;
