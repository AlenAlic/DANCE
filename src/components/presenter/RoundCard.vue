<template>
  <v-card>
    <v-card-title>
      {{ competition.name }}
    </v-card-title>
    <v-card-text :class="{ 'pb-0': rounds.length > 0 }">
      <v-progress-linear indeterminate v-if="loading" />
      <v-select
        v-else-if="rounds.length > 0"
        v-model="selectedRound"
        :items="rounds"
        :label="$t('presenter.round.label')"
        item-value="round_id"
        item-text="name"
        :disabled="rounds.length <= 1"
        return-object
      ></v-select>
      <span v-else>
        {{ $t("presenter.round.no_rounds", { competition: competition.name }) }}
      </span>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="primary" text :disabled="loading" :loading="reLoading" @click="reloadRound">
        {{ $t("presenter.round.reload") }}
      </v-btn>
      <v-spacer />
    </v-card-actions>
    <round-data
      v-if="!!selectedRound && !reLoading"
      :round="selectedRound"
      :key="selectedRound.round_id"
      @updated="updateRound"
    />
  </v-card>
</template>

<script>
import Vue from "vue";
import RoundData from "@/components/presenter/RoundData";
export default {
  components: { RoundData },
  props: {
    competition: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      rounds: [],
      selectedRound: undefined,
      reLoading: false
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get(`competition/presenter/${this.competition.competition_id}`)
        .then(response => {
          this.rounds = response.data;
          this.selectedRound = this.rounds.slice(-1)[0];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    reloadRound() {
      if (this.selectedRound) {
        this.reLoading = true;
        Vue.axios
          .get(`round/${this.selectedRound.round_id}/presenter`)
          .then(response => {
            this.selectedRound = response.data;
          })
          .finally(() => {
            this.reLoading = false;
          });
      } else {
        this.getData();
      }
    },
    updateRound(r) {
      this.selectedRound = r;
    }
  }
};
</script>
