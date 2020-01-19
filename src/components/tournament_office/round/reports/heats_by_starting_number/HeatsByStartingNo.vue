<template>
  <v-card flat class="report">
    <table class="pt-1">
      <thead>
        <tr>
          <th :colspan="round.dances.length + 1">
            <title-box
              v-if="!changePartnerMode"
              :round="round"
              :competition="competition"
              :title="$t(`round.reports.labels.${$constants.HEATS_BY_STARTING_NUMBER}`)"
              :subtitle="
                $t('round.reports.subtitles.couples_starting', { num: competitors.length })
              "
            />
            <title-box
              v-else
              :round="round"
              :competition="competition"
              :title="$t(`round.reports.labels.${$constants.HEATS_BY_STARTING_NUMBER}`)"
            />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr class="separator">
          <th class="text-left font-weight-black subtitle-1">#</th>
          <th
            class="text-left font-weight-black subtitle-1"
            v-for="dance in round.dances"
            :key="dance.dance_id"
          >
            {{ dance.tag }}
          </th>
        </tr>
        <template v-if="!changePartnerMode">
          <tr class="grey-separator" v-for="couple in competitors" :key="couple.couple_id">
            <td>{{ couple.number }}</td>
            <td v-for="dance in round.dances" :key="dance.dance_id">
              {{ data[dance.dance_id][couple.number] }}
            </td>
          </tr>
        </template>
        <template v-else>
          <tr class="grey-separator" v-for="dancer in dancers" :key="dancer.dancer_id">
            <td>{{ dancer.number }}</td>
            <td v-for="dance in round.dances" :key="dance.dance_id">
              <b>{{ data[dance.dance_id][dancer.number] }}: </b>
              <span>{{ partnerMapping[dance.dance_id][dancer.number] }}</span>
            </td>
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
    competition: { type: Object, default: () => {} },
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} },
    competitors: { type: Array, default: () => [] },
    leads: { type: Array, default: () => [] },
    follows: { type: Array, default: () => [] },
    partnerMapping: { type: Object, default: () => {} },
    changePartnerMode: { type: Boolean, default: false }
  },
  computed: {
    dancers() {
      if (this.changePartnerMode) {
        return [...this.leads, ...this.follows].sort((a, b) => {
          return a.number - b.number;
        });
      }
      return [];
    }
  }
};
</script>
