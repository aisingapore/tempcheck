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
          <v-row justify="center" class="mt-n3">
            <v-col cols="10" xs="12">
              <v-slider
                v-model="temperature"
                min="35"
                max="39"
                thumb-label="always"
                step="0.1"
                prepend-icon="mdi-minus"
                append-icon="mdi-plus"
              ></v-slider>
            </v-col>
          </v-row>
          <!-- The vuetify file input may not have Camera capture capability -->
          <v-row class="mt-n3">
            <v-col>
              <vue-picture-input
                height="300"
                width="300"
                accept="image/*"
                size="10"
                ref="fileInput"
                capture="environment"
                @change="fileUpload"
                :custom-strings="{
                  tap: 'Tap to <br />upload image',
                  drag: 'Drag to upload image'
                }"
              />
            </v-col>
          </v-row>
          <v-row justify="center" class="pa-1">
            <b>{{ location }}</b>
          </v-row>
          <v-row justify="center" class="pa-1">
            <b>{{ currentTime }}</b>
          </v-row>
          <v-row justify="center" class="mt-4">
            <v-btn color="success" @click="submit">
              Submit
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axios from "axios";
import PhotoInput from "./PhotoInput";
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
  components: {
    "vue-picture-input": PhotoInput
  },
  data: () => ({
    temperature: 37,
    geolocation: {},
    file: null,
    locationMsg: "Getting location"
  }),
  methods: {
    fileUpload() {
      console.log("fileInput", this.$refs.fileInput);
      this.file = this.$refs.fileInput.file;
    },
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
      };

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
      this.geolocation = geolocation;
      this.locationMsg =
        "Lat: " +
        geolocation.latitude +
        " | " +
        "Long: " +
        geolocation.longitude;
    },
    async submit() {
      const method = "post";
      const url = "/api/entries";
      const headers = {
        Authorization: `Token ${localStorage.getItem("token")}`,
        "Content-Type": "multipart/form-data"
      };
      const data = new FormData();
      data.append("temperature", parseFloat(this.temperature));
      data.append("long", this.geolocation.longitude);
      data.append("lat", this.geolocation.latitude);
      data.append("file", this.file);

      const response = await axios({ method, url, headers, data });
      if (response.data) {
        this.$router.push("/history");
      }
    }
  },
  mounted() {
    this.getLocation();
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
