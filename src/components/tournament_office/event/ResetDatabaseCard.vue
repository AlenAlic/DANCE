<template>
  <v-card>
    <v-card-title>
      {{ $t("event.database.title") }}
    </v-card-title>
    <v-card-subtitle class="text--wrap">
      {{ $t("event.database.subtitle") }}
    </v-card-subtitle>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="modal = true" :loading="loading">
        {{ $t("event.database.submit") }}
      </v-btn>
    </v-card-actions>
    <modal
      :show="modal"
      @closeModal="hideModal"
      :title="$t('event.database.modal.title')"
      :text="$t('event.database.modal.text')"
    ></modal>
  </v-card>
</template>

<script>
import Vue from "vue";
import loadStore from "@/store/loader";
import Modal from "@/components/general/modal/Modal";
import store from "@/store";
import { EVENTS_CLEAR } from "@/store/modules/events";
export default {
  components: { Modal },
  data: function() {
    return {
      loading: false,
      modal: false
    };
  },
  methods: {
    hideModal(data) {
      if (data.agree) {
        this.resetDatabase();
      }
      this.modal = false;
    },
    resetDatabase() {
      this.loading = true;
      Vue.axios
        .delete("config/reset")
        .then(() => {
          this.$router.push({ name: "tournament_office.event.new_event" });
          store.commit(EVENTS_CLEAR);
          loadStore();
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
