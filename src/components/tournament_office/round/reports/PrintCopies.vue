<template>
  <v-text-field
    class="print-copies-field"
    type="number"
    v-model="copies"
    :label="$t(`round.reports.copies.label`)"
    @input="handleChange"
  />
</template>

<script>
export default {
  props: {
    id: { type: String, default: null },
    prints: { type: Array, default: () => [] }
  },
  model: {
    prop: "prints",
    event: "prints"
  },
  data: function() {
    return {
      copies: 1
    };
  },
  methods: {
    handleChange() {
      let input = [...this.prints];
      let data = input.find(p => p.id === this.id);
      data.copies = Number(this.copies);
      this.$emit("prints", input);
    }
  }
};
</script>

<style lang="scss">
.print-copies-field {
  max-width: 4rem;
  input[type="number"] {
    text-align: center;
    -moz-appearance: textfield;
  }

  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
}
</style>
