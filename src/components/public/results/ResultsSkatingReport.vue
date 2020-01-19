<template>
  <div class="table-ranking-wrapper">
    <v-row no-gutters>
      <v-col cols="12">
        <final-summary :round="round" :results="data.summary" :numbers="data.numbers" light />
      </v-col>
      <v-col v-if="data.rule10.length > 0" cols="12">
        <rule-ten-eleven
          :round="round"
          :results="data.rule10"
          :numbers="data.numbers"
          :title="$t('round.reports.final_evaluation.rule10')"
          light
        />
      </v-col>
      <v-col v-if="data.rule11.length > 0" cols="12">
        <rule-ten-eleven
          :round="round"
          :results="data.rule11"
          :numbers="data.numbers"
          :title="$t('round.reports.final_evaluation.rule11')"
          light
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import FinalSummary from "@/components/tournament_office/round/reports/evaluation_of_final/tables/FinalSummary";
import RuleTenEleven from "@/components/tournament_office/round/reports/evaluation_of_final/tables/RuleTenEleven";
export default {
  components: { RuleTenEleven, FinalSummary },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} }
  }
};
</script>
