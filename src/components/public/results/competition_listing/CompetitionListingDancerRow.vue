<template>
  <tr>
    <td class="highlighted-col">{{ result.rank }}</td>
    <td class="highlighted-col">{{ result.number }}</td>
    <td class="text-left pl-1">{{ result.name }}</td>
    <td class="text-left pl-1">{{ result.team }}</td>
  </tr>
</template>

<script>
export default {
  props: {
    result: { type: Object, default: () => {} }
  }
};
</script>
