<template>
  <v-container fluid>
    <v-row>
      <v-col>
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
    <v-btn
      text
      color="grey accent-4"
      text-color="white"
      class="mr-4 white--text"
      @click="signOut"
      >Log Out
    </v-btn>
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
      name: "Ning Yu",
      list: []
    };
  },
  methods: {
    async getEntries() {
      const url = "/api/entries";
      const headers = {
        Authorization: "Basic bmluZzpjc3k0YnFmNQ=="
      };
      try {
        const response = await axios.get(url, { headers });
        console.log(response.data);
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
      this.$router.push("/");
    }
  },
  mounted() {
    this.getEntries();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.btn-new-entry {
  background-color: lightgrey;
  font-size: 12px;
}

.entry-list {
  display: flex;
  flex-wrap: wrap;
}
</style>
