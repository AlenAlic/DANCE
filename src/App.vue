<template>
  <v-app>
    <adjudicator-header
      v-if="$auth.isAdjudicator && $route.name === 'adjudicator.dance'"
      :adjudication="$store.state.adjudication"
    />
    <app-header
      v-else-if="!$auth.isAdjudicator"
      @toggleDrawer="toggleDrawer"
      :show-nav="showNavDrawer"
      @toggleRightDrawer="toggleRightDrawer"
      :show-right-nav="showRightNavDrawer"
      :breakpoint="breakpoint"
    />

    <v-navigation-drawer
      v-if="showNavDrawer"
      v-model="drawer"
      :clipped="breakpoint"
      :permanent="breakpoint"
      app
    >
      <navigation-drawer-content :breakpoint="breakpoint" />
    </v-navigation-drawer>

    <v-navigation-drawer
      v-if="showRightNavDrawer"
      v-model="rightDrawer"
      :clipped="breakpoint"
      :permanent="breakpoint"
      app
      right
    >
      <right-navigation-drawer-content :breakpoint="breakpoint" />
    </v-navigation-drawer>

    <v-content>
      <transition name="fade" mode="out-in">
        <router-view
          v-if="!$auth.isAuthenticated || ($auth.isAuthenticated && $store.state.config.config)"
        ></router-view>
      </transition>
    </v-content>
  </v-app>
</template>

<script>
import NavigationDrawerContent from "@/components/general/app/navigation_drawer/NavigationDrawerContent";
import AppHeader from "@/components/general/app/AppHeader";
import loadStore from "@/store/loader";
import { CONFIG } from "@/store/modules/config";
import { EVENTS } from "@/store/modules/events";
import RightNavigationDrawerContent from "@/components/general/app/navigation_drawer/RightNavigationDrawerContent";
import AdjudicatorHeader from "@/components/adjudication/AdjudicatorHeader";
export default {
  name: "App",
  components: {
    AdjudicatorHeader,
    RightNavigationDrawerContent,
    NavigationDrawerContent,
    AppHeader
  },
  data: () => ({
    drawer: null,
    rightDrawer: null
  }),
  created() {
    this.$store.dispatch(CONFIG);
    this.$store.dispatch(EVENTS);
    this.$nextTick(function() {
      this.$auth
        .renew()
        .then(() => {
          loadStore();
        })
        .catch(() => {
          this.$router.push({
            name: "home"
          });
        });
    });
  },
  computed: {
    breakpoint() {
      return this.$vuetify.breakpoint.lgAndUp;
    },
    showNavDrawer() {
      return (
        this.$auth.isTournamentOfficeManager ||
        this.$auth.isFloorManager ||
        (this.$auth.isPresenter && !this.breakpoint) ||
        (!this.$auth.isAuthenticated && !this.breakpoint)
      );
    },
    showRightNavDrawer() {
      return this.$auth.isTournamentOfficeManager;
    }
  },
  methods: {
    toggleDrawer() {
      this.drawer = !this.drawer;
    },
    toggleRightDrawer() {
      this.rightDrawer = !this.rightDrawer;
    }
  }
};
</script>

<style src="./assets/css/styles.scss" lang="scss"></style>
