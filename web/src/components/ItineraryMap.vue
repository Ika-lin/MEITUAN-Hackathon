<script setup lang="ts">
const mapBackgroundAsset = '/itinerary-map-bg.png'
const routeLineAsset = '/itinerary-route-line.svg'
const startMarkerAsset = '/Start Icon.svg'
const endMarkerAsset = '/MapPin.svg'
</script>

<template>
  <div class="itinerary-map-wrapper" aria-hidden="true">
    <img :src="mapBackgroundAsset" alt="" class="itinerary-map-background" />
    <img :src="routeLineAsset" alt="" class="itinerary-map-route" />

    <div class="itinerary-map-start-marker">
      <img :src="startMarkerAsset" alt="" class="itinerary-map-start-icon" />
    </div>

    <img :src="endMarkerAsset" alt="" class="itinerary-map-end-marker" />
  </div>
</template>

<style scoped>
.itinerary-map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #ece4e5;
}

.itinerary-map-background {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.itinerary-map-route {
  position: absolute;
  top: 204px;
  left: 94px;
  width: 276px;
  height: 149px;
  pointer-events: none;
}

.itinerary-map-start-marker {
  position: absolute;
  left: 108px;
  top: 387px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid #fff;
  border-radius: 50%;
  background: #000;
  box-shadow: 0 0 16px rgba(0, 0, 0, 0.25);
}

.itinerary-map-start-icon {
  width: 14px;
  height: 14px;
  display: block;
}

.itinerary-map-end-marker {
  position: absolute;
  left: 352px;
  top: 214px;
  width: 40px;
  height: 40px;
  display: block;
}
</style>
