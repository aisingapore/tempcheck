<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <p>
          Oops! The link has expired. A new token has been generated for you.
          Please check your email again and click on the link.
        </p>
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
