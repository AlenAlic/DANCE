<template>
  <v-row v-if="competition" no-gutters>
    <v-col cols="12" md="8" lg="12" xl="8">
      <competition-form
        class="mx-2 my-2"
        :competition="competition"
        @updated="setCompetition"
        :loading-competition="loading"
        :key="`${competition.competition_id}-cf-${competition.updated}`"
      />
    </v-col>
    <v-col cols="12" md="4" lg="12" xl="4">
      <v-row no-gutters="">
        <v-col cols="12">
          <new-round-form
            class="mx-2 my-2"
            v-if="createNewRound"
            :competition="competition"
            @updated="setCompetition"
            :key="`${competition.competition_id}-nrf-${competition.updated}`"
          />
        </v-col>
        <v-col cols="12" lg="6" xl="12">
          <adjudicators-role-form
            class="mx-2 my-2"
            v-if="adjudicatorsRole"
            :competition="competition"
            @updated="setCompetition"
            :key="`${competition.competition_id}-arf-${competition.updated}`"
          />
        </v-col>
        <v-col cols="12" lg="6" xl="12">
          <adjudicators-floor-form
            class="mx-2 my-2"
            v-if="adjudicatorsFloor"
            :competition="competition"
            @updated="setCompetition"
            :key="`${competition.competition_id}-aff-${competition.updated}`"
          />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import CompetitionForm from "@/components/tournament_office/competition/CompetitionForm";
import NewRoundForm from "@/components/tournament_office/competition/NewRoundForm";
import AdjudicatorsFloorForm from "@/components/tournament_office/competition/AdjudicatorsFloorForm";
import AdjudicatorsRoleForm from "@/components/tournament_office/competition/AdjudicatorsRoleForm";
import { UPDATE_COMPETITION } from "@/store/modules/competitions";
export default {
  components: {
    AdjudicatorsRoleForm,
    Loading,
    AdjudicatorsFloorForm,
    NewRoundForm,
    CompetitionForm
  },
  data: function() {
    return {
      loading: false,
      competition: null
    };
  },
  created() {
    this.getCompetition();
  },
  computed: {
    createNewRound() {
      return this.competition && this.competition.can_create_first_round;
    },
    adjudicatorsFloor() {
      return this.competition && this.competition.floors > 1 && this.competition.has_adjudicators;
    },
    adjudicatorsRole() {
      return (
        this.competition &&
        this.competition.has_adjudicators &&
        this.competition.mode === this.$constants.CHANGE_PER_DANCE
      );
    }
  },
  methods: {
    getCompetition() {
      this.loading = true;
      Vue.axios
        .get(`competition/${this.$route.params.competition_id}`)
        .then(response => {
          this.competition = response.data;
          this.$store.commit(UPDATE_COMPETITION, response.data);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    setCompetition(competition) {
      this.competition = competition;
    }
  },
  watch: {
    $route: function() {
      this.getCompetition();
    }
  }
};
</script>
