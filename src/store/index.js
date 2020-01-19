import Vue from "vue";
import Vuex from "vuex";
import auth from "./modules/auth";
import config from "./modules/config";
import competitions from "./modules/competitions";
import events from "./modules/events";
import dependencies from "./modules/dependencies";
import adjudicators from "./modules/adjudicators";
import couples from "./modules/couples";
import dancers from "./modules/dancers";
import adjudication from "./modules/adjudication";
import floor_manager from "./modules/floor_manager";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth: auth,
    config: config,
    competitions: competitions,
    events: events,
    dependencies: dependencies,
    adjudicators: adjudicators,
    couples: couples,
    dancers: dancers,
    adjudication: adjudication,
    floor_manager: floor_manager
  }
});
