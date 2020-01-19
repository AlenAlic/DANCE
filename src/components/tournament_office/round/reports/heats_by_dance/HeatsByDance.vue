<template>
  <v-card flat class="report">
    <table class="pt-1">
      <thead>
        <tr>
          <th colspan="2">
            <title-box
              v-if="round.competition.mode !== $constants.CHANGE_PER_DANCE"
              :round="round"
              :title="$t(`round.reports.labels.${$constants.HEATS_BY_DANCE}`)"
              :subtitle="
                $t('round.reports.subtitles.couples_starting', { num: competitors.length })
              "
            />
            <title-box
              v-else
              :round="round"
              :title="$t(`round.reports.labels.${$constants.HEATS_BY_STARTING_NUMBER}`)"
            />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr class="separator">
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.heat") }}
          </th>
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.dance_couple") }}
          </th>
        </tr>
        <template v-for="dance in round.dances">
          <tr class="grey-separator" :key="dance.dance_id">
            <td></td>
            <td>
              <b>{{ dance.name }}</b>
            </td>
          </tr>
          <template v-if="round.competition.mode !== $constants.CHANGE_PER_DANCE">
            <template v-for="heat in Object.keys(data[dance.dance_id])">
              <tr class="grey-separator" :key="`${dance.dance_id}-${heat}`">
                <td>
                  <b>{{ heat }}</b>
                </td>
                <td>
                  <span
                    class="number"
                    v-for="couple in data[dance.dance_id][heat]"
                    :key="couple.number"
                  >
                    {{ couple.number }}
                  </span>
                </td>
              </tr>
            </template>
          </template>
          <template v-else>
            <template v-for="heat in Object.keys(data[dance.dance_id])">
              <tr class="grey-separator" :key="`${dance.dance_id}-${heat}`">
                <td>
                  <b>{{ heat }}</b>
                </td>
                <td>
                  <div
                    class="number partner"
                    v-for="dancer in data[dance.dance_id][heat]"
                    :key="dancer.number"
                  >
                    <b>{{ dancer.number }}:</b>
                    <span> {{ partnerMapping[dance.dance_id][dancer.number] }}</span>
                  </div>
                </td>
              </tr>
            </template>
          </template>
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
    data: { type: Object, default: () => {} },
    competitors: { type: Array, default: () => [] },
    partnerMapping: { type: Object, default: () => {} }
  }
};
</script>

<style scoped lang="scss">
.number {
  display: inline-block;
  width: 2.5rem;
  text-align: left;

  &.partner {
    b {
      width: 2.5rem;
      display: inline-block;
      text-align: right;
    }
    width: 6rem;
  }
}
</style>
