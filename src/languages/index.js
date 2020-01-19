import Vue from "vue";
import VueI18n from "vue-i18n";

Vue.use(VueI18n);

// Import translations for all available languages
import en from "./en.json";
import nl from "./nl.json";

const messages = {
  en,
  nl
};

// Create a new vuei18n object with the locale and all messages.
const i18n = new VueI18n({
  locale: "en",
  messages
});

export default i18n;
