<template>
  <v-card flat class="report">
    <table class="pt-1">
      <thead>
        <tr>
          <th>
            <title-box
              v-if="round.type === $constants.FINAL"
              :round="round"
              :title="adjudicator.name"
            />
            <title-box
              v-else
              :round="round"
              :title="adjudicator.name"
              :subtitle="$t('round.reports.subtitles.target_marks', { marks: targetMarks })"
            />
          </th>
        </tr>
      </thead>
      <tbody v-if="round.type === $constants.FINAL">
        <tr v-for="dance in round.dances" :key="dance.dance_id">
          <td>
            <div class="subtitle-1 pl-1">
              <b>{{ dance.name }}</b>
            </div>
            <v-row no-gutters>
              <adjudication-cell
                v-for="couple in data[dance.dance_id]"
                :key="`${dance.dance_id}-${couple.number}`"
                :disabled="false"
                :mark="couple"
                :adjudicator="adjudicator"
              />
            </v-row>
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr v-for="dance in round.dances" :key="dance.dance_id">
          <td>
            <div
              v-for="heat in Object.keys(data[dance.dance_id])"
              :key="`${dance.dance_id}-${heat}`"
            >
              <div class="subtitle-1 pl-1">
                <b>{{ $t("round.reports.header.heat") }} {{ heat }} - {{ dance.name }}</b>
              </div>
              <v-row no-gutters>
                <adjudication-cell
                  v-for="mark in followSort(data[dance.dance_id][heat])"
                  :key="`${dance.dance_id}-${heat}-${mark.number}`"
                  :disabled="false"
                  :mark="mark"
                  :adjudicator="adjudicator"
                />
              </v-row>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </v-card>
</template>

<script>
import TitleBox from "@/components/tournament_office/round/reports/TitleBox";
import AdjudicationCell from "@/components/tournament_office/round/adjudication/AdjudicationCell";
export default {
  components: { AdjudicationCell, TitleBox },
  props: {
    round: { type: Object, default: () => {} },
    adjudicator: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} }
  },
  computed: {
    targetMarks() {
      const r = this.round;
      return r && r.min_marks === r.max_marks ? r.min_marks : `${r.min_marks} - ${r.max_marks}`;
    }
  },
  methods: {
    followSort(marks) {
      if (this.adjudicator.assignment === this.$constants.ADJUDICATION_FOLLOW) {
        const sortedMarks = [...marks];
        return sortedMarks.sort((a, b) => a.follow_number - b.follow_number);
      } else {
        return marks;
      }
    }
  }
};
</script>
