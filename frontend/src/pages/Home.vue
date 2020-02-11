<template>
  <div class="hello">
    <img src="../assets/logo.png" alt="Vue.js PWA">
    <h1>Hello {{ name }}</h1>
    <button @click="goToNewEntry()">New Entry</button>
    <h2>Past Records</h2>
    <ul>
      <p v-for="item in list" :key="item.id">Temperature: {{ item.temperature }} </p><br />
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'hello',
  data () {
    return {
      name: 'Ning Yu',
      list: []
    }
  },
  methods: {
    async getEntries () {
      const url = '/api/entries'
      const headers = {
        Authorization: 'Basic bmluZzpjc3k0YnFmNQ=='
      }
      try {
        const response = await axios.get(url, { headers })
        console.log(response.data)
        this.list = response.data
      } catch (err) {
        console.log('Error:', err)
      }
    },
    goToNewEntry () {
      this.$router.push('/entries/new')
    }
  },
  mounted () {
    this.getEntries()
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
