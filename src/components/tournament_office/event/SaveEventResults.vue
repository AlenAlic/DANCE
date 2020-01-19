<template>
  <v-card>
    <v-card-title>
      {{ $t("event.results.title") }}
    </v-card-title>
    <v-card-subtitle class="text--wrap">
      {{ $t("event.results.subtitle") }}
    </v-card-subtitle>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="modal = true" :loading="loading">
        {{ $t("event.results.submit") }}
      </v-btn>
    </v-card-actions>
    <modal :show="modal">
      <v-card>
        <v-card-title>{{ $t("event.results.modal.title") }}</v-card-title>
        <v-card-text class="text--wrap">
          {{ $t("event.results.modal.saved") }}
        </v-card-text>
        <v-card-text v-if="saved.length > 0">
          <div v-for="comp in saved" :key="comp.competition_id">
            {{ comp.name }}
          </div>
        </v-card-text>
        <template v-if="ignored.length > 0">
          <v-card-text class="text--wrap">
            {{ $t("event.results.modal.not_saved") }}
          </v-card-text>
          <v-card-text>
            <div v-for="comp in ignored" :key="comp.competition_id">
              {{ comp.name }}
            </div>
          </v-card-text>
        </template>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="hideModal">
            {{ $t("event.results.submit") }}
          </v-btn>
          <v-btn text @click="modal = false">
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
  data: function() {
    return {
      loading: false,
      modal: false,
      saved: [],
      ignored: []
    };
  },
  created() {
    this.getCompetitions();
  },
  methods: {
    hideModal() {
      this.saveResults();
      this.modal = false;
    },
    saveResults() {
      this.loading = true;
      Vue.axios
        .post("config/results")
        .then(() => {})
        .finally(() => {
          this.loading = false;
        });
    },
    getCompetitions() {
      this.loading = true;
      Vue.axios
        .get("config/results")
        .then(response => {
          this.saved = response.data.saved;
          this.ignored = response.data.ignored;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
