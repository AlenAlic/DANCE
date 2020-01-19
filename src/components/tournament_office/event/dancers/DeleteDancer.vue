<template>
  <v-card>
    <v-card-title>
      {{ $t("event.dancers.delete_dancer.title") }}
    </v-card-title>
    <v-card-text>
      {{ $t("event.dancers.delete_dancer.text", { name: dancer.name }) }}
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="error" text @click="deleteClass" :loading="loading">
        {{ $t("event.dancers.delete_dancer.submit") }}
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
import { DELETE_DANCER } from "@/store/modules/dancers";
export default {
  props: {
    dancer: { type: Object, default: () => null }
  },
  data: function() {
    return {
      loading: false
    };
  },
  methods: {
    deleteClass() {
      this.loading = true;
      Vue.axios
        .delete(`dancers/${this.dancer.dancer_id}`)
        .then(response => {
          store.commit(DELETE_DANCER, response.data);
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
