<template>
  <div>
    <v-card flat class="table-ranking-wrapper report" v-if="!changePerDance">
      <title-box
        class="mb-1"
        :round="round"
        :title="$t(`round.reports.labels.${$constants.RANKING_REPORT}`)"
      />
      <ranking-report-table :round="round" :data="data" />
    </v-card>
    <template v-else>
      <v-card flat class="table-ranking-wrapper report">
        <title-box
          class="mb-1"
          :round="round"
          :title="$t(`round.reports.labels.${$constants.RANKING_REPORT}`)"
          :subtitle="$t('round.reports.ranking_report.leads')"
        />
        <ranking-report-table :round="round" :data="data.leads" />
      </v-card>
      <v-card flat class="table-ranking-wrapper report">
        <title-box
          class="mb-1"
          :round="round"
          :title="$t(`round.reports.labels.${$constants.RANKING_REPORT}`)"
          :subtitle="$t('round.reports.ranking_report.follows')"
        />
        <ranking-report-table :round="round" :data="data.follows" />
      </v-card>
    </template>
  </div>
</template>

<script>
import TitleBox from "@/components/tournament_office/round/reports/TitleBox";
import RankingReportTable from "@/components/tournament_office/round/reports/ranking_report/RankingReportTable";
export default {
  components: { RankingReportTable, TitleBox },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} }
  },
  computed: {
    changePerDance() {
      return this.round.competition.mode === this.$constants.CHANGE_PER_DANCE;
    }
  }
};
</script>
