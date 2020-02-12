<template>
<v-container fluid>
    <v-form>
      <v-row justify="center">
        <v-col cols="12">
          <v-row justify="center" class="pa-0 ma-0">
            <v-col cols="1" class="pa-0 ma-0">
              <v-icon>mdi-thermometer-lines</v-icon>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="2" xs="12">
              <v-slider
                v-model="temperature"
                min="34"
                max="44"
                thumb-label="always"
                step="0.1"
                vertical
                prepend-icon="mdi-minus"
                append-icon="mdi-plus"
              ></v-slider>
            </v-col>
          </v-row>
<!--          <v-row justify="center">-->
<!--            <v-col cols="4">-->
<!--              <v-text-field-->
<!--                v-model="temperature"-->
<!--                label="Enter temperature"-->
<!--                required-->
<!--              ></v-text-field>-->
<!--            </v-col>-->
<!--          </v-row>-->
<!--          <v-row justify="center">-->
<!--            <input type="file" accept="image/*" id="file-input" capture=""/>-->
<!--          </v-row>-->

<!-- The vuetify file input may not have Camera capture capability -->
          <v-row justify="center" class="pb-0 mb-0">
            <v-col cols="2" xs="10" class="pb-0 mb-0">
              <v-file-input
                accept="image/*"
                id="file-input"
                capture=""
                label="Capture"
                filled prepend-icon="mdi-camera"
                height="10"
                dense
              ></v-file-input>
            </v-col>
          </v-row>
          <v-row justify="center" class="pa-1">
            <b>{{ location }}</b>
          </v-row>
          <v-row justify="center" class="pa-1">
            <b>{{ currentTime }}</b>
          </v-row>
          <v-row justify="center">
            <v-btn
                color="success"
                class="mr-4"
                @click="submit"
              >
                Submit
            </v-btn>
          </v-row>
          <v-row justify="center">
            <canvas id="canvas" width="320" height="240"></canvas>
          </v-row>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axios from "axios";
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
  name: "entry-form",
  data: () => ({
    temperature: 37,
    file: null,
    locationMsg: "Getting location"
  }),
  methods: {
    getDateTime(time) {
      const hour = time.getHours();
      const minutes = time.getMinutes();
      const year = time.getFullYear();
      const date = time.getDate();
      const month = months[time.getMonth()];
      const day = days[time.getDay()];
      return `${day}, ${date} ${month} ${year} ${hour % 12}:${
        minutes < 10 ? "0" : ""
      }${minutes} ${minutes > 12 ? "PM" : "AM"}`;
    },
    getLocation() {
      const vm = this;
      console.log("Attempting to get location");

      const locError = function(error) {
        console.error("Failed to get location", error);
        vm.locationMsg = "Please enable location access...";
      }

      if (navigator.geolocation) {
        console.log("Accessing location");
        navigator.geolocation.getCurrentPosition(this.showPosition, locError);
      } else {
        console.log("Geo Location not supported by browser");
      }
    },
    // function that retrieves the position
    showPosition(position) {
      const geolocation = {
        longitude: position.coords.longitude,
        latitude: position.coords.latitude
      };
      console.log("Location", geolocation);
      this.locationMsg = "Lat: "+geolocation.latitude+ " | " + "Long: "+ geolocation.longitude;
    },
    submit() {
      const method = "post";
      const url = "/api/entries";
      const headers = {
        Authorization: "Basic bmluZzpjc3k0YnFmNQ==",
        "Content-Type": "multipart/form-data"
      };
      const data = new FormData();
      data.append("temperature", parseFloat(this.temperature));
      data.append("long", this.location.longitude);
      data.append("lat", this.location.latitude);
      data.append("file", this.file);

      axios({ method, url, headers, data });
    }
  },
  mounted() {
    this.getLocation();

    const getImage = (files) => {

      function draw() {
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');
        ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
      }

      function failed() {
        console.error("The provided file couldn't be loaded as an Image media");
      }

      console.log("Images", files);
      const file = files[0];
      var img = new Image();
      img.onload = draw;
      img.onerror = failed;
      img.src = URL.createObjectURL(file);
    };

    const fileInput = document.getElementById('file-input');
    fileInput.addEventListener('change', (e) => getImage(e.target.files));
  },
  computed: {
    location: function() {
      console.log("Getting computed location");
      return this.locationMsg;
    },
    currentTime: function() {
      // Date is not reactive, make it so later
      const time = new Date(Date.now());
      const hour = time.getHours();
      const minutes = time.getMinutes();
      const year = time.getFullYear();
      const date = time.getDate();
      const month = months[time.getMonth()];
      const day = days[time.getDay()];
      return `${day}, ${date} ${month} ${year} ${hour % 12}:${
        minutes < 10 ? "0" : ""
      }${minutes} ${minutes > 12 ? "PM" : "AM"}`;
    }
  }
};
</script>
<style scoped>
form > input {
  border: 1px solid grey;
  margin: 5px 0px;
}

.form-input {
  background-color: linen;
  width: 60%;
  display: block;
  margin: 10px auto;
  padding: 8px 20px;
}

.btn-submit {
  border: 1px solid darkgrey;
  margin-top: 10px;
  margin-bottom: 5px;
}
</style>
