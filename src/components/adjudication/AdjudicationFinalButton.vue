<template>
  <v-btn
    color="primary"
    :outlined="value !== placing.final_placing_id"
    @click="$emit('input', placing.final_placing_id)"
    :disabled="disabled"
  >
    {{ number }}
  </v-btn>
</template>

<script>
export default {
  props: {
    value: { type: Number, default: 0 },
    adjudicator: { type: Object, default: () => {} },
    placing: { type: Object, default: () => {} },
    disabled: { type: Boolean, default: true }
  },
  data: function() {
    return {
      loading: false
    };
  },
  computed: {
    number() {
      return this.adjudicator.assignment === this.$constants.ADJUDICATION_FOLLOW
        ? this.placing.follow_number
        : this.placing.number;
    }
  }
};
</script>
