<template>
  <div class="no-page-break table-skating-wrapper">
    <table class="table-sm table-skating print-friendly" :class="{ 'table-skating--light': light }">
      <thead class="text-center">
        <tr>
          <th rowspan="3" class="table-skating--bottom number">
            {{ $t("round.reports.final_evaluation.number") }}
          </th>
          <th :colspan="round.number_of_couples + adjudicators.length">
            {{ dance.name }}
          </th>
          <th rowspan="3" class="table-skating--bottom result">
            {{ $t("round.reports.final_evaluation.result") }}
          </th>
        </tr>
        <tr>
          <th :colspan="adjudicators.length">
            {{ $t("round.reports.final_evaluation.adjudicators") }}
          </th>
          <th :colspan="round.number_of_couples">
            {{ $t("round.reports.final_evaluation.places") }}
          </th>
        </tr>
        <tr>
          <th v-for="adj in adjudicators" :key="`adj-${adj.adjudicator_id}`" class="adjudicator">
            {{ adj.tag }}
          </th>
          <th
            v-for="place in Array.from(Array(round.number_of_couples).keys()).map(x => x + 1)"
            :key="`place-${place}`"
            class="placing"
          >
            1{{ place > 1 ? `-${place}` : "" }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in results" :key="i">
          <td v-for="(col, j) in row" :key="`${i}-${j}`">{{ col }}</td>
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
    dance: { type: Object, default: () => {} },
    adjudicators: { type: Array, default: () => [] },
    light: { type: Boolean, default: false }
  }
};
</script>

<style
  src="../../../../../../assets/css/components/table-skating/table-skating.scss"
  lang="scss"
></style>
