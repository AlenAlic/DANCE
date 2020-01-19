<template>
  <v-simple-table dense>
    <template v-slot:default>
      <progress-table-head :round="round" />
      <progress-table-couple-body :round="round" :data="data" :competitors="competitors" />
    </template>
  </v-simple-table>
</template>

<script>
import ProgressTableCoupleBody from "@/components/tournament_office/round/progress/progress_table/ProgressTableCoupleBody";
import ProgressTableHead from "@/components/tournament_office/round/progress/progress_table/ProgressTableHead";
export default {
  components: { ProgressTableHead, ProgressTableCoupleBody },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} },
    competitors: { type: Array, default: () => [] }
  }
};
</script>
