<template>
  <v-app-bar dark app :clipped-left="breakpoint" :clipped-right="breakpoint" color="primary">
    <v-app-bar-nav-icon v-if="!breakpoint && showNav" @click.stop="$emit('toggleDrawer')" />

    <v-toolbar-title>
      <router-link tag="span" class="is-clickable" :to="{ name: 'home' }">
        {{ $t("header.links.title") }}
      </router-link>
    </v-toolbar-title>

    <v-spacer />

    <v-toolbar-items v-if="showPublicPages">
      <v-btn text :to="{ name: 'starting_lists' }">{{ $t("header.links.starting_lists") }}</v-btn>
      <v-btn text :to="{ name: 'heat_lists' }">{{ $t("header.links.heat_lists") }}</v-btn>
      <v-btn text :to="{ name: 'results' }">{{ $t("header.links.results") }}</v-btn>
      <v-btn text :to="{ name: 'events' }" v-if="$store.state.events.events.length > 1">
        {{ $t("header.links.past_events") }}
      </v-btn>
    </v-toolbar-items>

    <v-spacer />

    <v-btn
      text
      @click="signOut()"
      v-if="($auth.isAuthenticated && breakpoint) || $auth.isFloorManager || $auth.isPresenter"
    >
      {{ $t("auth.log_out") }}
    </v-btn>

    <v-icon v-if="!breakpoint && showRightNav" @click.stop="$emit('toggleRightDrawer')">
      mdi-dots-vertical
    </v-icon>
  </v-app-bar>
</template>

<script>
export default {
  props: {
    showNav: { type: Boolean, default: false },
    showRightNav: { type: Boolean, default: false },
    breakpoint: { type: Boolean, default: false }
  },
  computed: {
    showPublicPages() {
      return (
        this.breakpoint &&
        (!this.$auth.isAuthenticated ||
          this.$auth.isTournamentOfficeManager ||
          this.$auth.isPresenter)
      );
    }
  },
  methods: {
    signOut: function() {
      this.$auth.signOut().then(() => {
        this.$router.push({
          name: "home"
        });
      });
    }
  }
};
</script>
