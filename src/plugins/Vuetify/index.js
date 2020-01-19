import Vue from "vue";
import Vuetify from "vuetify/lib";
// import "vuetify/dist/vuetify.min.css";
import "@mdi/font/css/materialdesignicons.css";
import variables from "../../assets/css/general/settings.scss";

Vue.use(Vuetify);

const opts = {
  theme: {
    themes: {
      light: {
        primary: variables.primary,
        secondary: variables.secondary,
        accent: variables.accent,
        error: variables.error,
        warning: variables.warning,
        info: variables.info,
        success: variables.success
      }
    }
  },
  icons: {
    iconfont: "mdi"
  }
};

export default new Vuetify(opts);
