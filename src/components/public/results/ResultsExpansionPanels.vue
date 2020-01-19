<template>
  <v-expansion-panels accordion v-model="panels">
    <v-expansion-panel>
      <v-expansion-panel-header v-if="changePerDance">
        {{ $t("public.results.adjudicators.header") }}
      </v-expansion-panel-header>
      <v-expansion-panel-header v-else>
        {{ $t("public.results.competition_report.header") }}
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <results-adjudicators-table :adjudicators="adjudicators" />
        <competition-report-final
          v-if="!changePerDance && competition_listing[0].round.type === $constants.FINAL"
          :round="competition_listing[0]"
        />
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel>
      <v-expansion-panel-header>
        {{ $t("public.results.start_list.header") }}
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <results-starting-lists-table
          v-if="singlePartner || randomSinglePartner"
          :competitors="competitors"
        />
        <results-starting-lists-table
          v-else
          :leads="leads"
          :follows="follows"
          change-partner-mode
        />
      </v-expansion-panel-content>
    </v-expansion-panel>

    <template v-if="changePerDance">
      <v-card-subtitle>
        {{ $t("public.results.ranking_report.leads") }}
      </v-card-subtitle>
      <v-expansion-panel>
        <v-expansion-panel-header>
          {{ $t("public.results.competition_listing.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-competition-listing-table
            :rounds="competition_listing_leads"
            change-partner-mode
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>
          {{ $t("public.results.ranking_report.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ranking-report-table :round="round" :data="ranking_report.leads" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="!!evaluation_of_final">
        <v-expansion-panel-header>
          {{ $t("public.results.final_round.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-evaluation-of-final :round="round" :data="evaluation_of_final" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="!!evaluation_of_final">
        <v-expansion-panel-header>
          {{ $t("public.results.skating_report.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-skating-report :round="round" :data="evaluation_of_final" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-card-subtitle>
        {{ $t("public.results.ranking_report.follows") }}
      </v-card-subtitle>
      <v-expansion-panel>
        <v-expansion-panel-header>
          {{ $t("public.results.competition_listing.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-competition-listing-table
            :rounds="competition_listing_follows"
            change-partner-mode
            follows
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>
          {{ $t("public.results.ranking_report.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ranking-report-table :round="round" :data="ranking_report.follows" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="!!evaluation_of_final">
        <v-expansion-panel-header>
          {{ $t("public.results.final_round.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-evaluation-of-final :round="round" :data="evaluation_of_final.follows" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="!!evaluation_of_final">
        <v-expansion-panel-header>
          {{ $t("public.results.skating_report.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-skating-report :round="round" :data="evaluation_of_final.follows" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </template>

    <template v-else>
      <v-expansion-panel>
        <v-expansion-panel-header>
          {{ $t("public.results.competition_listing.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-competition-listing-table :rounds="competition_listing" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>
          {{ $t("public.results.ranking_report.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <ranking-report-table :round="round" :data="ranking_report" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="!!evaluation_of_final">
        <v-expansion-panel-header>
          {{ $t("public.results.final_round.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-evaluation-of-final :round="round" :data="evaluation_of_final" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="!!evaluation_of_final">
        <v-expansion-panel-header>
          {{ $t("public.results.skating_report.header") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <results-skating-report :round="round" :data="evaluation_of_final" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </template>
  </v-expansion-panels>
</template>

<script>
import ResultsAdjudicatorsTable from "@/components/public/results/ResultsAdjudicatorsTable";
import ResultsStartingListsTable from "@/components/public/results/ResultsStartingListsTable";
import ResultsEvaluationOfFinal from "@/components/public/results/ResultsEvaluationOfFinal";
import ResultsSkatingReport from "@/components/public/results/ResultsSkatingReport";
import RankingReportTable from "@/components/tournament_office/round/reports/ranking_report/RankingReportTable";
import ResultsCompetitionListingTable from "@/components/public/results/ResultsCompetitionListingTable";
import CompetitionReportFinal from "@/components/public/results/competition_report/CompetitionReportFinal";
export default {
  props: {
    round: { type: Object, default: () => null },
    adjudicators: { type: Array, default: () => null },
    competitors: { type: Array, default: () => null },
    competition_listing: { type: Array, default: () => null },
    competition_listing_leads: { type: Array, default: () => null },
    competition_listing_follows: { type: Array, default: () => null },
    evaluation_of_final: { type: Object, default: () => null },
    ranking_report: { type: Object, default: () => null },
    leads: { type: Array, default: () => null },
    follows: { type: Array, default: () => null },
    mode: { type: String, default: "" },
    expanded: { type: Boolean, default: true }
  },
  components: {
    CompetitionReportFinal,
    ResultsCompetitionListingTable,
    RankingReportTable,
    ResultsSkatingReport,
    ResultsEvaluationOfFinal,
    ResultsStartingListsTable,
    ResultsAdjudicatorsTable
  },
  data: function() {
    return {
      panels: this.expanded ? 0 : null
    };
  },
  computed: {
    singlePartnerModes() {
      return (
        this.mode === this.$constants.SINGLE_PARTNER ||
        this.mode === this.$constants.RANDOM_SINGLE_PARTNER
      );
    },
    singlePartner() {
      return this.mode === this.$constants.SINGLE_PARTNER;
    },
    randomSinglePartner() {
      return this.mode === this.$constants.RANDOM_SINGLE_PARTNER;
    },
    changePerRound() {
      return this.mode === this.$constants.CHANGE_PER_ROUND;
    },
    changePerDance() {
      return this.mode === this.$constants.CHANGE_PER_DANCE;
    }
  }
};
</script>
