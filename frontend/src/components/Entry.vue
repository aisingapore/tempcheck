<template>
  <div class="entry-container">
    <span class="date-time">{{ getTime }}, {{ getDate }}</span
    ><br />
    Temperature: <b>{{ temperature.toFixed(1) }}</b
    >&deg;C
  </div>
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
  name: "entry-form",
  computed: {
    getTime() {
      const hour = this.timeTaken.getHours();
      const minutes = this.timeTaken.getMinutes();
      return `${hour % 12}:${minutes < 10 ? "0" : ""}${minutes} ${minutes > 12 ? "PM" : "AM"}`;
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
    }
  }
};
</script>
<style scoped>
.entry-container {
  background-color: linen;
  width: 40%;
  display: block;
  margin: 10px auto;
  padding: 8px 20px;
}

.date-time {
  font-size: 12px;
  color: lightslategrey;
}
</style>
