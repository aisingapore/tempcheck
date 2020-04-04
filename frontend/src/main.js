import Vue from "vue";
import App from "./App.vue";
import VueRouter from "vue-router";
import * as VueGoogleMaps from "vue2-google-maps";

import router from "./router";
import "./registerServiceWorker";
import vuetify from "./plugins/vuetify";
import '@mdi/font/css/materialdesignicons.css'

Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(VueGoogleMaps, {
  load: {
    key: process.env.VUE_APP_GOOGLE_MAPS_KEY,
    installComponents: true
  }
});

new Vue({
  render: h => h(App),
  vuetify,
  router
}).$mount("#app");
