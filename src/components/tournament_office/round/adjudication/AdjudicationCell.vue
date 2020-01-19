<template>
  <div class="cell_container">
    <div class="cell number subtitle-2" :class="{ disabled: disabled }">
      <b>{{ number }}</b>
    </div>
    <div
      class="cell mark"
      :class="{ marked: isMarked, disabled: disabled }"
      @click="handleInput(mark.mark_id)"
    ></div>
  </div>
</template>

<script>
export default {
  props: {
    marked: { type: Array, default: () => [] },
    disabled: { type: Boolean, default: true },
    adjudicator: { type: Object, default: () => {} },
    mark: { type: Object, default: () => {} }
  },
  model: {
    prop: "marked",
    event: "marked"
  },
  methods: {
    handleInput(id) {
      if (!this.disabled) {
        let input = this.marked;
        if (Array.isArray(input)) {
          if (!input.includes(id)) {
            input.push(id);
          } else {
            input.splice(input.indexOf(id), 1);
          }
        } else {
          input = !input;
        }
        this.$emit("marked", input);
      }
    }
  },
  computed: {
    isMarked() {
      return Array.isArray(this.marked) ? this.marked.includes(this.mark.mark_id) : this.marked;
    },
    number() {
      return this.adjudicator.assignment === this.$constants.ADJUDICATION_FOLLOW
        ? this.mark.follow_number
        : this.mark.number;
    }
  }
};
</script>

<style
  src="../../../../assets/css/components/adjudication-cell/adjudication-cell.scss"
  lang="scss"
></style>
