<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <p>Oops! The link has expired. Please register again.</p>
        <v-btn
          @click="goToRegister"
          color="orange accent-4"
          text-color="white"
          class="mr-4 white--text"
          >Register</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "expired",
  methods: {
    goToRegister() {
      this.$router.push("/register");
    }
  }
};
</script>
