<template>
  <results-skating-dances
    :round="round"
    :dances="round.dances"
    :numbers="data.numbers"
    :data="data.dances"
    :adjudicators="data.adjudicators"
  />
</template>

<script>
import ResultsSkatingDances from "@/components/public/results/ResultsSkatingDances";
export default {
  components: { ResultsSkatingDances },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} }
  }
};
</script>
