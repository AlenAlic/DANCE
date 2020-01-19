<template>
  <v-card>
    <v-card-title>
      {{ $t("round.adjudication.close_and_evaluate.modal.title") }}
    </v-card-title>
    <v-card-text>
      {{ $t("round.adjudication.close_and_evaluate.modal.text") }}
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="$emit('evaluate')">
        {{ $t("round.adjudication.close_and_evaluate.modal.evaluate") }}
      </v-btn>
      <v-btn text @click="$emit('cancel')">
        {{ $t("general.cancel") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Array, default: () => [] }
  }
};
</script>
