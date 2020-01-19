<template>
  <div class="cell_container">
    <div class="cell number subtitle-2" :class="{ disabled: disabled }">
      <b>{{ number }}</b>
    </div>
    <div class="cell" :class="{ disabled: disabled }">
      <input type="number" v-model="final_placing" @change="handleInput" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    id: { type: Number, default: null },
    number: { type: Number, default: null },
    placing: { type: Array, default: () => [] },
    data: { type: Number, default: 0 },
    disabled: { type: Boolean, default: true }
  },
  model: {
    prop: "placing",
    event: "placing"
  },
  data: function() {
    return {
      final_placing: this.data
    };
  },
  methods: {
    handleInput(e) {
      if (!this.disabled) {
        let input = [...this.placing];
        const value = Number(e.target.value);
        let data = input.find(p => p.final_placing_id === this.id);
        data.final_placing = value;
        this.$emit("placing", input);
      }
    }
  }
};
</script>

<style
  src="../../../../assets/css/components/adjudication-cell/adjudication-cell.scss"
  lang="scss"
></style>
