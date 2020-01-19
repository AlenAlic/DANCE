<template>
  <thead>
    <tr>
      <th class="text-left font-weight-black subtitle-1">
        {{ $t("round.progress.header.number") }}
      </th>
      <th class="text-left font-weight-black subtitle-1">
        {{ $t("round.progress.header.lead") }}
      </th>
      <th class="text-left font-weight-black subtitle-1">
        {{ $t("round.progress.header.follow") }}
      </th>
      <th class="text-left font-weight-black subtitle-1">
        {{ $t("round.progress.header.teams") }}
      </th>
      <template v-if="round.type !== $constants.FINAL && round.number_of_heats > 1">
        <th
          class="text-left font-weight-black subtitle-1"
          v-for="dance in round.dances"
          :key="dance.dance_id"
        >
          {{ dance.tag }}
        </th>
      </template>
    </tr>
  </thead>
</template>

<script>
export default {
  props: {
    round: { type: Object, default: () => {} }
  }
};
</script>
