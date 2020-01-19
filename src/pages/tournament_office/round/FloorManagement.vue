<template>
  <v-card v-if="round">
    <v-card-title>
      {{ round.competition.name }} ({{ round.mode }}) / {{ round.name }}
    </v-card-title>
    <template v-if="round.type !== $constants.FINAL">
      <v-tabs v-model="tab" centered hide-slider show-arrows v-if="round" @change="changeTab">
        <v-tab v-for="dance in round.dances" :key="dance.dance_id" :href="`#${dance.dance_id}`">
          {{ dance.name }}
        </v-tab>
      </v-tabs>
      <v-divider />
      <v-card-text v-if="!disableCheckMarks">
        <div>
          <v-switch
            v-model="reload"
            :label="$t('round.floor_management.auto_reload')"
            dense
            color="primary"
            class="mt-0"
          ></v-switch>
          <v-btn color="primary" outlined class="mr-5 mb-3" @click="getData">
            {{ $t("round.floor_management.reload") }}
          </v-btn>
          <v-btn color="success" outlined class="mr-5 mb-3" @click="saveChecked">
            {{ $t("round.floor_management.save_checked") }}
          </v-btn>
          <v-btn color="error" outlined class="mr-5 mb-3" @click="uncheckModal = true">
            {{ $t("round.floor_management.uncheck_all.button") }}
          </v-btn>
          <modal
            :show="uncheckModal"
            @closeModal="hideUncheckModal"
            :title="$t('round.floor_management.uncheck_all.modal.title')"
            :text="
              $t('round.floor_management.uncheck_all.modal.text', {
                dance: round.dances.find(d => d.dance_id === Number(tab)).name
              })
            "
          ></modal>
          <template v-if="round.number_of_heats > 1">
            <v-btn color="primary" outlined class="mb-3" @click="moveCoupleModal = true">
              {{ $t("round.floor_management.move_couple.button") }}
            </v-btn>
            <modal :show="moveCoupleModal">
              <move-couple-card
                v-if="moveCoupleModal"
                :round="round"
                :dance_id="tab"
                @cancel="moveCoupleModal = false"
                @move="moveCouple"
              />
            </modal>
          </template>
        </div>
      </v-card-text>
      <v-card-text>
        <v-progress-linear indeterminate v-if="loading" />
      </v-card-text>
      <v-tabs-items v-model="tab" v-if="round">
        <v-tab-item
          v-for="dance in round.dances"
          :key="dance.dance_id"
          :value="`${dance.dance_id}`"
        >
          <v-card flat tile>
            <v-expansion-panels
              accordion
              multiple
              :value="Object.keys(data).map((v, i) => i)"
              v-if="data"
            >
              <v-expansion-panel v-for="heat in Object.keys(data)" :key="heat">
                <v-expansion-panel-header class="title">
                  {{ $t("round.floor_management.heat") }} {{ heat }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-row>
                    <template v-if="round.floors.length > 1">
                      <v-col
                        v-for="floor in Object.keys(data[heat])"
                        :key="floor"
                        cols="12"
                        md="6"
                        xl="4"
                      >
                        <div class="subtitle-2">
                          {{ $t("round.floor_management.floor") }} {{ floor }}
                        </div>
                        <div v-for="couple in Object.keys(data[heat][floor])" :key="couple">
                          <v-checkbox
                            class="mt-0"
                            hide-details
                            color="success"
                            v-model="present"
                            :disabled="disableCheckMarks"
                            :value="data[heat][floor][couple].couple_present_id"
                          >
                            <template v-slot:label>
                              <checkbox-couple-label
                                :couple="data[heat][floor][couple]"
                                :large="round.competition.mode === $constants.CHANGE_PER_DANCE"
                              />
                            </template>
                          </v-checkbox>
                        </div>
                      </v-col>
                    </template>
                    <v-col v-else>
                      <div v-for="couple in Object.keys(data[heat])" :key="couple">
                        <v-checkbox
                          class="mt-0"
                          hide-details
                          color="success"
                          v-model="present"
                          :disabled="disableCheckMarks"
                          :value="data[heat][couple].couple_present_id"
                        >
                          <template v-slot:label>
                            <checkbox-couple-label
                              :couple="data[heat][couple]"
                              :large="round.competition.mode === $constants.CHANGE_PER_DANCE"
                            />
                          </template>
                        </v-checkbox>
                      </div>
                    </v-col>
                  </v-row>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </template>
    <v-card-text v-else>
      {{ $t("round.floor_management.not_needed") }}
    </v-card-text>
  </v-card>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import CheckboxCoupleLabel from "@/components/tournament_office/round/adjudication/CheckboxCoupleLabel";
import Modal from "@/components/general/modal/Modal";
import Loading from "@/components/general/loading/Loading";
import MoveCoupleCard from "@/components/tournament_office/round/floor_management/MoveCoupleCard";
export default {
  components: { MoveCoupleCard, Modal, CheckboxCoupleLabel, Loading },
  data: function() {
    return {
      loading: false,
      round: null,
      tab: null,
      reload: false,
      timer: null,
      data: {},
      present: [],
      uncheckModal: false,
      moveCoupleModal: false
    };
  },
  created() {
    this.getRound();
  },
  computed: {
    disableCheckMarks() {
      return this.round && (this.round.has_next_round || this.round.completed);
    }
  },
  methods: {
    getRound() {
      clearInterval(this.timer);
      Vue.axios.get(`round/${this.$route.params.round_id}/floor_management`).then(response => {
        const round = response.data.round;
        const data = response.data.data;
        this.round = round;
        this.data = data.mapping;
        this.present = data.couples.filter(c => c.present).map(c => c.couple_present_id);
        this.tab = String(round.first_dance.dance_id);
      });
    },
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.$route.params.round_id}/floor_management/dance/${this.tab}`)
        .then(response => {
          this.data = response.data.mapping;
          this.present = response.data.couples.filter(c => c.present).map(c => c.couple_present_id);
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
        .patch(`round/${this.$route.params.round_id}/floor_management/dance/${this.tab}`, {
          couple_present_ids: this.present
        })
        .then(response => {
          this.data = response.data.mapping;
          this.present = response.data.couples.filter(c => c.present).map(c => c.couple_present_id);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    hideUncheckModal(data) {
      if (data.agree) {
        this.loading = true;
        Vue.axios
          .delete(`round/${this.$route.params.round_id}/floor_management/dance/${this.tab}`)
          .then(response => {
            this.data = response.data.mapping;
            this.present = [];
          })
          .finally(() => {
            this.loading = false;
          });
      }
      this.uncheckModal = false;
    },
    moveCouple(data) {
      this.moveCoupleModal = false;
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/floor_management/dance/${this.tab}/move`, data)
        .then(response => {
          this.data = response.data.mapping;
          this.present = response.data.couples.filter(c => c.present).map(c => c.couple_present_id);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    changeTab() {
      this.data = null;
      this.getData();
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
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  }
};
</script>
