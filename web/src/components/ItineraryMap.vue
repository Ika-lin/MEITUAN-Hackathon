<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const mapContainer = ref<HTMLElement | null>(null)
const map = ref<L.Map | null>(null)

const routePoints: [number, number][] = [
  [31.1932, 121.4383],
  [31.1939, 121.4389],
  [31.1947, 121.4401],
  [31.1952, 121.4414],
  [31.1963, 121.4417],
  [31.1975, 121.4425],
]

const startPoint = routePoints[0]
const endPoint = routePoints[routePoints.length - 1]

onMounted(() => {
  if (!mapContainer.value) return

  const leafletMap = L.map(mapContainer.value, {
    zoomControl: false,
    attributionControl: false,
    dragging: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    keyboard: false,
    touchZoom: false,
  }).setView([31.1951, 121.4403], 15)

  map.value = leafletMap

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    className: 'itinerary-map-tile'
  }).addTo(leafletMap)

  const startIcon = L.divIcon({
    className: 'itinerary-marker-shell',
    html: `
      <div style="
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 3px solid #ffffff;
        background: #000000;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 16px rgba(0, 0, 0, 0.25);
      ">
        <div style="
          width: 0;
          height: 0;
          border-left: 6px solid transparent;
          border-right: 6px solid transparent;
          border-bottom: 12px solid #ffffff;
          transform: translateY(-1px);
        "></div>
      </div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 20],
  })

  const endIcon = L.divIcon({
    className: 'itinerary-marker-shell',
    html: `
      <div style="
        position: relative;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <div style="
          width: 26px;
          height: 26px;
          border: 3px solid #111111;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.92);
          box-shadow: 0 0 16px rgba(0, 0, 0, 0.16);
        "></div>
        <div style="
          position: absolute;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #111111;
        "></div>
      </div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 20],
  })

  L.polyline(routePoints, {
    color: 'rgba(255, 255, 255, 0.9)',
    weight: 8,
    opacity: 1,
    lineJoin: 'round',
  }).addTo(leafletMap)

  L.polyline(routePoints, {
    color: '#111111',
    weight: 4,
    opacity: 0.95,
    lineJoin: 'round'
  }).addTo(leafletMap)

  L.marker(startPoint, { icon: startIcon, interactive: false }).addTo(leafletMap)
  L.marker(endPoint, { icon: endIcon, interactive: false }).addTo(leafletMap)

  leafletMap.fitBounds(L.latLngBounds(routePoints).pad(0.18), {
    padding: [24, 24],
  })
})

onBeforeUnmount(() => {
  map.value?.remove()
  map.value = null
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
  width: 100%;
  height: 100%;
  margin: 0;
  border-radius: inherit;
  overflow: hidden;
  background: #ece4e5;
}

.itinerary-map-container {
  width: 100%;
  height: 100%;
  background: #ece4e5;
}

:deep(.leaflet-container) {
  font-family: "SF Pro Rounded", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: #ece4e5 !important;
}

:deep(.itinerary-map-tile) {
  filter: saturate(0.86) brightness(1.04) contrast(0.96);
}

:deep(.leaflet-control-container),
:deep(.leaflet-top),
:deep(.leaflet-bottom) {
  display: none;
}
</style>
