<template>
  <v-card v-if="isLastRound">
    <v-card-title>
      {{ $t("round.progress.delete_round.title") }}
    </v-card-title>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="error" text @click="modal = true" :loading="loading">
        {{ $t("round.progress.delete_round.submit") }}
      </v-btn>
    </v-card-actions>
    <modal
      :show="modal"
      @closeModal="hideModal"
      :title="$t('round.progress.delete_round.modal.title')"
      :text="$t('round.progress.delete_round.modal.text')"
    ></modal>
  </v-card>
</template>

<script>
import Vue from "vue";
import Modal from "@/components/general/modal/Modal";
import store from "@/store";
import { UPDATE_COMPETITION } from "@/store/modules/competitions";
export default {
  components: { Modal },
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      modal: false
    };
  },
  computed: {
    isLastRound() {
      return (
        this.round && this.round.competition.last_round_id === Number(this.$route.params.round_id)
      );
    }
  },
  methods: {
    hideModal(data) {
      if (data.agree) {
        this.deleteRound();
      }
      this.modal = false;
    },
    deleteRound() {
      this.loading = true;
      Vue.axios
        .delete(`round/${this.$route.params.round_id}`)
        .then(response => {
          const competition = response.data;
          store.commit(UPDATE_COMPETITION, competition);
          if (competition.last_round) {
            this.$router.push({
              name: "tournament_office.round.progress",
              params: { round_id: competition.last_round.round_id }
            });
          } else {
            this.$router.push({
              name: "tournament_office.competition",
              params: { competition_id: competition.competition_id }
            });
          }
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
