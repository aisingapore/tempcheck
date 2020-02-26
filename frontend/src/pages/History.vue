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
    <div class="entry-list">
      <entry
        v-for="item in list"
        :key="item.id"
        :temperature="parseFloat(item.temperature)"
        :timeTaken="new Date(item.date_created)"
        :location="{ lat: item.lat, long: item.long }"
      />
    </div>
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
import Entry from "@/components/Entry";
export default {
  name: "hello",
  components: {
    entry: Entry
  },
  data() {
    return {
      name: localStorage.getItem("email"),
      list: []
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
        this.list = response.data;
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
    }
  },
  mounted() {
    this.getEntries();
    console.log("VUE_APP_GOOGLE_MAPS_KEY", process.env.VUE_APP_GOOGLE_MAPS_KEY);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.entry-list {
  display: flex;
  flex-wrap: wrap-reverse;
  flex-direction: row-reverse;
}
</style>
