<template>
  <v-card flat class="report">
    <table class="pt-1">
      <thead>
        <tr>
          <th colspan="6">
            <title-box
              :round="round"
              :title="$t(`round.reports.labels.${$constants.PLACINGS_AFTER_ROUND}`)"
            />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr class="separator">
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.number") }}
          </th>
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.placing") }}
          </th>
          <th v-if="round.type !== $constants.FINAL" class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.marks") }}
          </th>
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.lead") }}
          </th>
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.follow") }}
          </th>
          <th class="text-left font-weight-black subtitle-1">
            {{ $t("round.reports.header.teams") }}
          </th>
        </tr>
        <tr class="grey-separator" v-for="result in results" :key="result.round_result_id">
          <td>{{ result.couple.number }}</td>
          <td>{{ result.placing || result.final_placing }}</td>
          <td v-if="round.type !== $constants.FINAL">
            {{ result.marks !== -1 ? result.marks : "-" }}
          </td>
          <td>
            {{
              changePartnerMode
                ? result.follow
                  ? null
                  : result.couple.lead.name
                : result.couple.lead.name
            }}
          </td>
          <td>
            {{
              changePartnerMode
                ? result.follow
                  ? result.couple.follow.name
                  : null
                : result.couple.follow.name
            }}
          </td>
          <td>{{ result.couple.team }}</td>
        </tr>
        <tr
          class="grey-separator grey--text"
          v-for="result in previous_results"
          :key="result.round_result_id"
        >
          <td>{{ result.couple.number }}</td>
          <td>{{ result.placing }}</td>
          <td v-if="round.type !== $constants.FINAL"></td>
          <td>
            {{
              changePartnerMode
                ? result.follow
                  ? null
                  : result.couple.lead.name
                : result.couple.lead.name
            }}
          </td>
          <td>
            {{
              changePartnerMode
                ? result.follow
                  ? result.couple.follow.name
                  : null
                : result.couple.follow.name
            }}
          </td>
          <td>{{ result.couple.team }}</td>
        </tr>
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
    results: { type: Array, default: () => [] },
    previous_results: { type: Array, default: () => [] },
    changePartnerMode: { type: Boolean, default: false }
  }
};
</script>
