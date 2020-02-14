<template>
  <v-container fluid id="entry-form">
    <v-snackbar v-model="errorSnackbar.show" color="error" top>
      <span v-html="errorSnackbar.message" />
      <v-btn text @click="closeSnackbar">Close</v-btn>
    </v-snackbar>
    <v-form>
      <v-row justify="center">
        <v-col cols="12">
          <v-row justify="center" class="mt-4">
            <v-col cols="10" xs="12">
              <v-slider
                v-model="temperature"
                min="35"
                max="39"
                thumb-label="always"
                thumb-size="43"
                step="0.1"
              >
                <template v-slot:prepend>
                  <v-icon @click="decrement">
                    mdi-minus
                  </v-icon>
                </template>

                <template v-slot:append>
                  <v-icon @click="increment">
                    mdi-plus
                  </v-icon>
                </template>
              </v-slider>
            </v-col>
          </v-row>

          <v-row class="mt-n6 pb-2">
            <v-col>
              <vue-picture-input
                height="200"
                width="200"
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
    errorSnackbar: {
      show: false,
      message: null
    },
    file: null,
    locationMsg: "Getting location"
  }),
  methods: {
    closeSnackbar() {
      this.errorSnackbar = {
        show: false,
        message: null
      };
    },
    decrement() {
      this.temperature -= 0.1;
    },
    fileUpload() {
      // getting ready to resize file - read, write onto canvas, then save
      const width = 500;
      const reader = new FileReader();
      reader.readAsDataURL(this.$refs.fileInput.file);
      reader.onload = event => {
        const img = new Image();
        img.src = event.target.result;
        img.onload = () => {
          const canvas = document.createElement("canvas");
          canvas.width = width;
          canvas.height = parseInt((img.height / img.width) * width);
          const ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          ctx.canvas.toBlob(
            blob => {
              this.file = new File([blob], this.$refs.fileInput.file.name, {
                type: "image/png",
                lastModified: Date.now()
              });
            },
            "image/png",
            0.8
          ); // trial for file size/quality balance
        };
      };
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
    increment() {
      this.temperature += 0.1;
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
      if (!this.valid()) {
        return;
      }
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

      try {
        const response = await axios({ method, url, headers, data });
        console.log(response.data);
        this.$router.push("/history");
      } catch (error) {
        const errors = error.response.data;
        this.errorSnackbar = {
          show: true,
          message:
            "Errors from server: <br />" +
            Object.keys(errors)
              .map(k => `${k}: ${errors[k]}`)
              .join("<br />")
        };
      }
    },
    valid() {
      const errors = [];

      if (!this.file) {
        errors.push("Please upload a valid image.");
      }

      if (!this.geolocation.longitude || !this.geolocation.latitude) {
        errors.push("Please provide your location through location services.");
      }

      if (isNaN(this.temperature)) {
        errors.push("Please provide a valid temperature.");
      }

      if (errors.length === 0) {
        return true;
      }

      this.errorSnackbar = {
        message: errors.join("<br />"),
        show: true
      };
      return false;
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
<style>
#entry-form .v-slider__thumb-label {
  font-size: 1em !important;
  font-weight: bold;
}
</style>
