<template>
  <div>
    <h2>New Entry</h2>
    <form>
      <input v-model="temperature" placeholder="Temperature" class="form-input-text">
    </form>
  </div>
</template>

<script>
export default {
  name: 'entry-form',
  data: () => ({
    temperature: null
  })
}
</script>
<style scoped>
.form-input-text {
  border: 1px solid grey;
}
</style>
