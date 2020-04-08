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
              <p>Enter new password</p>
              <v-form ref="form" v-model="valid" :lazy-validation="lazy">
                <v-text-field
                  color="orange accent-4"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :rules="[rules.required]"
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  name="input-10-2"
                  label="Password"
                  value
                  v-on:keyup.enter="submit"
                  @click:append="showPassword = !showPassword"
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
  name: "reset-password",
  data: () => {
    return {
      lazy: false,
      valid: false,
      snackbar: {
        show: false,
        message: null,
        color: "success"
      },
      showPassword: false,
      password: null,
      token: null,
      rules: {
        required: value => !!value || "Required."
      }
    };
  },
  methods: {
    submit() {
      // validate data
      this.token = this.$route.query.token;
      if (this.password && this.token) {
        this.save();
      }
    },
    goToHome() {
      this.$router.push("/passwordResetDone");
    },
    save: async function() {
      const data = {
        password: this.password,
        token: this.token
      };
      // push to backend
      const url = "/api/auth/reset-password/confirm/";
      try {
        const response = await axios.post(url, data);
        console.log(response.data);

        if (response.status === 200) {
          this.goToHome();
        }
      } catch (err) {
        let msg = "Error resetting new password!";
        console.log(err.response.data);
        if (err.response.status === 404) {
          this.$router.push("/resetTokenExpired");
        } else {
          if (err.response.data && err.response.data.password) {
            const msgArr = err.response.data.password;
            let m;
            msg = "";
            for (m in msgArr) {
              msg += msgArr[m];
            }
          }
        }
        this.snackbar.message = msg;
        this.snackbar.color = "error";
        this.snackbar.show = true;
      }
    }
  },
  mounted() {
    if (this.$route.name === "ServerError") {
      this.snackbar.message =
        "We are currently experiencing problems with the server. Please try again later.";
      this.snackbar.show = true;
    }
  }
};
</script>
