<template>
  <v-form ref="form" v-model="valid" @submit.prevent="createRound">
    <v-card>
      <v-card-title>
        {{ $t("round.new_round.title") }}
      </v-card-title>
      <v-card-subtitle>
        {{ competition.name }}
      </v-card-subtitle>
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
          <template v-if="this.type !== $constants.FINAL">
            <v-col :cols="competition.floors > 1 ? 6 : 12">
              <v-text-field
                v-model="heats"
                :label="$t('round.new_round.heats.label')"
                :hint="
                  competition.floors > 1
                    ? $t('round.new_round.heats.hint', {
                        heats: heats,
                        couples: couplesPerHeatPerFloor,
                        total: competition.max_couples
                      })
                    : $t('round.new_round.heats.hint_no_floor', {
                        heats: heats,
                        couples: couplesPerHeatPerFloor,
                        total: competition.max_couples
                      })
                "
                persistent-hint
                :rules="[$form.fieldRequired]"
              ></v-text-field>
            </v-col>
            <v-col cols="6" v-if="competition.floors > 1">
              <v-select
                v-model="floors"
                :items="Array.from(Array(competition.floors), (x, i) => i + 1)"
                :label="$t('round.new_round.floors.label')"
                :rules="[$form.fieldRequired]"
              ></v-select>
            </v-col>
            <template v-if="type !== $constants.GENERAL_LOOK">
              <v-col cols="6">
                <v-text-field
                  v-model="min_marks"
                  :label="$t('round.new_round.min_marks.label')"
                  :hint="floors > 1 ? $t('round.new_round.min_marks.hint_multiple_floors') : ''"
                  :persistent-hint="floors > 1"
                  :rules="[$form.fieldRequired, $form.min(1), $form.max(competition.max_couples)]"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="max_marks"
                  :label="$t('round.new_round.max_marks.label')"
                  :hint="floors > 1 ? $t('round.new_round.max_marks.hint_multiple_floors') : ''"
                  :persistent-hint="floors > 1"
                  :rules="[$form.fieldRequired, $form.min(1), $form.max(competition.max_couples)]"
                ></v-text-field>
              </v-col>
            </template>
          </template>
          <v-col cols="12">
            <v-select
              v-model="dances"
              :items="competition.discipline.dances"
              :label="$t('round.new_round.dances.label')"
              persistent-hint
              :rules="[$form.fieldRequired]"
              item-value="dance_id"
              item-text="name"
              multiple
              chips
            ></v-select>
          </v-col>
          <template v-if="this.type !== $constants.FINAL && this.heats > 1">
            <v-col cols="12">
              <v-checkbox
                v-model="different_heats"
                :label="$t('round.new_round.different_heats.label')"
                hide-details
              ></v-checkbox>
            </v-col>
          </template>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
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
import { SOND } from "@/constants";
export default {
  props: {
    competition: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      type: this.competition.is_quali ? this.$constants.QUALIFICATION : null,
      heats: 1,
      floors: 1,
      min_marks: 1,
      max_marks: 1,
      different_heats: this.$store.state.config.config.tournament !== SOND,
      dances: this.getDances()
    };
  },
  computed: {
    getRoundTypes() {
      const types = this.$store.state.config.config.round_types_filter;
      if (this.competition.is_quali) {
        return types[2];
      } else if (!this.competition.last_round) {
        return types[1];
      } else if (this.competition.rounds.length === 1) {
        return types[3];
      }
      return this.$store.state.config.config.round_types;
    },
    couplesPerHeatPerFloor() {
      return Math.round(this.competition.max_couples / this.heats / this.floors);
    }
  },
  methods: {
    createRound() {
      this.loading = true;
      Vue.axios
        .post(`competition/${this.$route.params.competition_id}/round`, {
          type: this.type,
          dancing_class: this.dancing_class,
          heats: this.heats,
          floors: this.floors,
          min_marks: this.min_marks,
          max_marks: this.max_marks,
          dances: this.dances,
          different_heats: this.different_heats
        })
        .then(response => {
          const competition = response.data;
          this.$emit("updated", competition);
          store.commit(UPDATE_COMPETITION, competition);
          this.$router.push({
            name: "tournament_office.round.progress",
            params: { round_id: competition.last_round.round_id }
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getDances() {
      if (!this.competition.last_round) {
        return this.$store.state.config.config.base_dances[this.competition.discipline.name].map(
          d => d.dance_id
        );
      } else {
        return this.competition.dances.map(d => d.dance_id);
      }
    },
    resetForm() {
      this.type = null;
      this.heats = 1;
      this.floors = 1;
      this.min_marks = 1;
      this.max_marks = 1;
      this.different_heats = this.$store.state.config.config.tournament !== SOND;
      this.dances = this.getDances();
    }
  }
};
</script>
