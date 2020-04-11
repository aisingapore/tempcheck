<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <h2>{{ name }}</h2>
        <h1>History</h1>
      </v-col>
    </v-row>
    <v-row class="mt-n3">
      <v-col>
        <v-btn color="primary" @click="goToNewEntry()">New Entry</v-btn>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="4" class="entry-list">
        <entry
          v-for="item in todayList"
          :key="item.date"
          :temperature="item.temperature"
          :timeTaken="item.date"
          :location="item.location"
        />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="4" class="entry-list">
        <entry
          v-for="item in displayList.slice(0, numRecordsToShow)"
          :key="item.date"
          :temperature="item.temperature"
          :timeTaken="item.date"
          :location="item.location"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn
          v-if="numRecordsToShow < displayList.length"
          text
          outlined
          color="green"
          class="mr-4 white--text"
          @click="
            numRecordsToShow = Math.min(
              displayList.length,
              numRecordsToShow + 4
            )
          "
          >Load {{ Math.min(4, displayList.length - numRecordsToShow) }} more
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn
          text
          outlined
          color="indigo"
          class="mr-4 white--text"
          @click="signOut"
          >Log Out
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import moment from "moment-timezone";
import Entry from "@/components/Entry";
export default {
  name: "hello",
  components: {
    entry: Entry
  },
  data() {
    return {
      name: localStorage.getItem("email"),
      displayList: [],
      todayList: [],
      numRecordsToShow: 4
    };
  },
  methods: {
    async getEntries() {
      const url = "/api/entries";
      const headers = {
        Authorization: `Token ${localStorage.getItem("token")}`
      };
      try {
        const response = await axios.get(url, { headers });
        const entries = response.data;
        this.createDisplayList(entries);
      } catch (err) {
        console.log("Error:", err);
      }
    },
    goToNewEntry() {
      this.$router.push("/new");
    },
    signOut() {
      localStorage.removeItem("token");
      localStorage.removeItem("tokenExpiry");
      this.$router.push("/");
    },
    createDisplayList(entries) {
      if (entries) {
        const userTz = moment.tz.guess();
        const current = moment().tz(userTz);
        const firstEntry = entries[entries.length - 1];
        const firstEntryDate = moment(firstEntry.date_created).tz(userTz);
        const daysSince = current.diff(firstEntryDate, "days");

        const displays = {};
        for (let i = 1; i <= daysSince; i++) {
          const displayDate = current.subtract(1, "days").tz(userTz);
          const entryDate = displayDate.format("ddd DD MMM YYYY");
          const displayAM = {
            date: "AM, " + entryDate,
            location: { lat: 1.3521, long: 103.8198 },
            temperature: "None"
          };
          const displayPM = {
            date: "PM, " + entryDate,
            location: { lat: 1.3521, long: 103.8198 },
            temperature: "None"
          };
          const displayKey = displayDate.format("D M YY");
          displays[displayKey + "AM"] = displayAM;
          displays[displayKey + "PM"] = displayPM;
        }

        const now = moment().tz(userTz);
        for (const entry of entries) {
          const enDate = moment(entry.date_created).tz(userTz);
          const entryKey = enDate.format("D M YY");
          const suffix = enDate.hour() < 12 ? "AM" : "PM";

          const displayEntry = {
            date: enDate.format("H:mm A, ddd DD MMM YYYY"),
            location: { lat: entry.lat, long: entry.long },
            temperature: parseFloat(entry.temperature).toFixed(1)
          };

          const currentEntryDay = moment({
            year: enDate.year(),
            month: enDate.month(),
            day: enDate.date()
          });
          if (now.diff(currentEntryDay, "days") === 0) {
            // push only latest entry
            if (enDate.hour() < 12 && this.todayList.length === 0) {
              this.todayList.push(displayEntry);
            }

            if (enDate.hour() >= 12) {
              if (this.todayList.length === 0) {
                const missingAM = {
                  date: "AM, " + currentEntryDay.format("ddd DD MMM YYYY"),
                  location: { lat: 1.3521, long: 103.8198 },
                  temperature: "None"
                };
                this.todayList.push(missingAM);
              }
              // push only latest entry
              if (this.todayList.length === 1) {
                this.todayList.push(displayEntry);
              }
            }
          } else {
            const entryToReplace = displays[entryKey + suffix];
            // replace only if it is None, else already set to latest value
            if (entryToReplace && isNaN(entryToReplace.temperature)) {
              displays[entryKey + suffix] = displayEntry;
            }
          }
        }
        this.displayList = Object.values(displays);
      }
    }
  },
  mounted() {
    this.getEntries();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.entry-list {
  display: flex;
  flex-wrap: wrap;
}
</style>
