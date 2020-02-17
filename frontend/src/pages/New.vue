<template>
  <div id="new-entry">
    <h1>{{ name }}</h1>
    <h2>New Entry <v-icon>mdi-thermometer-lines</v-icon></h2>
    <entry-form />
    <button @click="goToHome">History</button>
  </div>
</template>

<script>
import EntryForm from "@/components/EntryForm";
export default {
  name: "hello",
  components: {
    "entry-form": EntryForm
  },
  data() {
    return {
      name: localStorage.getItem("email"),
      list: [
        {
          id: 1,
          temperature: 37.1
        },
        {
          id: 2,
          temperature: 37.2
        }
      ]
    };
  },
  methods: {
    goToHome() {
      this.$router.push("/history");
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #35495e;
}

#new-entry {
  margin-top: 30px;
}
</style>
