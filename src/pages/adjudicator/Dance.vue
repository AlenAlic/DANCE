<template>
  <v-card flat class="fill-height" v-if="!!adjudication">
    <template v-if="!adjudication.loading">
      <template v-if="adjudication.round.type === $constants.FINAL">
        <v-subheader class="justify-center">
          {{ adjudication.round.competition.name }}
        </v-subheader>
        <v-card flat>
          <v-card-text v-if="!!adjudication.adjudicator">
            <adjudication-final
              :adjudication="adjudication"
              :disabled="!adjudication.dance.is_active"
            />
          </v-card-text>
        </v-card>
      </template>
      <template v-else>
        <v-subheader class="justify-center">
          {{ adjudication.round.competition.name }} {{ adjudication.round.name }}
        </v-subheader>
        <v-card flat v-for="heat in Object.keys(adjudication.marks)" :key="heat">
          <v-card-title>{{ $t("adjudicator.heat") }} {{ heat }}</v-card-title>
          <v-card-text v-if="!!adjudication.adjudicator">
            <v-row no-gutters>
              <adjudication-cell
                v-for="m in followSort(adjudication.marks[heat])"
                :key="m.mark_id"
                :adjudicator="adjudication.adjudicator"
                :mark="m"
                :disabled="!adjudication.dance.is_active"
              />
            </v-row>
          </v-card-text>
        </v-card>
      </template>
    </template>
    <loading v-else />
  </v-card>
</template>

<script>
import Loading from "@/components/general/loading/Loading";
import store from "@/store";
import { ADJUDICATION } from "@/store/modules/adjudication";
import AdjudicationCell from "@/components/adjudication/AdjudicationCell";
import AdjudicationFinal from "@/components/adjudication/AdjudicationFinal";
export default {
  components: { AdjudicationFinal, AdjudicationCell, Loading },
  created() {
    store.dispatch(ADJUDICATION, {
      round_id: this.$route.params.round_id,
      dance_id: this.$route.params.dance_id
    });
  },
  computed: {
    adjudication() {
      return this.$store.state.adjudication;
    }
  },
  methods: {
    followSort(marks) {
      if (this.adjudication.adjudicator.assignment === this.$constants.ADJUDICATION_FOLLOW) {
        const sortedMarks = [...marks];
        return sortedMarks.sort((a, b) => a.follow_number - b.follow_number);
      } else {
        return marks;
      }
    }
  }
};
</script>
