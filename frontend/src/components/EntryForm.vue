<template>
  <form class="form-input">
    <input v-model="temperature" placeholder="Temperature" />
    <input
      type="file"
      accept="image/*"
      capture="user"
      @change="handleFileInput"
      ref="file"
    /><br /><br />
    <b>{{
      this.location.latitude
        ? `Lat:${this.location.latitude} | Long: ${this.location.longitude}`
        : "Getting location..."
    }}</b
    ><br /><br />
    Time of submission: <br />
    <b>{{ currTime ? getDateTime(currTime) : "" }}</b>
    <button @click="submit" class="btn-submit">Submit</button>
  </form>
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
    temperature: null,
    location: {},
    currTime: null,
    file: null
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
      console.log("Attempting to get location");
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(this.showPosition);
      } else {
        console.log("Geo Location not supported by browser");
      }
    },
    handleFileInput() {
      this.file = this.$refs.file.files[0];
    },
    // function that retrieves the position
    showPosition(position) {
      this.location = {
        longitude: position.coords.longitude,
        latitude: position.coords.latitude
      };
    },
    submit() {
      const method = "post";
      const url = "/api/entries";
      const headers = {
        Authorization: "Basic bmluZzpjc3k0YnFmNQ=="
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
    this.currTime = new Date(Date.now());
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
