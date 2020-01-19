<template>
  <tr class="grey-separator">
    <td>{{ dancer.number }}</td>
    <td>{{ follows ? null : dancer.name }}</td>
    <td>{{ follows ? dancer.name : null }}</td>
    <td>{{ dancer.team }}</td>
  </tr>
</template>

<script>
export default {
  props: {
    dancer: { type: Object, default: () => {} },
    follows: { type: Boolean, default: false }
  }
};
</script>
