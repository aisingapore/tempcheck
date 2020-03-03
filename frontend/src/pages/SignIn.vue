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
              <h3 class="my-4">Temperature recorder</h3>
              <v-form ref="form" v-model="valid" :lazy-validation="lazy">
                <v-text-field
                  color="orange accent-4"
                  :rules="[rules.required]"
                  v-model="email"
                  name="input-10-2"
                  label="E-mail"
                  value
                  v-on:keyup.enter="validate"
                  class="input-group--focused"
                ></v-text-field>

                <v-text-field
                  color="orange accent-4"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :rules="[rules.required]"
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  name="input-10-2"
                  label="Password"
                  value
                  v-on:keyup.enter="validate"
                  @click:append="showPassword = !showPassword"
                ></v-text-field>
                <v-checkbox
                  v-model="checkbox"
                  :label="`Remember Me`"
                ></v-checkbox>
                <v-btn
                  :disabled="!valid"
                  color="orange accent-4"
                  text-color="white"
                  class="mr-4 white--text"
                  @click="login"
                >
                  Sign In
                  <i class="material-icons">lock_open</i>
                </v-btn>
                <v-row justify="center" class="mt-8">
                  <v-btn
                    text
                    color="grey accent-4"
                    text-color="white"
                    class="mr-4 white--text"
                    @click="goToRegister"
                  >
                    No account?
                    <br />Register here
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
  name: "signin",
  data: () => {
    return {
      lazy: false,
      valid: false,
      email:
        localStorage.getItem("email") !== null
          ? localStorage.getItem("email")
          : "",
      password: "",
      showPassword: false,
      checkbox: true,
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
    login() {
      // validate data
      if (this.username !== "" && this.password !== "") {
        this.save();
      }
    },
    goToHome() {
      this.$router.push("/history");
    },
    goToRegister() {
      this.$router.push("/register");
    },
    save: async function() {
      const data = {
        username: this.email,
        password: this.password
      };
      // push to backend
      const url = "/api/auth/login";
      try {
        const response = await axios.post(url, data);
        console.log(response.data);
        console.log(response);

        const token = response.data.token;
        const tokenExpiry = response.data.expiry;

        if (response.status === 200) {
          if (token) {
            localStorage.setItem("token", token);
            localStorage.setItem("tokenExpiry", tokenExpiry);
            if (this.checkbox === true) {
              localStorage.setItem("email", this.email);
            } else {
              localStorage.removeItem("email");
            }
            this.goToHome();
          }
        } else if (response.status === 205) {
          this.snackbar.message =
            "Your account has not been verified yet. Check your email for the verification " +
            "link that we have just sent you.";
          this.snackbar.color = "warning";
          this.snackbar.show = true;
        }
      } catch (err) {
        this.snackbar.message = "Error logging in!";
        this.snackbar.color = "error";
        this.snackbar.show = true;
        console.log("Error:", err);
      }
    }
  },
  mounted() {
    if (this.$route.name === "Verified") {
      this.snackbar.message =
        "Your email has been verified! " +
        "Sign in to record your temperature.";
      this.snackbar.show = true;
    } else if (this.$route.name === "RenewToken") {
      this.snackbar.message =
        "This verification link has expired. " +
        "Click on the new link which we have just sent you.";
      this.snackbar.color = "warning";
      this.snackbar.show = true;
    } else if (this.$route.name === "EmailSent") {
      this.snackbar.message =
        "Thank you for registering. Click on the confirmation link " +
        "in the email that we just sent you. ";
      this.snackbar.show = true;
    } else if (this.$route.name === "ServerError") {
      this.snackbar.message =
        "We are currently experiencing problems with the server. Please try again later.";
      this.snackbar.show = true;
    }
  }
};
</script>
