<template>
  <v-card>
    <v-card-title>
      {{ $t("event.dances.delete_dance.title") }}
    </v-card-title>
    <v-card-text>
      {{ $t("event.dances.delete_dance.text", { dance: dance.name }) }}
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="error" text @click="deleteDance" :loading="loading">
        {{ $t("event.dances.delete_dance.submit") }}
      </v-btn>
      <v-btn text @click="close">
        {{ $t("general.cancel") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import Vue from "vue";
import store from "@/store";
import { SET_DANCES, SET_DISCIPLINES } from "@/store/modules/dependencies";
export default {
  props: {
    dance: { type: Object, default: () => null }
  },
  data: function() {
    return {
      loading: false
    };
  },
  methods: {
    deleteDance() {
      this.loading = true;
      Vue.axios
        .delete(`dependencies/dance/${this.dance.dance_id}`)
        .then(response => {
          store.commit(SET_DISCIPLINES, response.data.disciplines);
          store.commit(SET_DANCES, response.data.dances);
          this.close();
        })
        .finally(() => {
          this.loading = false;
        });
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>
