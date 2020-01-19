<template>
  <v-card>
    <v-card-title>
      {{ $t("event.classes.delete_class.title") }}
    </v-card-title>
    <v-card-text>
      {{ $t("event.classes.delete_class.text", { class: dancing_class.name }) }}
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="error" text @click="deleteClass" :loading="loading">
        {{ $t("event.classes.delete_class.submit") }}
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
import { SET_CLASSES } from "@/store/modules/dependencies";
export default {
  props: {
    dancing_class: { type: Object, default: () => null }
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
        .delete(`dependencies/class/${this.dancing_class.dancing_class_id}`)
        .then(response => {
          store.commit(SET_CLASSES, response.data.classes);
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
