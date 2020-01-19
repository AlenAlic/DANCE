<template>
  <table>
    <thead>
      <tr>
        <th class="text-start mr-4">
          <span class="mr-4">
            {{ $t("round.adjudication.adjudicator") }}
          </span>
        </th>
        <th class="text-start">
          {{ $t("round.adjudication.placings") }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="d in data" :key="d.adjudicator.adjudicator_id">
        <td>
          <span class="mr-4">{{ d.adjudicator.name }}</span>
        </td>
        <td>
          <span class="mr-4">{{ checkPlacings(d.placings) }}</span>
          <v-icon v-if="checkComplete(d.placings)">
            mdi-check-circle-outline
          </v-icon>
          <v-icon v-else>mdi-minus-circle-outline</v-icon>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  props: {
    data: { type: Array, default: () => [] }
  },
  methods: {
    getSet(placings) {
      return [...new Set(placings.map(p => p.final_placing))].filter(p => p > 0);
    },
    checkPlacings(placings) {
      const placements = this.getSet(placings).length;
      const couples = placings.length;
      return `${placements}/${couples}`;
    },
    checkComplete(placings) {
      const couples = placings.length;
      return couples > 0 && this.getSet(placings).length === couples;
    }
  }
};
</script>
