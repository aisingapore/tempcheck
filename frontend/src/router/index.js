import Vue from "vue";
import Router from "vue-router";
import HelloWorld from "@/components/HelloWorld";
import History from "@/pages/History";
import New from "@/pages/New";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Hello",
      component: HelloWorld
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
