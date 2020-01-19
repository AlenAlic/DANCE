<template>
  <table v-if="data && round">
    <thead>
      <tr>
        <th class="text-start mr-4">
          <span class="mr-4">
            {{ $t("round.adjudication.adjudicator") }}
          </span>
        </th>
        <th class="text-start">
          <span class="mr-4">
            {{ $t("round.adjudication.marks") }}
          </span>
        </th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="d in data" :key="d.adjudicator.adjudicator_id">
        <td>
          <span class="mr-4">{{ d.adjudicator.name }}</span>
        </td>
        <td>{{ d.marks.length }}</td>
        <td>
          <v-icon class="mr-2" v-if="checkMarks(d.marks)">
            mdi-check-circle-outline
          </v-icon>
          <v-icon class="mr-2" v-else>mdi-minus-circle-outline</v-icon>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Array, default: () => [] }
  },
  model: {
    prop: "round",
    event: "input"
  },
  methods: {
    checkMarks(marks) {
      return marks.length >= this.round.min_marks && this.round.max_marks >= marks.length;
    }
  }
};
</script>
