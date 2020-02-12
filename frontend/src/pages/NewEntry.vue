<template>
  <div class="hello">
    <h1>Hello {{ name }}</h1>
    <h2>New Entry</h2>
    <entry-form />
    <button @click="goToHome">Back to Home</button>
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
      name: "Ning Yu",
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
      this.$router.push("/home");
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
</style>
