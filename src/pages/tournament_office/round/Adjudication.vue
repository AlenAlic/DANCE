<template>
  <v-card v-if="round">
    <v-card-title>
      {{ round.competition.name }} ({{ round.mode }}) / {{ round.name }}
    </v-card-title>
    <v-tabs v-model="tab" centered hide-slider show-arrows v-if="round" @change="changeTab">
      <template v-for="dance in round.dances">
        <div :key="`btn-${dance.dance_id}`" class="my-auto">
          <v-btn
            v-if="!round.completed"
            small
            depressed
            class="ml-5"
            :color="dance.is_active ? 'error' : 'success'"
            @click="toggleDance(dance.dance_id)"
            :disabled="!showData"
          >
            {{
              dance.is_active ? $t("round.adjudication.disable") : $t("round.adjudication.enable")
            }}
          </v-btn>
        </div>
        <v-tab :key="`tab-${dance.dance_id}`" :href="`#${dance.dance_id}`">
          {{ dance.name }}
        </v-tab>
      </template>
    </v-tabs>
    <v-divider />
    <v-card-text v-if="!round.completed">
      <v-row>
        <v-col cols="12" :md="showData ? '6' : '12'">
          <div>
            <v-btn
              color="primary"
              class="mr-5 mb-3"
              @click="modal = true"
              :disabled="!round.can_evaluate"
            >
              {{ $t("round.adjudication.close_and_evaluate.button") }}
            </v-btn>
            <modal :show="modal">
              <close-and-evaluate-card
                :round="round"
                :data="evaluationData"
                @cancel="modal = false"
                @evaluate="evaluateRound"
              />
            </modal>
            <v-btn
              class="mb-3"
              :color="round.dances.filter(d => d.is_active).length > 0 ? 'error' : 'success'"
              @click="toggleRound"
              :disabled="!showData"
            >
              {{
                round.dances.filter(d => d.is_active).length > 0
                  ? $t("round.adjudication.close_round")
                  : $t("round.adjudication.open_round")
              }}
            </v-btn>
            <div v-if="showData">
              <v-switch
                v-model="reload"
                :label="$t('round.adjudication.auto_reload')"
                color="primary"
              ></v-switch>
              <v-btn color="primary" outlined class="mr-5 mb-3" @click="getData">
                {{ $t("round.adjudication.reload") }}
              </v-btn>
              <v-btn v-if="final" color="success" outlined class="mb-3" @click="savePlacings">
                {{ $t("round.adjudication.save_placings") }}
              </v-btn>
              <v-btn v-else color="success" outlined class="mb-3" @click="saveChecked">
                {{ $t("round.adjudication.save_crosses") }}
              </v-btn>
            </div>
            <div v-else class="text--wrap">
              {{ $t("round.adjudication.general_look_round_explanation") }}
            </div>
          </div>
        </v-col>
        <v-col cols="12" md="6" v-if="showData && data">
          <div class="title">
            <template v-if="final">
              {{ $t("round.adjudication.final_summary") }}
            </template>
            <template v-else>
              {{ $t("round.adjudication.target_marks") }}: {{ round.target_marks }}
              <v-icon class="ml-2 is-clickable" @click="editMarksModal = true">mdi-pencil</v-icon>
              <modal :show="editMarksModal">
                <update-target
                  v-if="editMarksModal"
                  :round="round"
                  @cancel="editMarksModal = false"
                  @updated="updateTarget"
                />
              </modal>
            </template>
          </div>
          <adjudicator-final-table v-if="final" :data="finalData" />
          <adjudicator-marks-table v-else :round="round" :data="evaluationData" />
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-text v-if="showData">
      <v-progress-linear indeterminate v-if="loading" />
    </v-card-text>
    <v-tabs-items v-model="tab" v-if="showData">
      <v-tab-item v-for="dance in round.dances" :key="dance.dance_id" :value="`${dance.dance_id}`">
        <v-card flat tile v-if="data">
          <v-card-text v-if="!round.completed">
            <div class="title">
              <span class="mr-3">{{ $t("round.adjudication.missing_adjudicators") }}</span>
              <span v-if="loadingAdjudicators">
                <v-progress-circular indeterminate color="primary" size="20" />
              </span>
            </div>
            <div v-if="round.is_active && !adjudicatorsPresent">
              {{
                adjudicators
                  .filter(a => !a.is_present)
                  .map(a => a.name)
                  .join(", ")
              }}
            </div>
            <div v-else-if="adjudicatorsPresent">
              {{ $t("round.adjudication.all_adjudicators_present") }}
            </div>
            <div v-else>
              {{ $t("round.adjudication.not_tracking_adjudicators") }}
            </div>
          </v-card-text>
          <v-card-text>
            <v-row>
              <v-col
                :cols="final ? 'auto' : 12"
                v-for="adjudicator in adjudicators"
                :key="adjudicator.adjudicator_id"
              >
                <v-card>
                  <v-card-title class="subheading font-weight-bold">
                    {{ adjudicator.name }}
                    <span class="ml-2 subtitle-1" v-if="round.floors.length > 1">
                      {{ $t("round.floor_management.floor") }} {{ adjudicator.floor }}
                    </span>
                    <span
                      class="ml-2 subtitle-2"
                      v-if="round.competition.mode === $constants.CHANGE_PER_DANCE"
                    >
                      ({{ $t(`round.adjudication.assignment.${adjudicator.assignment}`) }})
                    </span>
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-card-text>
                    <v-row v-if="final">
                      <adjudication-final-cell
                        v-for="p in data[adjudicator.adjudicator_id].placings"
                        :key="`${p.final_placing_id}-${p.final_placing}`"
                        v-model="placing"
                        :number="
                          adjudicator.assignment === $constants.ADJUDICATION_FOLLOW
                            ? p.follow_number
                            : p.number
                        "
                        :id="p.final_placing_id"
                        :data="p.final_placing"
                        :disabled="danceActive"
                      />
                    </v-row>
                    <v-row no-gutters v-else>
                      <adjudication-cell
                        v-for="m in followSort(data[adjudicator.adjudicator_id].marks, adjudicator)"
                        :key="m.mark_id"
                        v-model="mark"
                        :adjudicator="adjudicator"
                        :mark="m"
                        :disabled="danceActive"
                      />
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Modal from "@/components/general/modal/Modal";
import Loading from "@/components/general/loading/Loading";
import AdjudicationCell from "@/components/tournament_office/round/adjudication/AdjudicationCell";
import CloseAndEvaluateCard from "@/components/tournament_office/round/adjudication/CloseAndEvaluateCard";
import AdjudicatorMarksTable from "@/components/tournament_office/round/adjudication/AdjudicatorMarksTable";
import { FINAL, GENERAL_LOOK, RELOAD_TIMER_SHORT } from "@/constants";
import AdjudicatorFinalTable from "@/components/tournament_office/round/adjudication/AdjudicatorFinalTable";
import AdjudicationFinalCell from "@/components/tournament_office/round/adjudication/AdjudicationFinalCell";
import UpdateTarget from "@/components/tournament_office/round/adjudication/UpdateTarget";
export default {
  components: {
    UpdateTarget,
    AdjudicationFinalCell,
    AdjudicatorFinalTable,
    AdjudicatorMarksTable,
    AdjudicationCell,
    Modal,
    Loading,
    CloseAndEvaluateCard
  },
  data: function() {
    return {
      loading: false,
      round: null,
      tab: null,
      reload: false,
      key: 0,
      timer: null,
      data: null,
      adjudicators: [],
      mark: [],
      placing: [],
      modal: false,
      loadingAdjudicators: false,
      adjudicatorsTimer: null,
      editMarksModal: false
    };
  },
  created() {
    this.getRound();
  },
  computed: {
    showData() {
      return this.round && this.round.type !== GENERAL_LOOK;
    },
    adjudicatorsPresent() {
      return this.adjudicators.filter(a => !a.is_present).length === 0;
    },
    danceActive() {
      return this.round
        ? this.round.dances.find(d => {
            return d.dance_id === Number(this.tab);
          }).is_active
        : false;
    },
    loadAdjudicators() {
      return !this.adjudicatorsPresent && this.danceActive;
    },
    evaluationData() {
      return this.data && !this.final
        ? this.adjudicators.map(a => {
            return { adjudicator: a, marks: this.data[a.adjudicator_id].marks.filter(m => m.mark) };
          })
        : [];
    },
    general_look() {
      return this.round && this.round.type === GENERAL_LOOK;
    },
    final() {
      return this.round && this.round.type === FINAL;
    },
    finalData() {
      return this.data && this.final
        ? this.adjudicators.map(a => {
            return { adjudicator: a, placings: this.data[a.adjudicator_id].placings };
          })
        : [];
    }
  },
  methods: {
    getRound() {
      clearInterval(this.timer);
      Vue.axios.get(`round/${this.$route.params.round_id}/adjudication`).then(response => {
        const round = response.data.round;
        const data = response.data.data;
        this.round = round;
        this.data = data.mapping;
        this.adjudicators = Object.values(data.mapping)
          .map(a => a.adjudicator)
          .sort((a, b) => a.name.localeCompare(b.name));
        if (this.round.type === FINAL) {
          this.placing = data.couples;
        } else {
          this.mark = data.couples.filter(c => c.mark).map(c => c.mark_id);
        }
        this.tab = String(round.first_dance.dance_id);
      });
    },
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.$route.params.round_id}/adjudication/dance/${this.tab}`)
        .then(response => {
          this.round = response.data.round;
          this.data = response.data.mapping;
          this.adjudicators = Object.values(response.data.mapping)
            .map(a => a.adjudicator)
            .sort((a, b) => a.name.localeCompare(b.name));
          if (this.round.type === FINAL) {
            this.placing = response.data.couples;
          } else {
            this.mark = response.data.couples.filter(c => c.mark).map(c => c.mark_id);
          }
        })
        .catch(() => {
          clearInterval(this.timer);
          this.timer = null;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    saveChecked() {
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/adjudication/dance/${this.tab}`, {
          mark_ids: this.mark
        })
        .then(response => {
          this.round = response.data.round;
          this.data = null;
          this.data = response.data.mapping;
          this.adjudicators = Object.values(response.data.mapping)
            .map(a => a.adjudicator)
            .sort((a, b) => a.name.localeCompare(b.name));
          this.mark = response.data.couples.filter(c => c.mark).map(c => c.mark_id);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    savePlacings() {
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/adjudication/dance/${this.tab}`, {
          placings: this.placing
        })
        .then(response => {
          this.round = response.data.round;
          this.data = response.data.mapping;
          this.adjudicators = Object.values(response.data.mapping)
            .map(a => a.adjudicator)
            .sort((a, b) => a.name.localeCompare(b.name));
          this.placing = response.data.couples;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getAdjudicators() {
      this.loadingAdjudicators = true;
      Vue.axios
        .get(`round/${this.$route.params.round_id}/adjudication/dance/${this.tab}/adjudicators`)
        .then(response => {
          this.adjudicators = response.data;
          if (this.adjudicatorsPresent || !this.round.is_active) {
            clearInterval(this.adjudicatorsTimer);
          }
        })
        .catch(() => {
          clearInterval(this.adjudicatorsTimer);
          this.adjudicatorsTimer = null;
        })
        .finally(() => {
          this.loadingAdjudicators = false;
        });
    },
    toggleRound() {
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/adjudication/toggle`)
        .then(response => {
          this.round = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    toggleDance(dance_id) {
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/adjudication/dance/${dance_id}/toggle`)
        .then(response => {
          this.round = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    evaluateRound() {
      this.modal = false;
      this.loading = true;
      Vue.axios
        .post(`round/${this.$route.params.round_id}/adjudication/evaluate`)
        .then(() => {
          this.$router.push({
            name: "tournament_office.round.progress",
            params: { round_id: this.$route.params.round_id }
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    updateTarget(data) {
      this.editMarksModal = false;
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/adjudication`, {
          min_marks: data.min_marks,
          max_marks: data.max_marks
        })
        .then(response => {
          this.round = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    followSort(marks, adjudicator) {
      if (adjudicator.assignment === this.$constants.ADJUDICATION_FOLLOW) {
        const sortedMarks = [...marks];
        return sortedMarks.sort((a, b) => a.follow_number - b.follow_number);
      } else {
        return marks;
      }
    },
    changeTab() {
      if (!this.general_look) {
        this.data = null;
        this.getData();
      }
    }
  },
  watch: {
    reload: function(status) {
      if (status) {
        clearInterval(this.timer);
        this.timer = setInterval(this.getData, 5000);
        this.getData();
      } else {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
    loadAdjudicators: {
      immediate: true,
      handler(val) {
        if (val) {
          clearInterval(this.adjudicatorsTimer);
          this.adjudicatorsTimer = setInterval(this.getAdjudicators, RELOAD_TIMER_SHORT);
          this.getAdjudicators();
        } else {
          clearInterval(this.adjudicatorsTimer);
          this.adjudicatorsTimer = null;
        }
      }
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
    clearInterval(this.adjudicatorsTimer);
  }
};
</script>
