<template>
  <v-card flat class="report">
    <table class="pt-1">
      <thead>
        <tr>
          <th colspan="2">
            <title-box
              :round="round"
              :title="$t(`round.reports.labels.${$constants.ADJUDICATORS}`)"
            />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr class="separator">
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.name") }}
          </th>
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.tag") }}
          </th>
        </tr>
        <template v-if="round.floors.length > 1">
          <template v-for="floor in round.floors">
            <tr :key="floor">
              <th class="text-left font-weight-black subtitle-2" colspan="2">
                {{ $t("round.reports.header.floor") }} {{ floor }}
              </th>
            </tr>
            <tr v-for="adj in adjudicatorsOnFloor(floor)" :key="`${adj.adjudicator_id}-${floor}`">
              <td>{{ adj.name }}</td>
              <td>{{ adj.tag }}</td>
            </tr>
          </template>
        </template>
        <template v-else>
          <tr v-for="adj in adjudicators" :key="adj.adjudicator_id">
            <td>{{ adj.name }}</td>
            <td>{{ adj.tag }}</td>
          </tr>
        </template>
      </tbody>
    </table>
  </v-card>
</template>

<script>
import TitleBox from "@/components/tournament_office/round/reports/TitleBox";
export default {
  components: { TitleBox },
  props: {
    round: { type: Object, default: () => {} },
    adjudicators: { type: Array, default: () => [] }
  },
  methods: {
    adjudicatorsOnFloor(floor) {
      return this.adjudicators.filter(a => a.floor === floor);
    }
  }
};
</script>
