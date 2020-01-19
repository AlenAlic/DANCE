<template>
  <v-row>
    <v-col cols="12" xl="6">
      <v-card>
        <v-card-title>
          {{ $t("event.final_results.title") }}
        </v-card-title>
        <v-card-subtitle>
          {{ $t("event.final_results.subtitle") }}
        </v-card-subtitle>
        <v-card-text>
          <v-checkbox
            v-for="comp in data"
            :key="comp.competition_id"
            v-model="competitions"
            :label="comp.name"
            :value="comp.competition_id"
            hide-details
            color="primary"
            :disabled="!comp.publishable"
          ></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn :loading="loading" color="primary" text @click="publishFinalResults">
            {{ $t("event.final_results.save") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import Vue from "vue";
export default {
  data: function() {
    return {
      loading: false,
      data: [],
      competitions: []
    };
  },
  created() {
    this.getCompetitions();
  },
  methods: {
    getCompetitions() {
      this.loading = true;
      Vue.axios
        .get("competition/results")
        .then(response => {
          this.data = response.data;
          this.competitions = response.data
            .filter(c => c.results_published)
            .map(c => c.competition_id);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    publishFinalResults() {
      this.loading = true;
      Vue.axios
        .patch("competition/results", {
          competitions: this.competitions
        })
        .then(response => {
          this.data = response.data;
          this.competitions = response.data
            .filter(c => c.results_published)
            .map(c => c.competition_id);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
