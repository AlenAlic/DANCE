<template>
  <v-card>
    <v-card-title>
      {{ $t("round.new_round.adjudicators_roles.title") }}
    </v-card-title>
    <v-card-text class="text--wrap">
      {{ $t("round.new_round.adjudicators_roles.text") }}
    </v-card-text>
    <v-card-text>
      <v-row>
        <v-col
          v-for="adj in adjudicatorData"
          :key="adj.adjudicator_competition_assignment_id"
          cols="6"
          sm="4"
          md="12"
          lg="6"
          xl="12"
        >
          <v-select
            v-model="adjudicators[adj.adjudicator_competition_assignment_id]"
            :items="$store.state.config.config.adjudication_assignments"
            :label="adj.name"
            item-text="name"
          ></v-select>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn :loading="loading" color="primary" text @click="saveAdjudicators">
        {{ $t("round.new_round.adjudicators_roles.submit") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { UPDATE_COMPETITION } from "@/store/modules/competitions";
export default {
  props: {
    competition: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      adjudicators: Object.assign(
        ...this.competition.adjudicators.map(a => ({
          [a.adjudicator_competition_assignment_id]: a.assignment
        }))
      ),
      adjudicatorData: this.competition.adjudicators
    };
  },
  computed: {
    createNextRound() {
      let assignments = this.$store.state.config.config.adjudication_assignments;
      assignments.find(x => x.value === "both").text = this.$t(
        "round.new_round.adjudicators_roles.both"
      );
      return assignments;
    },
    showAddRemoveCouple() {
      return (
        this.round &&
        this.round.type !== this.$constants.FINAL &&
        this.round.competition.rounds === 1 &&
        this.round.competition.mode !== this.$constants.CHANGE_PER_DANCE
      );
    }
  },
  methods: {
    saveAdjudicators() {
      this.loading = true;
      Vue.axios
        .post(`competition/${this.$route.params.competition_id}/role_assignments`, {
          role_assignments: this.adjudicators
        })
        .then(response => {
          store.commit(UPDATE_COMPETITION, response.data);
          this.$emit("updated", response.data);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
