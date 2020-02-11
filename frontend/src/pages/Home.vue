<template>
  <div class="hello">
    <img src="../assets/logo.png" alt="Vue.js PWA">
    <h1>Hello {{ name }}</h1>
    <h2>Past Records</h2>
    <ul>
      <p v-for="item in list" :key="item.id"><a href="https://vuejs.org" target="_blank" rel="noopener">Temperature: {{ item.temperature }}</a></p><br />
    </ul>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      name: 'Ning Yu',
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
    }
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
