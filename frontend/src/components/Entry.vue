<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <div class="entry-container" v-on="on">
        <span class="date-time">{{ timeTaken }}</span
        ><br />
        <span v-bind:class="{ twarn: parseFloat(temperature) >= 38 }">
          <span class="display-1">{{ temperature }}</span>
          <span v-if="!isNaN(temperature)" class="deg-c">&deg;C</span>
        </span>
      </div>
    </template>
    <v-card ma-0>
      <v-card-title class="headline card-title lighten-4">
        <v-container>
          <v-row class="mt-n6 mb-n3">
            <v-col cols="12" class="text-right body-2 grey--text">
              Your temperature at {{ timeTaken }}
            </v-col>
          </v-row>
          <v-row class="text-right mb-n3">
            <v-col cols="12" class="text-right grey--text text--darken-2">
              <span v-bind:class="{ twarn: parseFloat(temperature) >= 38 }">
                <span class="display-2">{{ temperature }}</span>
                <span v-if="!isNaN(temperature)" class="body-2">&deg;C</span>
              </span>
            </v-col>
          </v-row>
        </v-container>
      </v-card-title>
      <div v-if="dialog">
        <GmapMap
          v-if="map === 'gmap'"
          :center="{
            lat: parseFloat(location.lat),
            lng: parseFloat(location.long)
          }"
          :zoom="15"
          map-type-id="roadmap"
          style="width: 100%; height: 40%"
          :options="{
            zoomControl: false,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            rotateControl: false,
            fullscreenControl: false,
            disableDefaultUi: false,
            draggable: false,
            disableDefaultUI: true
          }"
        >
          <GmapCircle
            :center="{
              lat: parseFloat(location.lat),
              lng: parseFloat(location.long)
            }"
            :options="{
              fillColor: 'pink',
              strokeColor: 'pink'
            }"
            :clickable="false"
            :draggable="false"
            :radius="500"
          />
        </GmapMap>
        <OneMap v-if="map == 'onemap'" :location="location" />
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
import OneMap from "@/components/OneMap";

export default {
  name: "entry",
  components: {
    OneMap
  },
  data() {
    return {
      dialog: false,
      map: "onemap"
    };
  },
  props: {
    temperature: {
      type: String,
      default: "37"
    },
    timeTaken: {
      type: String,
      default: () => new Date()
    },
    location: {
      type: Object,
      default: () => ({
        lat: 0,
        long: 0
      })
    }
  }
};
</script>
<style scoped>
.entry-container {
  background-color: #f5faff;
  border: 1.5px solid #1976d2;
  width: 185px;
  display: block;
  margin: 10px auto;
  padding: 8px 10px;
  box-shadow: 1px 5px 2px -2px rgba(0, 0, 0, 0.3),
    0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12);
  border-radius: 4px;
}

.date-time {
  font-size: 12px;
  color: lightslategrey;
}

.deg-c {
  display: inline-block;
  margin-top: 3px;
  margin-left: 2px;
  vertical-align: top;
}

.card-title {
  background-color: #dbedff;
}

.twarn {
  color: red;
}
</style>
