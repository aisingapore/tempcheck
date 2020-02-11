<template>
  <div class="entry-container">Temperature: {{ temperature }}</div>
</template>

<script>
export default {
  name: "entry-form",
  props: {
    temperature: {
      type: Number,
      default: 37
    }
  }
};
</script>
<style scoped>
.form-input-text {
  border: 1px solid grey;
}
</style>
