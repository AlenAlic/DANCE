<template>
  <v-simple-table dense>
    <template v-slot:default>
      <progress-table-head :round="round" />
      <tbody>
        <progress-table-dancer-row
          v-for="dancer in leads"
          :key="dancer.dancer_id"
          :round="round"
          :data="data"
          :dancer="dancer"
        />
        <progress-table-dancer-row
          v-for="dancer in follows"
          :key="dancer.dancer_id"
          :round="round"
          :data="data"
          :dancer="dancer"
          follows
        />
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
import ProgressTableHead from "@/components/tournament_office/round/progress/progress_table/ProgressTableHead";
import ProgressTableDancerRow from "@/components/tournament_office/round/progress/progress_table/ProgressTableDancerRow";
export default {
  components: { ProgressTableDancerRow, ProgressTableHead },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} },
    leads: { type: Array, default: () => [] },
    follows: { type: Array, default: () => [] }
  }
};
</script>
