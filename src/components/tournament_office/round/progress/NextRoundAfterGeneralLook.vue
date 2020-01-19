<template>
  <v-form class="mb-5" ref="form" v-model="valid" @submit.prevent="createRound">
    <v-card>
      <v-card-title>
        {{ $t("round.progress.next_round_after_general_look.title") }}
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-select
              v-model="type"
              :items="getRoundTypes"
              :label="$t('round.new_round.round_types.label')"
              :rules="[$form.fieldRequired]"
              item-text="name"
            ></v-select>
          </v-col>
          <template v-if="type !== $constants.FINAL">
            <v-col cols="6">
              <v-text-field
                v-model="min_marks"
                :label="$t('round.new_round.min_marks.label')"
                :rules="[$form.fieldRequired, $form.min(1), $form.max(round.number_of_couples)]"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="max_marks"
                :label="$t('round.new_round.max_marks.label')"
                :rules="[$form.fieldRequired, $form.min(1), $form.max(round.number_of_couples)]"
              ></v-text-field>
            </v-col>
            <v-col cols="12" v-if="round.number_of_heats > 1">
              <v-checkbox
                v-model="same_heats"
                :label="$t('round.progress.next_round_after_general_look.same_heats.label')"
                hide-details
              ></v-checkbox>
            </v-col>
          </template>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          :disabled="!valid || computedLoading"
          :loading="computedLoading"
          color="primary"
          text
          type="submit"
        >
          {{ $t("round.new_round.submit") }}
        </v-btn>
        <v-btn text @click="resetForm">
          {{ $t("general.cancel") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { UPDATE_COMPETITION } from "@/store/modules/competitions";
export default {
  props: {
    round: { type: Object, default: () => {} },
    progressLoading: { type: Boolean, default: false }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      type: null,
      min_marks: this.round.min_marks,
      max_marks: this.round.max_marks,
      same_heats: false
    };
  },
  computed: {
    computedLoading() {
      return this.loading || this.progressLoading;
    },
    getRoundTypes() {
      const types = this.$store.state.config.config.round_types_filter;
      return types[9];
    }
  },
  methods: {
    createRound() {
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/progress`, {
          type: this.type,
          min_marks: this.min_marks,
          max_marks: this.max_marks,
          same_heats: this.same_heats
        })
        .then(response => {
          const round = response.data.round;
          store.commit(UPDATE_COMPETITION, response.data.competition);
          if (round.round_id !== this.$route.params.round_id) {
            this.$router.push({
              name: "tournament_office.round.progress",
              params: { round_id: round.round_id }
            });
          } else {
            this.$emit("updated", round);
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    resetForm() {
      this.type = null;
      this.min_marks = this.round.min_marks;
      this.max_marks = this.round.max_marks;
      this.same_heats = false;
      this.$refs.form.resetValidation();
    }
  }
};
</script>
