<template>
  <div class="title-box">
    <v-card-title class="pt-2" v-if="!!round">
      {{ round.competition.name }} {{ round.name }}
    </v-card-title>
    <v-card-title class="pt-2" v-else>{{ competition.name }}</v-card-title>
    <v-card-subtitle class="pb-2">
      <div class="font-weight-bold">{{ title }}</div>
      <div v-if="!!subtitle">{{ subtitle }}</div>
    </v-card-subtitle>
  </div>
</template>

<script>
export default {
  props: {
    competition: { type: Object, default: () => {} },
    round: { type: Object, default: () => {} },
    title: { type: String, default: "" },
    subtitle: { type: String, default: "" }
  }
};
</script>
