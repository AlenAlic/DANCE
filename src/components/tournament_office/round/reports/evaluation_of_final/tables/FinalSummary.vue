<template>
  <div class="no-page-break table-skating-wrapper">
    <table class="table-sm table-skating print-friendly" :class="{ 'table-skating--light': light }">
      <thead class="text-center">
        <tr>
          <th :colspan="round.dances.length + 3">
            {{ round.competition.name }} {{ $t("round.reports.final_evaluation.summary") }}
          </th>
        </tr>
        <tr>
          <th rowspan="2" class="table-skating--bottom number">
            {{ $t("round.reports.final_evaluation.number") }}
          </th>
          <th :colspan="round.dances.length">
            {{ $t("round.reports.final_evaluation.dances") }}
          </th>
          <th rowspan="2" class="table-skating--bottom result">
            {{ $t("round.reports.final_evaluation.total") }}
          </th>
          <th rowspan="2" class="table-skating--bottom result">
            {{ $t("round.reports.final_evaluation.result") }}
          </th>
        </tr>
        <tr>
          <th v-for="dance in round.dances" :key="dance.dance_id" class="dance">
            {{ dance.tag }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in results" :key="i">
          <td v-for="(col, j) in row" :key="`${i}-${j}`">
            <v-tooltip right color="primary" dark v-if="j === 0">
              <template v-slot:activator="{ on }">
                <span v-on="on" class="is-clickable">{{ col }}</span>
              </template>
              <span>{{ numbers[col] }}</span>
            </v-tooltip>
            <span v-else>{{ col }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    round: { type: Object, default: () => {} },
    results: { type: Array, default: () => [] },
    numbers: { type: Object, default: () => {} },
    title: { type: String, default: "" },
    light: { type: Boolean, default: false }
  }
};
</script>

<style
  src="../../../../../../assets/css/components/table-skating/table-skating.scss"
  lang="scss"
></style>
