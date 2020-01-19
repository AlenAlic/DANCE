<template>
  <v-card>
    <v-card-title>
      {{ $t("round.progress.split.title") }}
    </v-card-title>
    <v-card-text v-if="!round.is_split">
      {{ $t("round.progress.split.text.not_split") }}
    </v-card-text>
    <v-card-text v-else>
      {{ $t("round.progress.split.text.split") }}
    </v-card-text>
    <v-card-actions v-if="!round.is_split">
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="showModal" :loading="loading">
        {{ $t("round.progress.split.button") }}
      </v-btn>
    </v-card-actions>
    <modal :show="modal" v-if="modal" @closeModal="modal = false">
      <v-card>
        <v-card-title>
          {{ $t("round.progress.split.modal.title") }}
        </v-card-title>
        <v-card-text>
          {{ $t("round.progress.split.modal.text") }}
        </v-card-text>
        <v-card-text v-if="loading">
          <v-progress-linear indeterminate />
        </v-card-text>
        <v-card-text v-else>
          <v-list dense>
            <v-list-item v-for="competition in competitions" :key="competition">
              <v-list-item-content>
                <v-list-item-title>{{ competition }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-text>
          <v-select
            v-model="split"
            :items="splitOptions"
            :label="$t('round.progress.split.modal.split.label')"
            :hint="$t('round.progress.split.modal.split.hint')"
            persistent-hint
            :rules="[$form.fieldRequired]"
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="splitRound" :loading="loading" :disabled="!split">
            {{ $t("round.progress.split.modal.button") }}
          </v-btn>
          <v-btn text @click="hideModal">
            {{ $t("general.cancel") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </modal>
  </v-card>
</template>

<script>
import Vue from "vue";
import Modal from "@/components/general/modal/Modal";
import store from "@/store";
import { SET_COMPETITIONS } from "@/store/modules/competitions";
export default {
  components: { Modal },
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      modal: false,
      split: "",
      splitOptions: [],
      competitions: []
    };
  },
  methods: {
    showModal() {
      this.getData();
      this.modal = true;
    },
    hideModal() {
      this.modal = false;
      this.splitOptions = [];
      this.competitions = [];
      this.split = "";
    },
    getData() {
      this.loading = true;
      Vue.axios
        .get(`round/${this.$route.params.round_id}/progress/split`)
        .then(response => {
          this.splitOptions = response.data.splits;
          this.competitions = response.data.competitions;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    splitRound() {
      const split = this.split;
      this.loading = true;
      this.hideModal();
      Vue.axios
        .post(`round/${this.$route.params.round_id}/progress/split`, {
          split: split
        })
        .then(response => {
          store.commit(SET_COMPETITIONS, response.data.competitions);
          this.$emit("updated", response.data.round);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
