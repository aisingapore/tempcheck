import VueRouter from "vue-router";
import History from "@/pages/History";
import New from "@/pages/New";
import Register from "@/pages/Register";
import SignIn from "@/pages/SignIn";

const routes = [
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
    component: History,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/new",
    name: "New",
    component: New,
    meta: {
      requiresAuth: true
    }
  }
];

const router = new VueRouter({
  routes // short for `routes: routes`
})

router.beforeEach((to, from, next) => {
  console.log("Checking route request", to);
  const userToken = localStorage.getItem("token");
  if (to.matched.some(record => record.meta.requiresAuth)) {
    console.log("Found token. Continue to page");
    if (userToken == null) {
      console.log("No token. Redirecting to sign in page");
      next({
        path: "/",
        params: { nextUrl: to.fullPath }
      });
    } else {
      next();
    }
  } else if (
    to.matched.some(record => record && to.path === "/" && userToken)
  ) {
    console.log("User already signed in. Redirecting to dashboard");
    next({
      path: "/history"
    });
  } else {
    next();
  }
});

export default router;
