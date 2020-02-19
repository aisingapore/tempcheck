<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <div class="entry-container" v-on="on">
        <span class="date-time">{{ getTime }}, {{ getDate }}</span
        ><br />
        <span class="display-1">{{ temperature.toFixed(1) }}</span>
        <span class="deg-c">&deg;C</span>
      </div>
    </template>
    <v-card ma-0>
      <v-card-title class="headline card-title lighten-4">
        <v-container>
          <v-row class="mt-n6 mb-n3">
            <v-col cols="12" class="text-right body-2 grey--text">
              Your temperature at {{ getTime }},<br />
              {{ getDate }}:
            </v-col>
          </v-row>
          <v-row class="text-right mb-n3">
            <v-col cols="12" class="text-right grey--text text--darken-2">
              <span class="display-2">{{ temperature.toFixed(1) }}</span>
              <span class="body-2">&deg;C</span>
            </v-col>
          </v-row>
        </v-container>
      </v-card-title>
      <div v-if="dialog">
        <GmapMap
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
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
const months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec"
];

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export default {
  name: "entry",
  data() {
    return {
      dialog: false
    };
  },
  computed: {
    getTime() {
      const hour = this.timeTaken.getHours();
      const minutes = this.timeTaken.getMinutes();
      return `${hour % 12}:${minutes < 10 ? "0" : ""}${minutes} ${
        hour > 12 ? "PM" : "AM"
      }`;
    },
    getDate() {
      const year = this.timeTaken.getFullYear();
      const date = this.timeTaken.getDate();
      const month = months[this.timeTaken.getMonth()];
      const day = days[this.timeTaken.getDay()];
      return `${day}, ${date} ${month} ${year}`;
    }
  },
  props: {
    temperature: {
      type: Number,
      default: 37
    },
    timeTaken: {
      type: Date,
      default: () => new Date("12-12-2019 11:22:33Z")
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
</style>
