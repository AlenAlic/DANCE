<template>
  <v-card>
    <v-card-title>
      {{ $t("round.progress.add_remove_couple.title") }}
    </v-card-title>
    <v-card-subtitle>
      {{ $t("round.progress.add_remove_couple.subtitle") }}
    </v-card-subtitle>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="getAddCouples" :disabled="round" :loading="loading">
        {{ $t("round.progress.add_remove_couple.add") }}
      </v-btn>
      <v-btn color="error" text @click="getRemoveCouples" :disabled="round" :loading="loading">
        {{ $t("round.progress.add_remove_couple.remove") }}
      </v-btn>
    </v-card-actions>
    <modal :show="addModal" @closeModal="addModal = false">
      <v-card>
        <v-card-title>
          {{ $t("round.progress.add_couple.title") }}
        </v-card-title>
        <v-card-text>
          <v-select
            v-model="couple"
            :items="couples"
            :label="$t('round.progress.add_couple.label')"
            :no-data-text="$t('round.progress.add_couple.no_data')"
            :loading="loadingModal"
            item-value="couple_id"
            item-text="name"
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            :disabled="!couple"
            :loading="loadingModal"
            @click="addCouple"
          >
            {{ $t("round.progress.add_couple.submit") }}
          </v-btn>
          <v-btn text @click="closeModal">
            {{ $t("general.cancel") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </modal>
    <modal :show="removeModal" @closeModal="removeModal = false">
      <v-card>
        <v-card-title>
          {{ $t("round.progress.remove_couple.title") }}
        </v-card-title>
        <v-card-text>
          <v-select
            v-model="couple"
            :items="couples"
            :label="$t('round.progress.remove_couple.label')"
            :no-data-text="$t('round.progress.remove_couple.no_data')"
            :loading="loadingModal"
            item-value="couple_id"
            item-text="name"
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            :disabled="!couple"
            :loading="loadingModal"
            @click="removeCouple"
          >
            {{ $t("round.progress.remove_couple.submit") }}
          </v-btn>
          <v-btn text @click="closeModal">
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
export default {
  components: { Modal },
  props: {
    round: { type: Object, default: () => {} }
  },
  data: function() {
    return {
      loading: false,
      couple: null,
      couples: [],
      loadingModal: false,
      addModal: false,
      removeModal: false
    };
  },
  methods: {
    getAddCouples() {
      this.addModal = true;
      this.loadingModal = true;
      Vue.axios
        .get(`round/${this.$route.params.round_id}/progress/couples/possible`)
        .then(response => {
          if (this.addModal) {
            this.couples = response.data;
          }
        })
        .finally(() => {
          this.loadingModal = false;
        });
    },
    getRemoveCouples() {
      this.removeModal = true;
      this.loadingModal = true;
      Vue.axios
        .get(`round/${this.$route.params.round_id}/progress/couples`)
        .then(response => {
          if (this.removeModal) {
            this.couples = response.data;
          }
        })
        .finally(() => {
          this.loadingModal = false;
        });
    },
    closeModal() {
      this.couple = null;
      this.couples = [];
      this.addModal = false;
      this.removeModal = false;
    },
    addCouple() {
      this.loading = true;
      const couple = String(this.couple);
      this.closeModal();
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/progress/couple/${couple}`)
        .then(response => {
          this.emitData(response.data);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    removeCouple() {
      this.loading = true;
      const couple = String(this.couple);
      this.closeModal();
      Vue.axios
        .delete(`round/${this.$route.params.round_id}/progress/couple/${couple}`)
        .then(response => {
          this.emitData(response.data);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    emitData(d) {
      this.$emit("update", d);
    }
  }
};
</script>
