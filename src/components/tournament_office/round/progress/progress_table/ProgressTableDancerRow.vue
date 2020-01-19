<template>
  <tr>
    <td>{{ dancer.number }}</td>
    <td>{{ follows ? null : dancer.name }}</td>
    <td>{{ follows ? dancer.name : null }}</td>
    <td>{{ dancer.team }}</td>
    <template v-if="round.type !== $constants.FINAL && round.number_of_heats > 1">
      <td v-for="dance in round.dances" :key="dance.dance_id">
        {{ data[dance.dance_id][dancer.number] }}
      </td>
    </template>
  </tr>
</template>

<script>
export default {
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} },
    dancer: { type: Object, default: () => {} },
    follows: { type: Boolean, default: false }
  }
};
</script>
