<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100">
        <v-container>
          <v-snackbar v-model="snackbar.show" :color="snackbar.color" top>
            {{ snackbar.message }}
            <v-btn text @click="snackbar.show = false">Close</v-btn>
          </v-snackbar>
          <v-row align="center">
            <v-card
              class="mx-auto"
              style="padding-left: 16px; padding-right: 16px; padding-bottom: 16px;"
              min-width="400"
            >
              <h3 class="my-4">Tempcheck</h3>
              <p>Enter email address to send password reset link</p>
              <v-form ref="form" v-model="valid" :lazy-validation="lazy">
                <v-text-field
                  color="orange accent-4"
                  :rules="[rules.required]"
                  v-model="email"
                  name="input-10-2"
                  label="E-mail"
                  value
                  v-on:keyup.enter="submit"
                  class="input-group--focused"
                ></v-text-field>

                <v-btn
                  :disabled="!valid"
                  color="orange accent-4"
                  text-color="white"
                  class="mr-4 white--text"
                  @click="submit"
                >
                  Submit
                  <v-icon class="ml-2">mdi-lock-open</v-icon>
                </v-btn>
                <v-row justify="center" class="mt-8">
                  <v-btn
                    text
                    color="grey accent-4"
                    text-color="white"
                    class="mr-4 white--text"
                    @click="goToHome"
                  >
                    Back to Sign In
                  </v-btn>
                </v-row>
              </v-form>
            </v-card>
          </v-row>
        </v-container>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "forget-password",
  data: () => {
    return {
      lazy: false,
      valid: false,
      email:
        localStorage.getItem("email") !== null
          ? localStorage.getItem("email")
          : "",
      snackbar: {
        show: false,
        message: null,
        color: "success"
      },
      rules: {
        required: value => !!value || "Required."
      }
    };
  },
  methods: {
    submit() {
      // validate data
      if (this.email) {
        this.save();
      }
    },
    goToHome() {
      this.$router.push("/passwordEmailSent");
    },
    save: async function() {
      const data = {
        email: this.email
      };
      // push to backend
      const url = "/api/auth/reset-password/";
      try {
        const response = await axios.post(url, data);
        console.log(response.data);

        if (response.status === 200) {
          this.goToHome();
        }
      } catch (err) {
        this.snackbar.message = "Error requesting password reset!";
        this.snackbar.color = "error";
        this.snackbar.show = true;
        console.log("Error:", err);
      }
    }
  },
  mounted() {
    if (this.$route.name === "EmailSent") {
      this.snackbar.message =
        "Click on the reset password link in the email that we just sent you. ";
      this.snackbar.show = true;
    } else if (this.$route.name === "ServerError") {
      this.snackbar.message =
        "We are currently experiencing problems with the server. Please try again later.";
      this.snackbar.show = true;
    }
  }
};
</script>
