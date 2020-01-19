<template>
  <v-simple-table dense>
    <template v-slot:default>
      <tbody v-if="!changePartnerMode">
        <qualified-starts-header-row />
        <tr v-for="couple in competitors" :key="couple.couple_id">
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
    </template>
  </v-simple-table>
</template>

<script>
import QualifiedStartsHeaderRow from "@/components/tournament_office/round/reports/qualified_starts/QualifiedStartsHeaderRow";
import QualifiedStartsDancerRow from "@/components/tournament_office/round/reports/qualified_starts/QualifiedStartsDancerRow";
export default {
  components: { QualifiedStartsHeaderRow, QualifiedStartsDancerRow },
  props: {
    competitors: { type: Array, default: () => [] },
    leads: { type: Array, default: () => [] },
    follows: { type: Array, default: () => [] },
    changePartnerMode: { type: Boolean, default: false }
  }
};
</script>
