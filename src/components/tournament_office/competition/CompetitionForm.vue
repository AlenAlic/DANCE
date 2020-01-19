<template>
  <v-form ref="form" v-model="valid" @submit.prevent="updateCompetition" v-if="competition">
    <v-card>
      <v-card-title>
        {{ $t("competition.title") }}
      </v-card-title>
      <v-card-text v-if="loadingCompetition">
        <v-progress-linear indeterminate />
      </v-card-text>
      <template v-else>
        <v-card-subtitle>
          {{ competition.name }}
        </v-card-subtitle>
        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6" xl="4">
              <v-select
                v-model="discipline"
                :items="$store.state.dependencies.disciplines"
                :label="$t('competition.discipline.label')"
                :no-data-text="$t('competition.discipline.no_data')"
                :rules="[$form.fieldRequired]"
                item-value="discipline_id"
                item-text="name"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" xl="4">
              <v-select
                v-model="dancing_class"
                :items="$store.state.dependencies.classes"
                :label="$t('competition.dancing_class.label')"
                :no-data-text="$t('competition.dancing_class.no_data')"
                :rules="[$form.fieldRequired]"
                item-value="dancing_class_id"
                item-text="name"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" xl="4">
              <v-select
                v-model="mode"
                :items="$store.state.config.config.competition_modes"
                :label="$t('competition.mode.label')"
                :hint="$t('competition.mode.hint')"
                persistent-hint
                :rules="[$form.fieldRequired]"
                item-text="name"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" xl="4">
              <v-select
                v-model="qualification"
                :items="$store.state.competitions.competitions"
                :label="$t('competition.qualification.label')"
                :hint="$t('competition.qualification.hint')"
                persistent-hint
                item-text="name"
                item-value="competition_id"
                clearable
              ></v-select>
            </v-col>
            <v-col cols="4">
              <v-select
                v-model="floors"
                :items="[1, 2, 3]"
                :label="$t('competition.floors.label')"
                :hint="$t('competition.floors.hint')"
                persistent-hint
                :rules="[$form.fieldRequired]"
              ></v-select>
            </v-col>
            <v-col cols="9" xl="4">
              <v-datetime-picker
                v-model="date"
                :label="$t('competition.date.label')"
                :hint="$t('competition.date.hint')"
                persistent-hint
                :rules="[$form.fieldRequired]"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-autocomplete
                v-model="adjudicators"
                :items="$store.state.adjudicators.adjudicators"
                :label="$t('competition.adjudicators.label')"
                chips
                deletable-chips
                multiple
                item-text="name"
                item-value="adjudicator_id"
                clearable
                counter
                :menu-props="{ top: true }"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" v-if="mode === $constants.SINGLE_PARTNER">
              <v-autocomplete
                v-model="couples"
                :items="$store.state.couples.couples"
                :label="$t('competition.couples.label')"
                chips
                deletable-chips
                multiple
                item-text="name"
                item-value="couple_id"
                :disabled="!allowCouples"
                clearable
                counter
                :menu-props="{ top: true }"
              >
              </v-autocomplete>
            </v-col>
            <template v-else>
              <v-col cols="12">
                <v-autocomplete
                  v-model="leads"
                  :items="$store.state.dancers.leads"
                  :label="$t('competition.leads.label')"
                  chips
                  deletable-chips
                  multiple
                  item-text="competition_name"
                  item-value="dancer_id"
                  :disabled="!allowDancers"
                  clearable
                  counter
                  :menu-props="{ top: true }"
                ></v-autocomplete>
              </v-col>
              <v-col cols="12">
                <v-autocomplete
                  v-model="follows"
                  :items="$store.state.dancers.follows"
                  :label="$t('competition.follows.label')"
                  chips
                  deletable-chips
                  multiple
                  item-text="competition_name"
                  item-value="dancer_id"
                  :disabled="!allowDancers"
                  clearable
                  counter
                  :menu-props="{ top: true }"
                ></v-autocomplete>
              </v-col>
            </template>
          </v-row>
          <modal
            :show="deleteModal"
            v-if="deleteModal"
            @closeModal="hideModal"
            :title="$t('competition.delete.modal.title')"
            :text="$t('competition.delete.modal.text', { competition: competition.name })"
          ></modal>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="error" :disabled="!deletable" @click="showDeleteModal" type="button">
            {{ $t("general.delete") }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
            {{ $t("competition.submit") }}
          </v-btn>
          <v-btn text :to="{ name: 'tournament_office.event.setup' }">
            {{ $t("general.cancel") }}
          </v-btn>
        </v-card-actions>
      </template>
    </v-card>
  </v-form>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { UPDATE_COMPETITION, DELETE_COMPETITION } from "@/store/modules/competitions";
import VDatetimePicker from "@/components/general/datetime_picker/VDatetimePicker";
import Modal from "@/components/general/modal/Modal";
import { SET_ADJUDICATORS } from "@/store/modules/adjudicators";
export default {
  components: { Modal, VDatetimePicker },
  props: {
    competition: { type: Object, default: () => {} },
    loadingCompetition: { type: Boolean, default: false }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      discipline: this.competition.discipline.discipline_id,
      dancing_class: this.competition.dancing_class.dancing_class_id,
      floors: this.competition.floors,
      date: this.$util.dateTimeFromUTC(this.competition.date),
      mode: this.competition.mode,
      qualification: this.competition.qualification_id,
      adjudicators: this.competition.adjudicators.map(a => a.adjudicator_id),
      couples: this.competition.couples.map(c => c.couple_id),
      leads: this.competition.leads.map(d => d.dancer_id),
      follows: this.competition.follows.map(d => d.dancer_id),
      deleteModal: false
    };
  },
  computed: {
    allowCouples() {
      return this.mode === this.$constants.SINGLE_PARTNER;
    },
    allowDancers() {
      return (
        this.mode === this.$constants.RANDOM_SINGLE_PARTNER ||
        this.mode === this.$constants.CHANGE_PER_ROUND ||
        this.mode === this.$constants.CHANGE_PER_DANCE
      );
    },
    deletable() {
      return (
        this.competition &&
        this.competition.adjudicators.length === 0 &&
        this.competition.couples.length === 0 &&
        this.competition.leads.length === 0 &&
        this.competition.follows.length === 0
      );
    }
  },
  methods: {
    updateCompetition() {
      this.loading = true;
      Vue.axios
        .patch(`competition/${this.$route.params.competition_id}`, {
          discipline: this.discipline,
          dancing_class: this.dancing_class,
          floors: this.floors,
          date: this.$util.dateTimeToUTCString(this.date),
          mode: this.mode,
          qualification: this.qualification === undefined ? null : this.qualification,
          adjudicators: this.adjudicators,
          couples: this.couples,
          leads: this.leads,
          follows: this.follows
        })
        .then(response => {
          this.$emit("updated", response.data.competition);
          store.commit(UPDATE_COMPETITION, response.data.competition);
          store.commit(SET_ADJUDICATORS, response.data.adjudicators);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteCompetition() {
      this.loading = true;
      Vue.axios
        .delete(`competition/${this.$route.params.competition_id}`)
        .then(response => {
          store.commit(DELETE_COMPETITION, response.data);
          this.$router.push({
            name: "dashboard"
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    showDeleteModal() {
      this.deleteModal = true;
    },
    hideModal(data) {
      if (data.agree) {
        this.deleteCompetition();
      }
      this.deleteModal = false;
    }
  }
};
</script>
