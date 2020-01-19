<template>
  <div>
    <v-row justify="center">
      <v-img alt="4hf logo" src="../../../../assets/logo-4hf.png" max-width="200" />
    </v-row>
    <v-list dense v-if="$route.matched.map(r => r.name).includes('tournament_office.event')">
      <v-subheader inset>
        {{ $t("navigation_drawers.event.headers.competition_dependencies") }}
      </v-subheader>

      <v-list-item link :to="{ name: 'tournament_office.event.dances' }">
        <v-list-item-icon>
          <v-icon>mdi-format-list-bulleted</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.dances") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{ name: 'tournament_office.event.disciplines' }">
        <v-list-item-icon>
          <v-icon>mdi-format-list-bulleted</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.disciplines") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{ name: 'tournament_office.event.classes' }">
        <v-list-item-icon>
          <v-icon>mdi-format-list-bulleted</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.classes") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-subheader inset>{{ $t("navigation_drawers.event.headers.adjudication") }}</v-subheader>

      <v-list-item link :to="{ name: 'tournament_office.event.adjudicators' }">
        <v-list-item-icon>
          <v-icon>mdi-account-box</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.adjudicators") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item link :to="{ name: 'tournament_office.event.assignments' }">
        <v-list-item-icon>
          <v-icon>mdi-format-list-checkbox</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.assignments") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-subheader inset>
        {{ $t("navigation_drawers.event.headers.competition_nexus") }}
      </v-subheader>

      <v-list-item link :to="{ name: 'tournament_office.event.dancers' }">
        <v-list-item-icon>
          <v-icon>mdi-account</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.dancers") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item link :to="{ name: 'tournament_office.event.couples' }">
        <v-list-item-icon>
          <v-icon>mdi-account-supervisor</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.couples") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-subheader inset>{{ $t("navigation_drawers.event.headers.publication") }}</v-subheader>

      <v-list-item link :to="{ name: 'tournament_office.event.results' }">
        <v-list-item-icon>
          <v-icon>mdi-publish</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.event.results") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-list v-if="$route.matched.map(r => r.name).includes('tournament_office.round')">
      <v-subheader inset>
        {{ $t("navigation_drawers.round.headers.round") }}
      </v-subheader>

      <v-list-item link :to="{ name: 'tournament_office.round.progress' }">
        <v-list-item-icon>
          <v-icon>mdi-file-outline</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.round.progress") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{ name: 'tournament_office.round.reports' }">
        <v-list-item-icon>
          <v-icon>mdi-file-document-outline</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.round.reports") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-subheader inset>{{ $t("navigation_drawers.round.headers.dance") }}</v-subheader>

      <v-list-item link :to="{ name: 'tournament_office.round.floor_management' }">
        <v-list-item-icon>
          <v-icon>mdi-format-list-checkbox</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>
            {{ $t("navigation_drawers.round.floor_management") }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item link :to="{ name: 'tournament_office.round.adjudication' }">
        <v-list-item-icon>
          <v-icon>mdi-account-box-multiple</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ $t("navigation_drawers.round.adjudication") }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <template v-if="!breakpoint">
      <v-divider />
      <v-row justify="center">
        <v-btn color="primary" class="my-5" @click="signOut()" v-if="$auth.isAuthenticated">
          {{ $t("auth.log_out") }}
        </v-btn>
      </v-row>
    </template>
  </div>
</template>

<script>
export default {
  props: { breakpoint: { type: Boolean, default: false } },
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
