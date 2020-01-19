<template>
  <div class="table-skating-wrapper">
    <table class="table-skating table-skating--light">
      <template v-if="!changePartnerMode">
        <tbody v-for="(round, index) in rounds" :key="round.round.round_id">
          <tr class="dance-col">
            <th colspan="4" class="text-left pl-1">{{ round.round.name }}</th>
          </tr>
          <competition-listing-header-row v-if="index === 0" />
          <tr v-for="result in round.results" :key="result.name">
            <td class="highlighted-col">{{ result.rank }}</td>
            <td class="highlighted-col">{{ result.number }}</td>
            <td class="text-left pl-1">{{ result.name }}</td>
            <td class="text-left pl-1">{{ result.team }}</td>
          </tr>
        </tbody>
      </template>
      <template v-else-if="follows">
        <tbody v-for="(round, index) in rounds" :key="round.round.round_id">
          <tr class="dance-col">
            <th colspan="4" class="text-left pl-1">{{ round.round.name }}</th>
          </tr>
          <competition-listing-header-row v-if="index === 0" change-partner-mode />
          <competition-listing-dancer-row
            v-for="result in round.results"
            :key="result.name"
            :result="result"
          />
        </tbody>
      </template>
      <template v-else>
        <tbody v-for="(round, index) in rounds" :key="round.round.round_id">
          <tr class="dance-col">
            <th colspan="4" class="text-left pl-1">{{ round.round.name }}</th>
          </tr>
          <competition-listing-header-row v-if="index === 0" change-partner-mode />
          <competition-listing-dancer-row
            v-for="result in round.results"
            :key="result.name"
            :result="result"
          />
        </tbody>
      </template>
    </table>
  </div>
</template>

<script>
import CompetitionListingDancerRow from "@/components/public/results/competition_listing/CompetitionListingDancerRow";
import CompetitionListingHeaderRow from "@/components/public/results/competition_listing/CompetitionListingHeaderRow";
export default {
  components: { CompetitionListingHeaderRow, CompetitionListingDancerRow },
  props: {
    rounds: { type: Array, default: () => [] },
    follows: { type: Boolean, default: false },
    changePartnerMode: { type: Boolean, default: false }
  }
};
</script>
