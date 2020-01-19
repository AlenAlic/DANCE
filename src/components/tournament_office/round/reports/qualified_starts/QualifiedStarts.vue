<template>
  <v-card flat class="report">
    <table class="pt-1">
      <thead>
        <tr>
          <th colspan="4">
            <title-box
              :round="round"
              :competition="competition"
              :title="title"
              :subtitle="
                !changePartnerMode
                  ? $t('round.reports.subtitles.couples_starting', { num: competitors.length })
                  : $t('round.reports.subtitles.dancers_starting', {
                      leads: leads.length,
                      follows: follows.length
                    })
              "
            />
          </th>
        </tr>
      </thead>
      <tbody v-if="!changePartnerMode">
        <qualified-starts-header-row />
        <tr class="grey-separator" v-for="couple in competitors" :key="couple.couple_id">
          <td>{{ couple.number }}</td>
          <td>{{ couple.lead.name }}</td>
          <td>{{ couple.follow.name }}</td>
          <td>{{ couple.team }}</td>
        </tr>
      </tbody>
      <tbody v-else>
        <qualified-starts-header-row />
        <qualified-starts-dancer-row
          v-for="dancer in leads"
          :key="dancer.dancer_id"
          :dancer="dancer"
        />
        <qualified-starts-dancer-row
          v-for="dancer in follows"
          follows
          :key="dancer.dancer_id"
          :dancer="dancer"
        />
      </tbody>
    </table>
  </v-card>
</template>

<script>
import TitleBox from "@/components/tournament_office/round/reports/TitleBox";
import QualifiedStartsHeaderRow from "@/components/tournament_office/round/reports/qualified_starts/QualifiedStartsHeaderRow";
import QualifiedStartsDancerRow from "@/components/tournament_office/round/reports/qualified_starts/QualifiedStartsDancerRow";
export default {
  components: { QualifiedStartsHeaderRow, QualifiedStartsDancerRow, TitleBox },
  props: {
    competition: { type: Object, default: () => {} },
    round: { type: Object, default: () => {} },
    competitors: { type: Array, default: () => [] },
    leads: { type: Array, default: () => [] },
    follows: { type: Array, default: () => [] },
    reDance: { type: Boolean, default: false },
    changePartnerMode: { type: Boolean, default: false }
  },
  computed: {
    title() {
      return this.reDance
        ? this.$t(`round.reports.labels.${this.$constants.NO_RE_DANCE}`)
        : this.$t(`round.reports.labels.${this.$constants.QUALIFIED_STARTS}`);
    }
  }
};
</script>
