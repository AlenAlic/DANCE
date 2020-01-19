<template>
  <v-card flat class="report">
    <v-row no-gutters>
      <v-col cols="12">
        <title-box :round="round" :title="title" />
      </v-col>
      <v-col cols="12">
        <final-summary :round="round" :results="data.summary" :numbers="data.numbers" />
      </v-col>
      <v-col v-if="data.rule10.length > 0" cols="12">
        <rule-ten-eleven
          :round="round"
          :results="data.rule10"
          :numbers="data.numbers"
          :title="$t('round.reports.final_evaluation.rule10')"
        />
      </v-col>
      <v-col v-if="data.rule11.length > 0" cols="12">
        <rule-ten-eleven
          :round="round"
          :results="data.rule11"
          :numbers="data.numbers"
          :title="$t('round.reports.final_evaluation.rule11')"
        />
      </v-col>
      <v-col v-for="dance in round.dances" :key="dance.dance_id" cols="12">
        <skating-dance
          :round="round"
          :dance="dance"
          :adjudicators="data.adjudicators"
          :results="data.dances[dance.dance_id]"
        />
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import FinalSummary from "@/components/tournament_office/round/reports/evaluation_of_final/tables/FinalSummary";
import RuleTenEleven from "@/components/tournament_office/round/reports/evaluation_of_final/tables/RuleTenEleven";
import SkatingDance from "@/components/tournament_office/round/reports/evaluation_of_final/tables/SkatingDance";
import TitleBox from "@/components/tournament_office/round/reports/TitleBox";
export default {
  components: { TitleBox, SkatingDance, RuleTenEleven, FinalSummary },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} },
    title: { type: String, default: "" }
  }
};
</script>
