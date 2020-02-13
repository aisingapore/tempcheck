import Vue from "vue";
import Router from "vue-router";
import History from "@/pages/History";
import New from "@/pages/New";
import Register from "@/pages/Register";
import SignIn from "@/pages/SignIn";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "SignIn",
      component: SignIn
    },
    {
      path: "/register",
      name: "Register",
      component: Register
    },
    {
      path: "/history",
      name: "history",
      component: History
    },
    {
      path: "/new",
      name: "New",
      component: New
    }
  ]
});
