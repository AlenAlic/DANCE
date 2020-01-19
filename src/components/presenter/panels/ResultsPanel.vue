<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <span>
        <span class="mr-3">
          {{ $t("presenter.panel.results") }}
        </span>
        <v-progress-circular indeterminate color="primary" size="12" width="3" v-if="loading" />
      </span>
    </v-expansion-panel-header>
    <v-expansion-panel-content v-if="data && roundData && results">
      <v-row>
        <v-col :cols="round.mode === $constants.CHANGE_PER_DANCE ? 6 : 12">
          <div v-if="round.mode === $constants.CHANGE_PER_DANCE" class="title">
            {{ $t("presenter.leads") }}
          </div>
          <table class="mb-5">
            <thead>
              <tr>
                <th>
                  <span class="mr-3">{{ $t("presenter.place") }}</span>
                </th>
                <th>
                  <span class="mr-3">{{ $t("presenter.number") }}</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="result in leads" :key="result.round_result_id">
                <td class="text-right">
                  <b class="mr-3">{{ result.final_placing }}</b>
                </td>
                <td class="text-right">
                  <b class="mr-3">{{ result.couple.number }}</b>
                </td>
                <td v-if="round.mode === $constants.CHANGE_PER_DANCE">
                  {{ result.couple.lead.name }}
                </td>
                <td v-else>{{ result.couple.lead.name }}/{{ result.couple.follow.name }}</td>
              </tr>
            </tbody>
          </table>
          <final-summary
            :round="roundData"
            :results="data.summary"
            :numbers="data.numbers"
            class="presenter-final-results"
          />
          <rule-ten-eleven
            v-if="data.rule10.length > 0"
            :round="roundData"
            :results="data.rule10"
            :numbers="data.numbers"
            :title="$t('round.reports.final_evaluation.rule10')"
            class="presenter-final-results"
          />
          <rule-ten-eleven
            v-if="data.rule11.length > 0"
            :round="roundData"
            :results="data.rule11"
            :numbers="data.numbers"
            :title="$t('round.reports.final_evaluation.rule11')"
            class="presenter-final-results"
          />
        </v-col>
        <v-col v-if="round.mode === $constants.CHANGE_PER_DANCE" cols="6">
          <div class="title">{{ $t("presenter.follows") }}</div>
          <table class="mb-5">
            <thead>
              <tr>
                <th>
                  <span class="mr-3">{{ $t("presenter.place") }}</span>
                </th>
                <th>
                  <span class="mr-3">{{ $t("presenter.number") }}</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="result in follows" :key="result.round_result_id">
                <td class="text-right">
                  <b class="mr-3">{{ result.final_placing }}</b>
                </td>
                <td class="text-right">
                  <b class="mr-3">{{ result.couple.follow.number }}</b>
                </td>
                <td>{{ result.couple.follow.name }}</td>
              </tr>
            </tbody>
          </table>
          <final-summary
            :round="roundData"
            :results="data.follows.summary"
            :numbers="data.follows.numbers"
            class="presenter-final-results"
          />
          <rule-ten-eleven
            v-if="data.follows.rule10.length > 0"
            :round="roundData"
            :results="data.follows.rule10"
            :numbers="data.follows.numbers"
            :title="$t('round.reports.final_evaluation.rule10')"
            class="presenter-final-results"
          />
          <rule-ten-eleven
            v-if="data.follows.rule11.length > 0"
            :round="roundData"
            :results="data.follows.rule11"
            :numbers="data.follows.numbers"
            :title="$t('round.reports.final_evaluation.rule11')"
            class="presenter-final-results"
          />
        </v-col>
      </v-row>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import Vue from "vue";
import FinalSummary from "@/components/tournament_office/round/reports/evaluation_of_final/tables/FinalSummary";
import RuleTenEleven from "@/components/tournament_office/round/reports/evaluation_of_final/tables/RuleTenEleven";
export default {
  components: { RuleTenEleven, FinalSummary },
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      data: null,
      roundData: null,
      results: null
    };
  },
  created() {
    this.getData();
  },
  computed: {
    leads() {
      return this.results && this.results.filter(r => !r.follow);
    },
    follows() {
      return this.results && this.results.filter(r => !!r.follow);
    }
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.round.round_id}/presenter/results`)
        .then(response => {
          this.data = response.data.data;
          this.roundData = response.data.round;
          this.results = response.data.results;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

<style lang="scss">
.presenter-final-results {
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 100% !important;
  }
}
</style>
