import VueRouter from "vue-router";
import History from "@/pages/History";
import New from "@/pages/New";
import Register from "@/pages/Register";
import SignIn from "@/pages/SignIn";

const routes = [
  {
    path: "/",
    name: "SignIn",
    component: SignIn,
    children: [
      {
        path: "",
        name: "NormalSignIn"
      },
      {
        path: "/verified",
        name: "Verified"
      },
      {
        path: "/renewToken",
        name: "RenewToken"
      },
      {
        path: "/emailSent",
        name: "EmailSent"
      },
      {
        path: "/serverError",
        name: "ServerError"
      }
    ]
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    children: [
      {
        path: "/serverError",
        name: "ServerError"
      }
    ]
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
});

/*
Current Router logic:
If going to dashboard/new
--> if token does not exist or has expired
    --> send to login
If going to login/register
--> if token exists and has not expired
    --> send to history
*/

router.beforeEach((to, from, next) => {
  console.log("Checking route request", to);
  const userToken = localStorage.getItem("token");
  const tokenExpiry = new Date(localStorage.getItem("tokenExpiry"));
  const today = new Date();
  if (to.matched.some(record => record.meta.requiresAuth)) {
    console.log("Found token. Continue to page");
    if (userToken == null || today >= tokenExpiry) {
      localStorage.removeItem("token");
      localStorage.removeItem("tokenExpiry");

      console.log("No/Expired token. Redirecting to sign in page");
      next({
        path: "/",
        params: { nextUrl: to.fullPath }
      });
    } else {
      next();
    }
  } else if (
    to.matched.some(
      record => record && !(userToken == null || today >= tokenExpiry)
    )
  ) {
    console.log("User already signed in. Redirecting to dashboard");
    next({
      path: "/history"
    });
  } else {
    localStorage.removeItem("token");
    localStorage.removeItem("tokenExpiry");
    next();
  }
});

export default router;
