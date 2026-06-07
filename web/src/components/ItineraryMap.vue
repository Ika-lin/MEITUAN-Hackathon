<script setup lang="ts">
import { computed } from 'vue'
import type { RoutePoint } from '../data/itineraryRoute'

const props = defineProps<{
  startPoint: RoutePoint
  endPoint: RoutePoint
  routePoints: RoutePoint[]
}>()

const mapBackgroundAsset = '/itinerary-map-bg.png'
const startMarkerAsset = '/Start Icon.svg'
const endMarkerAsset = '/MapPin.svg'

const hasRoute = computed(() => props.routePoints.length > 1)

const routePolylinePoints = computed(() => props.routePoints.map((point) => `${point.x},${point.y}`).join(' '))

const startMarkerStyle = computed(() => ({
  left: `${props.startPoint.x - 20}px`,
  top: `${props.startPoint.y - 20}px`,
}))

const endMarkerStyle = computed(() => ({
  left: `${props.endPoint.x - 20}px`,
  top: `${props.endPoint.y - 40}px`,
}))
</script>

<template>
  <div class="itinerary-map-wrapper" aria-hidden="true">
    <img :src="mapBackgroundAsset" alt="" class="itinerary-map-background" />

    <svg class="itinerary-map-route-layer" viewBox="0 0 417 551" preserveAspectRatio="none">
      <polyline v-if="hasRoute" :points="routePolylinePoints" class="itinerary-map-route-shadow" />
      <polyline v-if="hasRoute" :points="routePolylinePoints" class="itinerary-map-route" />
    </svg>

    <div class="itinerary-map-start-marker" :style="startMarkerStyle">
      <img :src="startMarkerAsset" alt="" class="itinerary-map-start-icon" />
    </div>

    <img :src="endMarkerAsset" alt="" class="itinerary-map-end-marker" :style="endMarkerStyle" />
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

.itinerary-map-route-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.itinerary-map-route-shadow {
  fill: none;
  stroke: rgba(95, 49, 83, 0.16);
  stroke-width: 18px;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.itinerary-map-route {
  fill: none;
  stroke: #5f3153;
  stroke-width: 9px;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.88;
}

.itinerary-map-start-marker {
  position: absolute;
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
  width: 40px;
  height: 40px;
  display: block;
}
</style>
