<template>
  <div v-if="data">
    <template v-for="d in printData">
      <template v-for="c in d.copies">
        <heats-by-starting-no
          v-if="
            d.id === $constants.HEATS_BY_STARTING_NUMBER && (singlePartnerModes || changePerRound)
          "
          :key="`${d.id}-${c}`"
          :round="round"
          :competition="round.competition"
          :data="data[d.id].heat_mapping"
          :competitors="data.competitors"
        />
        <heats-by-starting-no
          v-else-if="d.id === $constants.HEATS_BY_STARTING_NUMBER"
          :key="`${d.id}-${c}`"
          :round="round"
          :competition="round.competition"
          :data="data[d.id].heat_mapping"
          :leads="data.competitors.leads"
          :follows="data.competitors.follows"
          :partner-mapping="data[d.id].partner_mapping"
          change-partner-mode
        />
        <heats-by-dance
          v-if="d.id === $constants.HEATS_BY_DANCE && changePerDance"
          :key="`${d.id}-${c}`"
          :round="round"
          :data="data[d.id].heat_mapping"
          :partner-mapping="data[d.id].partner_mapping"
        />
        <heats-by-dance
          v-else-if="d.id === $constants.HEATS_BY_DANCE"
          :key="`${d.id}-${c}`"
          :round="round"
          :data="data[d.id].heat_mapping"
          :competitors="data.competitors"
          :partner-mapping="data[d.id].partner_mapping"
        />
        <qualified-starts
          v-if="d.id === $constants.QUALIFIED_STARTS && singlePartnerModes"
          :key="`${d.id}-${c}`"
          :round="round"
          :competition="round.competition"
          :competitors="data.competitors"
        />
        <qualified-starts
          v-else-if="d.id === $constants.QUALIFIED_STARTS"
          :key="`${d.id}-${c}`"
          :round="round"
          :competition="round.competition"
          :leads="data.competitors.leads"
          :follows="data.competitors.follows"
          change-partner-mode
        />
        <!--No re-dance-->
        <qualified-starts
          v-if="d.id === $constants.NO_RE_DANCE && singlePartnerModes"
          :key="`${d.id}-${c}`"
          :round="round"
          :competition="round.competition"
          :competitors="data[d.id]"
          re-dance
        />
        <qualified-starts
          v-else-if="d.id === $constants.NO_RE_DANCE"
          :key="`${d.id}-${c}`"
          :round="round"
          :competition="round.competition"
          :leads="data[d.id].leads"
          :follows="data[d.id].follows"
          re-dance
          change-partner-mode
        />
        <adjudicators
          v-if="d.id === $constants.ADJUDICATORS"
          :key="`${d.id}-${c}`"
          :round="round"
          :adjudicators="data.adjudicators"
        />
        <template v-if="d.id === $constants.ADJUDICATION_SHEETS">
          <adjudication-sheet
            v-for="adj in data[d.id].adjudicators"
            :key="`${d.id}-${c}-${adj.adjudicator_id}`"
            :round="round"
            :adjudicator="adj"
            :data="data[d.id].mapping[adj.adjudicator_id]"
          />
        </template>
        <placings-after-round
          v-if="d.id === $constants.PLACINGS_AFTER_ROUND && changePerDance"
          :key="`${d.id}-${c}`"
          :round="round"
          :results="data[d.id].this_round"
          :previous_results="data[d.id].previous_rounds"
          change-partner-mode
        />
        <placings-after-round
          v-else-if="d.id === $constants.PLACINGS_AFTER_ROUND"
          :key="`${d.id}-${c}`"
          :round="round"
          :results="data[d.id].this_round"
          :previous_results="data[d.id].previous_rounds"
        />
        <template v-if="d.id === $constants.EVALUATION_OF_FINAL && changePerDance">
          <evaluation-of-final
            :key="`${d.id}-${c}-leads`"
            :round="round"
            :data="data[d.id]"
            title="Leads"
          />
          <evaluation-of-final
            :key="`${d.id}-${c}-follows`"
            :round="round"
            :data="data[d.id].follows"
            title="Follows"
          />
        </template>
        <evaluation-of-final
          v-else-if="d.id === $constants.EVALUATION_OF_FINAL"
          :key="`${d.id}-${c}`"
          :round="round"
          :data="data[d.id]"
        />
        <ranking-report
          v-else-if="d.id === $constants.RANKING_REPORT"
          :key="`${d.id}-${c}`"
          :round="round"
          :data="data[d.id]"
        />
      </template>
    </template>
  </div>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import HeatsByStartingNo from "@/components/tournament_office/round/reports/heats_by_starting_number/HeatsByStartingNo";
import QualifiedStarts from "@/components/tournament_office/round/reports/qualified_starts/QualifiedStarts";
import Adjudicators from "@/components/tournament_office/round/reports/adjudicators/Adjudicators";
import HeatsByDance from "@/components/tournament_office/round/reports/heats_by_dance/HeatsByDance";
import AdjudicationSheet from "@/components/tournament_office/round/reports/adjudication_sheets/AdjudicationSheet";
import PlacingsAfterRound from "@/components/tournament_office/round/reports/placings_after_round/PlacingsAfterRound";
import EvaluationOfFinal from "@/components/tournament_office/round/reports/evaluation_of_final/EvaluationOfFinal";
import RankingReport from "@/components/tournament_office/round/reports/ranking_report/RankingReport";
export default {
  components: {
    RankingReport,
    EvaluationOfFinal,
    PlacingsAfterRound,
    AdjudicationSheet,
    HeatsByDance,
    Adjudicators,
    QualifiedStarts,
    HeatsByStartingNo,
    Loading
  },
  props: {
    round: { type: Object, default: () => {} },
    printData: { type: Array, default: () => [] }
  },
  data: function() {
    return {
      loading: false,
      data: null
    };
  },
  computed: {
    prints() {
      return this.printData.map(p => p.id);
    },
    singlePartnerModes() {
      return (
        this.round.competition.mode === this.$constants.SINGLE_PARTNER ||
        this.round.competition.mode === this.$constants.RANDOM_SINGLE_PARTNER
      );
    },
    changePerRound() {
      return this.round.competition.mode === this.$constants.CHANGE_PER_ROUND;
    },
    changePerDance() {
      return this.round.competition.mode === this.$constants.CHANGE_PER_DANCE;
    }
  },
  created() {
    this.getPrintData();
  },
  methods: {
    getPrintData() {
      this.loading = true;
      Vue.axios
        .post(`round/${this.$route.params.round_id}/reports`, { prints: this.prints })
        .then(response => {
          this.data = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
