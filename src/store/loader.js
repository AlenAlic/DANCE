import Vue from "vue";
import store from "@/store";
import { CONFIG } from "@/store/modules/config";
import { COMPETITIONS } from "@/store/modules/competitions";
import { EVENTS } from "@/store/modules/events";
import { ALL_DEPENDENCIES } from "@/store/modules/dependencies";
import { ADJUDICATORS } from "@/store/modules/adjudicators";
import { COUPLES } from "@/store/modules/couples";
import { DANCERS } from "@/store/modules/dancers";
import { FLOOR_MANAGER } from "@/store/modules/floor_manager";

export default () => {
  store.dispatch(CONFIG);
  store.dispatch(EVENTS);
  if (Vue.prototype.$auth.isTournamentOfficeManager) {
    // store.dispatch(CONFIG);
    // store.dispatch(EVENTS);
    store.dispatch(COMPETITIONS);
    store.dispatch(ALL_DEPENDENCIES);
    store.dispatch(ADJUDICATORS);
    store.dispatch(COUPLES);
    store.dispatch(DANCERS);
  }
  if (Vue.prototype.$auth.isFloorManager) {
    store.dispatch(FLOOR_MANAGER);
  }
};
