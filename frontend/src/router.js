import Vue from "vue";
import Router from "vue-router";
import Register from "@/pages/Register";
import SignIn from "@/pages/SignIn";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/signin",
      name: "SignIn",
      component: SignIn
    },
    {
      path: "/register",
      name: "Register",
      component: Register
    },
  ]
});
