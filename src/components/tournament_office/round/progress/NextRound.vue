<template>
  <v-row>
    <v-col cols="12" md="8" lg="12" xl="8" v-if="round">
      <v-card>
        <v-card-title>
          {{ round.competition.name }} ({{ round.mode }}) / {{ round.name }}
        </v-card-title>
        <v-card-text v-if="computedLoading">
          <v-progress-linear indeterminate />
        </v-card-text>
        <v-card-text v-else>
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th v-if="showNewRoundForm" class="text-left font-weight-black subtitle-1">
                    Starting
                  </th>
                  <th class="text-left font-weight-black subtitle-1">
                    {{ $t("round.progress.header.number") }}
                  </th>
                  <template v-if="round.type === $constants.FINAL">
                    <th class="text-left font-weight-black subtitle-1">
                      {{ $t("round.progress.header.total") }}
                    </th>
                    <th class="text-left font-weight-black subtitle-1">
                      {{ $t("round.progress.header.result") }}
                    </th>
                  </template>
                  <template v-else>
                    <th class="text-left font-weight-black subtitle-1">
                      {{ $t("round.progress.header.placing") }}
                    </th>
                    <th class="text-left font-weight-black subtitle-1">
                      {{ $t("round.progress.header.marks") }}
                    </th>
                  </template>
                  <th class="text-left font-weight-black subtitle-1">
                    {{ $t("round.progress.header.lead") }}
                  </th>
                  <th class="text-left font-weight-black subtitle-1">
                    {{ $t("round.progress.header.follow") }}
                  </th>
                  <th class="text-left font-weight-black subtitle-1">
                    {{ $t("round.progress.header.teams") }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="result in data"
                  :key="result.round_result_id"
                  :class="{
                    selected:
                      getStarting.map(r => r.round_result_id).includes(result.round_result_id) &&
                      ids.includes(result.round_result_id) &&
                      showNewRoundForm
                  }"
                >
                  <td v-if="showNewRoundForm">
                    <v-checkbox
                      v-model="ids"
                      class="mt-0 mb-1"
                      :value="result.round_result_id"
                      hide-details
                    />
                  </td>
                  <td
                    v-if="round.competition.mode === $constants.CHANGE_PER_DANCE && result.follow"
                  >
                    {{ result.couple.follow.number }}
                  </td>
                  <td v-else>{{ result.couple.lead.number }}</td>
                  <template v-if="round.type === $constants.FINAL">
                    <td>{{ result.total }}</td>
                    <td>{{ result.final_placing }}</td>
                  </template>
                  <template v-else>
                    <td>{{ result.placing }}</td>
                    <td>{{ result.marks !== -1 ? result.marks : "-" }}</td>
                  </template>
                  <template v-if="round.competition.mode === $constants.CHANGE_PER_DANCE">
                    <template v-if="result.follow">
                      <td></td>
                      <td>{{ result.couple.follow.name }}</td>
                    </template>
                    <template v-else>
                      <td>{{ result.couple.lead.name }}</td>
                      <td></td>
                    </template>
                  </template>
                  <template v-else>
                    <td>{{ result.couple.lead.name }}</td>
                    <td>{{ result.couple.follow.name }}</td>
                  </template>
                  <td>{{ result.couple.team }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="4" lg="12" xl="4" v-if="!computedLoading">
      <v-form
        class="mb-5"
        ref="form"
        v-model="valid"
        @submit.prevent="createRound"
        v-if="showNewRoundForm"
      >
        <v-card>
          <v-card-title>
            {{ $t("round.progress.next_round.title") }}
          </v-card-title>
          <v-card-subtitle class="text--wrap">
            {{ $t("round.progress.next_round.subtitle") }}
          </v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-select
                  v-model="type"
                  :items="getRoundTypes"
                  :label="$t('round.new_round.round_types.label')"
                  :hint="
                    type === $constants.RE_DANCE
                      ? $t('round.new_round.round_types.hints.re_dance', { num: noReDanceCouples })
                      : type === $constants.FINAL
                      ? $t('round.new_round.round_types.hints.final', {
                          num: getStarting.length / factor
                        })
                      : ''
                  "
                  persistent-hint
                  :rules="[$form.fieldRequired]"
                  item-text="name"
                ></v-select>
              </v-col>
              <v-col cols="12" v-if="round.type !== $constants.FINAL">
                <v-select
                  v-model="cutoff"
                  :items="cutoffs"
                  :label="$t('round.new_round.cutoff.label')"
                  :hint="$t('round.new_round.cutoff.hint')"
                  persistent-hint
                  :rules="[$form.fieldRequired]"
                ></v-select>
              </v-col>
              <template v-if="this.type !== $constants.FINAL && round.type !== $constants.FINAL">
                <v-col :cols="round.competition.floors > 1 ? 6 : 12">
                  <v-text-field
                    v-model="heats"
                    :label="$t('round.new_round.heats.label')"
                    :hint="
                      round.competition.floors > 1
                        ? $t('round.new_round.heats.hint', {
                            heats: heats,
                            couples: couplesPerHeatPerFloor,
                            total: getStarting.length / factor
                          })
                        : $t('round.new_round.heats.hint_no_floor', {
                            heats: heats,
                            couples: couplesPerHeatPerFloor,
                            total: getStarting.length / factor
                          })
                    "
                    persistent-hint
                    :rules="[$form.fieldRequired]"
                  ></v-text-field>
                </v-col>
                <v-col cols="6" v-if="round.competition.floors > 1">
                  <v-select
                    v-model="floors"
                    :items="Array.from(Array(round.competition.floors), (x, i) => i + 1)"
                    :label="$t('round.new_round.floors.label')"
                    :rules="[$form.fieldRequired]"
                  ></v-select>
                </v-col>
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
              </template>
              <v-col cols="12" v-if="round.type !== $constants.FINAL">
                <v-select
                  v-model="dances"
                  :items="$store.getters.danceMap(round.competition.discipline.discipline_id)"
                  :label="$t('round.new_round.dances.label')"
                  persistent-hint
                  :rules="[$form.fieldRequired]"
                  item-value="dance_id"
                  item-text="name"
                  multiple
                  chips
                ></v-select>
              </v-col>
              <v-col
                cols="12"
                v-if="this.type !== $constants.FINAL && round.type !== $constants.FINAL"
              >
                <v-checkbox
                  v-model="different_heats"
                  :label="$t('round.new_round.different_heats.label')"
                  hide-details
                ></v-checkbox>
              </v-col>
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
              {{ $t("round.progress.next_round.submit") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
      <split-card v-if="showSplitModal" class="mb-5" :round="round" @updated="emitRound" />
      <delete-round-card class="mb-5" :round="round" />
    </v-col>
  </v-row>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { UPDATE_COMPETITION } from "@/store/modules/competitions";
import { EIGHT_FINAL, FINAL, QUARTER_FINAL, RE_DANCE, SEMI_FINAL, SOND } from "@/constants";
import DeleteRoundCard from "@/components/tournament_office/round/progress/DeleteRoundCard";
import SplitCard from "@/components/tournament_office/round/progress/SplitCard";
export default {
  components: { SplitCard, DeleteRoundCard },
  props: {
    round: { type: Object, default: () => {} },
    data: { type: Array, default: () => [] },
    cutoffs: { type: Array, default: () => [] },
    progressLoading: { type: Boolean, default: false }
  },
  data: function() {
    return {
      ids: this.data.map(r => r.round_result_id),
      starting: this.data.map(r => r.round_result_id),
      valid: false,
      loading: false,
      type: this.round.type === this.$constants.FINAL ? this.$constants.FINAL : null,
      cutoff: -1,
      heats: 1,
      floors: 1,
      min_marks: 1,
      max_marks: 1,
      different_heats: this.$store.state.config.config.tournament !== SOND,
      dances: this.round.dances.map(d => d.dance_id)
    };
  },
  computed: {
    changePerDance() {
      return this.round.competition.mode === this.$constants.CHANGE_PER_DANCE;
    },
    computedLoading() {
      return this.loading || this.progressLoading;
    },
    getRoundTypes() {
      const types = this.$store.state.config.config.round_types_filter;
      if (this.round.competition.rounds === 1) {
        return types[3];
      } else if (this.round.type === EIGHT_FINAL) {
        return types[6];
      } else if (this.round.type === QUARTER_FINAL) {
        return types[7];
      } else if (this.round.type === SEMI_FINAL) {
        return types[7];
      } else if (this.round.type === FINAL) {
        return types[8];
      } else {
        return types[4];
      }
    },
    factor() {
      return this.changePerDance ? 2 : 1;
    },
    noReDanceCouples() {
      return this.round ? this.round.number_of_couples - this.getStarting.length / this.factor : 0;
    },
    couplesPerHeatPerFloor() {
      return Math.round(this.getStarting.length / this.heats / this.floors / this.factor);
    },
    getStarting() {
      let data = this.data;
      data = data.filter(r => this.ids.includes(r.round_result_id));
      if (this.cutoff === -1) {
        return data;
      }
      if (this.type === RE_DANCE) {
        return data.filter(r => r.marks < this.cutoff);
      } else {
        return data.filter(r => r.marks >= this.cutoff || r.marks === -1);
      }
    },
    getStartingCouples() {
      return this.getStarting.map(r => r.round_result_id);
    },
    finalNeedsNextRound() {
      return this.round && this.round.type === this.$constants.FINAL
        ? Math.min(...this.data.map(r => r.final_placing)) > 1
        : true;
    },
    showNewRoundForm() {
      return (
        this.round &&
        !this.round.is_active &&
        !this.round.has_next_round &&
        this.finalNeedsNextRound &&
        this.round.type !== this.$constants.QUALIFICATION
      );
    },
    showSplitModal() {
      return (
        this.round &&
        !this.round.is_active &&
        this.round.completed &&
        this.round.type === this.$constants.QUALIFICATION
      );
    }
  },
  methods: {
    createRound() {
      this.loading = true;
      Vue.axios
        .post(`round/${this.$route.params.round_id}/progress`, {
          type: this.type,
          dancing_class: this.dancing_class,
          heats: this.heats,
          floors: this.floors,
          min_marks: this.min_marks,
          max_marks: this.max_marks,
          dances: this.dances,
          different_heats: this.different_heats,
          ids: this.getStartingCouples
        })
        .then(response => {
          const competition = response.data;
          store.commit(UPDATE_COMPETITION, competition);
          this.$router.push({
            name: "tournament_office.round.progress",
            params: { round_id: competition.last_round.round_id }
          });
          this.loading = false;
        });
    },
    emitRound(round) {
      this.$emit("updated", round);
    }
  },
  watch: {
    cutoff: {
      immediate: true,
      handler() {
        this.$emit("cutoff", this.cutoff);
      }
    }
  }
};
</script>

<style scoped lang="scss">
tr {
  &.selected {
    background-color: #a0eaff55;
  }
}
</style>
