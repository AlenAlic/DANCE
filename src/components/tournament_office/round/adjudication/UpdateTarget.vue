<template>
  <v-card>
    <v-card-title>
      {{ $t("round.adjudication.update_target.modal.title") }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="6">
          <v-text-field
            v-model="min_marks"
            :label="$t('round.adjudication.update_target.modal.min_marks.label')"
            :hint="
              round.floors.length > 1
                ? $t('round.adjudication.update_target.modal.min_marks.hint_multiple_floors')
                : ''
            "
            :persistent-hint="round.floors.length > 1"
            :rules="[$form.fieldRequired, $form.min(1), $form.max(round.number_of_couples)]"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="max_marks"
            :label="$t('round.adjudication.update_target.modal.max_marks.label')"
            :hint="
              round.floors.length > 1
                ? $t('round.adjudication.update_target.modal.max_marks.hint_multiple_floors')
                : ''
            "
            :persistent-hint="round.floors.length > 1"
            :rules="[$form.fieldRequired, $form.min(1), $form.max(round.number_of_couples)]"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="$emit('updated', returnData)">
        {{ $t("round.adjudication.update_target.modal.save") }}
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
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      min_marks: this.round.min_marks,
      max_marks: this.round.max_marks
    };
  },
  computed: {
    returnData() {
      return {
        min_marks: this.min_marks,
        max_marks: this.max_marks
      };
    }
  }
};
</script>
