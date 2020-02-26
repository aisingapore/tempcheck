<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <p>
          Your email has been verified! Sign in and record your temperature.
        </p>
        <v-btn
          @click="goToSignIn"
          color="orange accent-4"
          text-color="white"
          class="mr-4 white--text"
          >Sign in</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "verified-email",
  methods: {
    goToSignIn() {
      this.$router.push("/");
    }
  }
};
</script>
