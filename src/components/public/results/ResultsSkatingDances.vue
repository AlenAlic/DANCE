<template>
  <div class="no-page-break table-skating-wrapper">
    <table class="table-sm table-skating table-skating--light print-friendly">
      <thead class="text-center highlighted-col">
        <tr>
          <th rowspan="2" class="table-skating--bottom number">
            {{ $t("round.reports.final_evaluation.number") }}
          </th>
          <th :colspan="adjudicators.length">
            {{ $t("round.reports.final_evaluation.adjudicators") }}
          </th>
          <th :colspan="round.number_of_couples">
            {{ $t("round.reports.final_evaluation.places") }}
          </th>
          <th rowspan="2" class="table-skating--bottom result">
            {{ $t("round.reports.final_evaluation.result") }}
          </th>
        </tr>
        <tr>
          <th v-for="adj in adjudicators" :key="`adj-${adj.adjudicator_id}`" class="adjudicator">
            <v-tooltip bottom color="primary" dark>
              <template v-slot:activator="{ on }">
                <span v-on="on" class="is-clickable">{{ adj.tag }}</span>
              </template>
              <span>{{ adj.name }}</span>
            </v-tooltip>
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
      <tbody v-for="dance in round.dances" :key="dance.dance_id">
        <tr>
          <th></th>
          <th :colspan="adjudicators.length" class="dance-col">
            {{ dance.name }}
          </th>
          <th :colspan="round.number_of_couples + 1"></th>
        </tr>
        <tr v-for="(row, i) in data[dance.dance_id]" :key="i">
          <td
            v-for="(col, j) in row"
            :key="`${i}-${j}`"
            :class="{ 'highlighted-col': j === 0 || j === row.length - 1 }"
          >
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
    adjudicators: { type: Array, default: () => [] },
    numbers: { type: Object, default: () => {} },
    dances: { type: Array, default: () => [] },
    data: { type: Object, default: () => {} }
  }
};
</script>

<style src="../../../assets/css/components/table-skating/table-skating.scss" lang="scss"></style>
