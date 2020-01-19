<template>
  <div class="table-skating-wrapper">
    <table class="table-skating table-skating--light">
      <tbody>
        <tr class="dance-col">
          <th colspan="4" class="text-left pl-1">{{ round.round.name }}</th>
        </tr>
        <competition-listing-header-row />
        <tr v-for="result in round.results" :key="result.name">
          <td class="highlighted-col">{{ result.rank }}</td>
          <td class="highlighted-col">{{ result.number }}</td>
          <td class="text-left pl-1">{{ result.name }}</td>
          <td class="text-left pl-1">{{ result.team }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import CompetitionListingHeaderRow from "@/components/public/results/competition_listing/CompetitionListingHeaderRow";
export default {
  props: {
    round: { type: Object, default: () => null }
  },
  components: { CompetitionListingHeaderRow }
};
</script>
