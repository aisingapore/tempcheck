<template>
  <v-dialog v-model="dialog" width="100%">
    <template v-slot:activator="{ on }">
      <div class="entry-container" v-on="on">
        <span class="date-time">{{ getTime }}, {{ getDate }}</span
        ><br />
        <span class="display-1">{{ temperature.toFixed(1) }}</span>
        <span class="deg-c">&deg;C</span>
      </div>
    </template>
    <v-card>
      <v-card-title class="headline yellow lighten-4">
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

      <v-card-text> </v-card-text>
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
    }
  }
};
</script>
<style scoped>
.entry-container {
  background-color: linen;
  width: 185px;
  display: block;
  margin: 10px auto;
  padding: 8px 10px;
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
</style>
