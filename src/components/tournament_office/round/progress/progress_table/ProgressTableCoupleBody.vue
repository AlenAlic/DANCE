<template>
  <tbody>
    <tr v-for="couple in competitors" :key="couple.couple_id">
      <td>{{ couple.number }}</td>
      <td>{{ couple.lead.name }}</td>
      <td>{{ couple.follow.name }}</td>
      <td>{{ couple.team }}</td>
      <template v-if="round.type !== $constants.FINAL && round.number_of_heats > 1">
        <td v-for="dance in round.dances" :key="dance.dance_id">
          {{ data[dance.dance_id][couple.number] }}
        </td>
      </template>
    </tr>
  </tbody>
</template>

<script>
export default {
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Object, default: () => {} },
    competitors: { type: Array, default: () => [] }
  }
};
</script>
