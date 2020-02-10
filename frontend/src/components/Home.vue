<template>
  <div class="hello">
    <h1>Hello, {{ name }}</h1>
    <h2>Here are your records for the past week.</h2>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'hello',
  data () {
    return {
      name: 'Ning Yu',
      records: []
    }
  },
  methods: {
      fetchRecords() {

      }
  },
  mounted() {
      this.fetchRecords();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
h1, h2 {
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
  color: #35495E;
}
</style>
