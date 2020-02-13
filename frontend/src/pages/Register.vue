<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100">
        <v-container>
          <v-snackbar v-model="snackbar.show" color="error" top>
            {{ snackbar.message }}
            <v-btn text @click="snackbar.show = false">Close</v-btn>
          </v-snackbar>
          <v-row align="center">
            <v-card
              class="mx-auto"
              style="padding-left: 16px; padding-right: 16px; padding-bottom: 16px;"
              min-width="400"
            >
              <h3>Register your Details!</h3>
              <v-form ref="form" v-model="valid" :lazy-validation="lazy">
                <v-text-field
                  color="orange accent-4"
                  :rules="[rules.required]"
                  v-model="email"
                  name="input-10-2"
                  label="E-mail"
                  value
                  v-on:keyup="onType"
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
                  v-on:keyup="onType"
                  @click:append="showPassword = !showPassword"
                ></v-text-field>
                <v-p v-if="invalidCredentials" class="errorMsg">
                  Invalid credentials
                </v-p>
                <v-btn
                  :disabled="!valid"
                  color="orange accent-4"
                  text-color="white"
                  class="mr-4 white--text"
                  @click="register"
                  >Register
                </v-btn>
                <v-btn
                  color="grey accent-4"
                  text-color="white"
                  class="mr-4 white--text"
                  @click="goToSignIn"
                  >Go to Sign In?
                </v-btn>
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
  name: "Register",

  data: () => {
    return {
      lazy: false,
      valid: false,
      invalidCredentials: false,
      email: "",
      password: "",
      showPassword: false,
      snackbar: {
          show: false,
          message: null,
      },
      rules: {
        required: value => !!value || "Required."
      }
    };
  },
  methods: {
    register() {
      // validate data
      if (this.username !== "" && this.password !== "") {
        this.save();
      }
    },
    goToSignIn() {
      this.$router.push("/signin");
    },
    save: async function() {
      const data = {
        email: this.email,
        password: this.password
      };
      // push to backend
      const url = "/api/auth/register";
      try {
        console.log(data);
        const response = await axios.post(url, data);
        console.log(response.data);
        this.goToHome();
      } catch (err) {
        this.snackbar.message = "Error registering!"
        this.snackbar.show = true;
        console.log("Error:", err);
      }
    },
    goToHome() {
      this.$router.push("/signin");
    },
    onType: function() {
      this.invalidCredentials = false;
    }
  }
};
</script>
