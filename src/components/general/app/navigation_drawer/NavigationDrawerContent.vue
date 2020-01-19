<template>
  <div>
    <template v-if="!breakpoint">
      <v-list
        dense
        v-if="!$auth.isAuthenticated || $auth.isTournamentOfficeManager || $auth.isPresenter"
      >
        <v-row justify="center">
          <v-img alt="4hf logo" src="../../../../assets/logo-4hf.png" max-width="200" />
        </v-row>
        <template v-if="$auth.isPresenter">
          <v-list-item :to="{ name: 'presenter.dashboard' }">
            <v-list-item-icon>
              <v-icon>mdi-view-dashboard</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ $t("navigation_drawers.dashboard") }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider />
        </template>
        <v-list-item exact :to="{ name: 'home' }" v-if="!$auth.isAuthenticated">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("header.links.home") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item :to="{ name: 'starting_lists' }">
          <v-list-item-icon>
            <v-icon>mdi-format-list-bulleted</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("header.links.starting_lists") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item :to="{ name: 'heat_lists' }">
          <v-list-item-icon>
            <v-icon>mdi-format-list-numbered</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("header.links.heat_lists") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item :to="{ name: 'results' }">
          <v-list-item-icon>
            <v-icon>mdi-license</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("header.links.results") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item :to="{ name: 'events' }" v-if="$store.state.events.events.length > 1">
          <v-list-item-icon>
            <v-icon>mdi-calendar-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("header.links.past_events") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider v-if="$auth.isTournamentOfficeManager" />
    </template>

    <v-list dense v-if="$auth.isAuthenticated">
      <template v-if="$auth.isTournamentOfficeManager">
        <v-list-item :to="{ name: 'tournament_office.dashboard' }">
          <v-list-item-icon>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("navigation_drawers.dashboard") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          v-if="$store.state.events.activeEvent"
          link
          :to="{ name: 'tournament_office.event' }"
        >
          <v-list-item-icon>
            <v-icon>mdi-calendar</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $store.state.events.activeEvent.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          v-else-if="!$store.state.events.loading"
          link
          :to="{ name: 'tournament_office.event' }"
        >
          <v-list-item-icon>
            <v-icon>mdi-calendar</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("navigation_drawers.new_event") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider />
      </template>

      <loading v-if="$store.state.competitions.loading || $store.state.events.loading" />
      <template v-else-if="$auth.isTournamentOfficeManager">
        <div v-for="competition in competitions" :key="competition.competition_id">
          <v-list-group
            v-if="competition.has_rounds"
            :value="
              competition.rounds.map(r => r.round_id).includes(Number($route.params.round_id))
            "
            :group="`/tournament_office/competition/${competition.competition_id}/round/`"
          >
            <template v-slot:activator>
              <v-list-item-title class="text--wrap">
                <b>{{ competition.name }} ({{ competition.number_of_competitors }})</b>
              </v-list-item-title>
            </template>
            <v-list-item
              v-for="round in competition.rounds"
              :key="round.id"
              :to="{
                name: 'tournament_office.round',
                params: { competition_id: competition.competition_id, round_id: round.round_id }
              }"
            >
              <v-list-item-title class="text--wrap">
                {{ round.name }} ({{ round.number_of_couples }})
              </v-list-item-title>
            </v-list-item>
          </v-list-group>
          <v-list-item
            v-else
            :to="{
              name: 'tournament_office.competition',
              params: { competition_id: competition.competition_id }
            }"
          >
            <v-list-item-content>
              <v-list-item-title class="text--wrap">
                <b>{{ competition.name }} ({{ competition.number_of_competitors }})</b>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </div>
      </template>

      <template v-else-if="$auth.isFloorManager">
        <v-list-item :to="{ name: 'floor_manager.dashboard' }">
          <v-list-item-icon>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("navigation_drawers.dashboard") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <loading v-if="$store.state.floor_manager.loading" />
        <v-list-item
          v-for="competition in $store.state.floor_manager.competitions"
          :key="competition.competition_id"
          :to="{
            name: 'floor_manager.competition',
            params: { competition_id: competition.competition_id }
          }"
        >
          <v-list-item-content>
            <v-list-item-title class="text--wrap">
              <b>{{ competition.name }}</b>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </div>
</template>

<script>
import Loading from "@/components/general/loading/Loading";
export default {
  components: { Loading },
  props: { breakpoint: { type: Boolean, default: false } },
  computed: {
    competitions() {
      return this.$store.state.competitions.competitions;
    }
  }
};
</script>
