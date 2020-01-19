// Main components
import Vue from "vue";
import App from "@/App";
import AppNotLoaded from "@/AppNotLoaded";

// Main extension
import router from "@/router";
import store from "@/store";
import i18n from "@/languages";

// Service Worker
import "./registerServiceWorker";

// Import the config independent modules.
import { frontendApi } from "@/api/frontend";
import { backendServer } from "@/api/backend";
import AuthHandler from "@/components/auth/AuthHandler";
import UtilitiesHandler from "@/assets/js/utilities";
import Notify from "@/plugins/Alerts";
import vuetify from "@/plugins/Vuetify";
import VueAxios from "vue-axios";
import FormRulesHandler from "@/assets/js/formRules";
import Constants from "@/constants";

// Register the config independent modules.
Vue.use(AuthHandler);
Vue.use(UtilitiesHandler);
Vue.use(Notify);
Vue.use(FormRulesHandler);
Vue.use(Constants);

// Turn off Vue Production tip
Vue.config.productionTip = false;

// Mount App function
async function main() {
  try {
    const config = await frontendApi.fetchConfig().catch(err => {
      throw err;
    });

    // Set config
    Vue.prototype.$config = config;
    Vue.prototype.$config.debug = config.debug || process.env.NODE_ENV === "development";

    // Set the baseURL according to the latest config and register the instance.
    backendServer.defaults.baseURL = Vue.prototype.$config.api.url;

    // Register the backend server as the Vue.axios instance.
    Vue.use(VueAxios, backendServer);

    new Vue({
      router,
      store,
      i18n,
      vuetify,
      render: h => h(App)
    }).$mount("#app");
  } catch (error) {
    new Vue({
      el: "#app",
      render: h => h(AppNotLoaded)
    }).$mount("#app");
  }
}

// Mount App
main();
