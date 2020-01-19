import Vue from "vue";
import VueRouter from "vue-router";

// Pages
const Home = () => import("@/pages/Home.vue");
const PageNotFound = () => import("@/pages/PageNotFound.vue");

// Pages modules
import tournamentOfficePages from "@/router/modules/tournament_office";
import adjudicatorPages from "@/router/modules/adjudicator";
import floorManagerPages from "@/router/modules/floor_manager";
import presenterPages from "@/router/modules/presenter";

// Public pages
import startingListPages from "@/router/modules/starting_lists";
import heatListsPages from "@/router/modules/heat_lists";
import resultsPages from "@/router/modules/results";
import pastEventPages from "@/router/modules/past_events";

Vue.use(VueRouter);

const routes = [
  {
    path: "/index.html",
    alias: "/",
    component: Home
  },
  {
    path: "/",
    name: "home",
    component: Home
  },
  tournamentOfficePages,
  adjudicatorPages,
  floorManagerPages,
  presenterPages,
  startingListPages,
  heatListsPages,
  resultsPages,
  pastEventPages,
  {
    path: "/dashboard",
    name: "dashboard",
    meta: {
      auth: true
    }
  },
  {
    path: "**",
    name: "PageNotFound",
    component: PageNotFound
  }
];

const router = new VueRouter({
  mode: "history",
  linkActiveClass: "is-active",
  linkExactActiveClass: "is-active",
  routes
});

/**
 * Handle routes that need authentication
 */
router.beforeEach((to, from, next) => {
  if (!Vue.prototype.$auth.isAuthenticated) {
    if (to.matched.filter(r => r.meta.auth).length > 0) {
      next({
        name: "home",
        query: {
          redirect: to.path
        }
      });
      return;
    }
  } else {
    if (to.name === "dashboard" || to.name === "home" || (to.name && to.fullPath === "/")) {
      if (Vue.prototype.$auth.isTournamentOfficeManager) {
        next({ name: "tournament_office.dashboard" });
      }
      if (Vue.prototype.$auth.isFloorManager) {
        next({ name: "floor_manager.dashboard" });
      }
      if (Vue.prototype.$auth.isAdjudicator) {
        next({ name: "adjudicator.dashboard" });
      }
      if (Vue.prototype.$auth.isPresenter) {
        next({ name: "presenter.dashboard" });
      }
      return;
    } else {
      if (
        to.matched.filter(
          r => r.meta.access !== undefined && r.meta.access !== Vue.prototype.$auth.access
        ).length > 0
      ) {
        next({ name: "home" });
        return;
      }
    }
  }
  next();
});

/**
 * Disable debug routes on production
 */
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.debugRoute)) {
    if (!Vue.prototype.$config.debug) {
      next({
        name: "home",
        query: {
          redirect: to.path
        }
      });
      return;
    }
  }
  next();
});

export default router;
