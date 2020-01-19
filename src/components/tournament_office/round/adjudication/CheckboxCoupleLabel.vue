<template>
  <div v-if="couple">
    <span class="number" :class="{ large: large }">{{ couple.number }}</span>
    <span>{{ couple.name }}</span>
  </div>
</template>

<script>
export default {
  props: {
    couple: { type: Object, default: () => null },
    large: { type: Boolean, default: false }
  }
};
</script>

<style scoped lang="scss">
.number {
  width: 2.5rem;
  text-align: right;
  display: inline-block;
  margin-right: 1rem;

  &.large {
    width: 5.5rem;
  }
}
</style>
