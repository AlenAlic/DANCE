<template>
  <v-card-text v-if="loading">
    <v-progress-linear indeterminate />
  </v-card-text>
  <v-expansion-panels v-else multiple accordion>
    <results-panel :round="round" v-if="round.type === $constants.FINAL && round.completed" />
    <adjudicator-panel :round="round" />
    <start-list-panel :round="round" />
    <no-re-dance-panel :round="round" v-if="round.type === $constants.RE_DANCE" />
    <couples-present-panel
      :round="round"
      @updated="emitRound"
      v-if="round.type !== $constants.FINAL"
    />
  </v-expansion-panels>
</template>

<script>
import AdjudicatorPanel from "@/components/presenter/panels/AdjudicatorPanel";
import StartListPanel from "@/components/presenter/panels/StartListPanel";
import CouplesPresentPanel from "@/components/presenter/panels/CouplesPresentPanel";
import NoReDancePanel from "@/components/presenter/panels/NoReDancePanel";
import ResultsPanel from "@/components/presenter/panels/ResultsPanel";
export default {
  components: {
    ResultsPanel,
    NoReDancePanel,
    CouplesPresentPanel,
    StartListPanel,
    AdjudicatorPanel
  },
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      adjudicatorsLoading: false,
      floorLoading: false,
      adjudicatorsInterval: null,
      floorInterval: null
    };
  },
  // created() {
  //   this.getData();
  // },
  methods: {
    emitRound(r) {
      this.$emit("updated", r);
    }
  }
};
</script>
