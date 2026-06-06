<script setup lang="ts">
import { onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const mapContainer = ref<HTMLElement | null>(null)
const map = ref<L.Map | null>(null)

// Define locations (Shanghai coordinates)
const locations = [
  { 
    name: '武康路 376 号附近',
    lat: 31.1932,
    lng: 121.4383,
    type: 'start'
  },
  { 
    name: 'FILM电影时光书店',
    lat: 31.1945,
    lng: 121.4395,
    type: 'activity'
  },
  { 
    name: 'RAC BAR (安福路店)',
    lat: 31.1955,
    lng: 121.4405,
    type: 'activity'
  },
  { 
    name: '一面春风 (吴兴路总店)',
    lat: 31.1965,
    lng: 121.4415,
    type: 'activity'
  },
  { 
    name: '上海图书馆地铁站',
    lat: 31.1975,
    lng: 121.4425,
    type: 'end'
  }
]

onMounted(() => {
  if (!mapContainer.value) return

  // Initialize map centered on Shanghai
  const leafletMap = L.map(mapContainer.value).setView([31.195, 121.44], 15)
  map.value = leafletMap

  // Add tile layer (OpenStreetMap)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
    className: 'itinerary-map-tile'
  }).addTo(leafletMap)

  // Add markers for each location
  const markers: L.Marker[] = []
  locations.forEach((location, index) => {
    let iconColor = '#666666'
    let iconNumber = ''

    if (location.type === 'start') {
      iconColor = '#000000'
      iconNumber = 'S'
    } else if (location.type === 'end') {
      iconColor = '#d9534f'
      iconNumber = 'E'
    } else if (location.type === 'activity') {
      iconColor = '#461c3a'
      iconNumber = String(index)
    }

    // Create custom marker HTML
    const markerHtml = `
      <div style="
        background: ${iconColor};
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      ">
        ${iconNumber}
      </div>
    `

    const customIcon = L.divIcon({
      html: markerHtml,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -16],
      className: 'itinerary-marker'
    })

    const marker = L.marker([location.lat, location.lng], { icon: customIcon })
      .bindPopup(location.name)
      .addTo(leafletMap)

    marker.on('click', () => {
      marker.openPopup()
    })

    markers.push(marker)
  })

  // Draw route line between locations
  const routePoints = locations.map(loc => [loc.lat, loc.lng] as [number, number])
  L.polyline(routePoints, {
    color: '#4a7db8',
    weight: 3,
    opacity: 0.7,
    dashArray: '5, 5',
    lineJoin: 'round'
  }).addTo(leafletMap)

  // Fit map bounds to show all markers
  if (markers.length > 0) {
    const group = new L.FeatureGroup(markers)
    leafletMap.fitBounds(group.getBounds().pad(0.1), {
      padding: [50, 50]
    })
  }
})
</script>

<template>
  <div class="itinerary-map-wrapper">
    <div ref="mapContainer" class="itinerary-map-container"></div>
  </div>
</template>

<style scoped>
.itinerary-map-wrapper {
  position: relative;
  z-index: 5;
  width: 100%;
  height: 280px;
  margin: 16px 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.itinerary-map-container {
  width: 100%;
  height: 100%;
  background: #f5f5f5;
}

:deep(.leaflet-container) {
  font-family: "SF Pro Rounded", "PingFang SC", "Microsoft YaHei", sans-serif;
}

:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

:deep(.leaflet-popup-content) {
  font-size: 13px;
  color: #2a2a2a;
  margin: 8px 0;
}

:deep(.leaflet-popup-tip) {
  background: white;
}

:deep(.itinerary-map-tile) {
  filter: saturate(1.1) brightness(1.05);
}
</style>
