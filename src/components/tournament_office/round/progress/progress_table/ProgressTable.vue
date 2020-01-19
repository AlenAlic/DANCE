<template>
  <v-card v-if="round">
    <v-card-title v-if="round.competition.mode !== $constants.CHANGE_PER_DANCE">
      {{ round.competition.name }} ({{ round.mode }}) / {{ round.name }} ({{ competitors.length }})
    </v-card-title>
    <v-card-title v-else>
      {{ round.competition.name }} ({{ round.mode }}) / {{ round.name }} ({{ leads.length }})
    </v-card-title>
    <v-card-text v-if="loading">
      <v-progress-linear indeterminate />
    </v-card-text>
    <v-card-text v-else>
      <progress-table-couple
        v-if="round.competition.mode !== $constants.CHANGE_PER_DANCE"
        :round="round"
        :data="data"
        :competitors="competitors"
      />
      <progress-table-dancer v-else :round="round" :data="data" :leads="leads" :follows="follows" />
    </v-card-text>
  </v-card>
</template>

<script>
import ProgressTableCouple from "@/components/tournament_office/round/progress/progress_table/ProgressTableCouple";
import ProgressTableDancer from "@/components/tournament_office/round/progress/progress_table/ProgressTableDancer";
export default {
  components: { ProgressTableDancer, ProgressTableCouple },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} },
    competitors: { type: Array, default: () => [] },
    leads: { type: Array, default: () => [] },
    follows: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false }
  },
  data: function() {
    return {
      ids: []
    };
  }
};
</script>
