<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100">
        <v-container>
          <v-row align="center">
            <v-card
              class="mx-auto"
              style="padding-left: 16px; padding-right: 16px; padding-bottom: 16px;"
              min-width="400"
            >
              <h3>Sign In Here!</h3>
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
                  @click="login"
                  >Sign In
                </v-btn>
                <v-btn
                  color="grey accent-4"
                  text-color="white"
                  class="mr-4 white--text"
                  @click="goToRegister"
                  >Go to Register?
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
  name: "signin",
  data: () => {
    return {
      lazy: false,
      valid: false,
      invalidCredentials: false,
      email: "",
      password: "",
      showPassword: false,
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
      this.$router.push("/");
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
        console.log(data);
        const response = await axios.post(url, data);
        console.log(response.data);

        const token = response.data.token;

        // extract token and put in session

        if (token) {
          localStorage.setItem("token", token);
          this.goToHome();
        } else {
          this.invalidCredentials = true;
          // console.log("No token in headers", headers);
        }
      } catch (err) {
        console.log("Error:", err);
      }
    },
    onType: function() {
      this.invalidCredentials = false;
    }
  }
};
</script>
