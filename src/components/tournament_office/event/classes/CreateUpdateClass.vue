<template>
  <v-form ref="form" v-model="valid" @submit.prevent="newDance">
    <v-card>
      <v-card-title>
        {{ edit ? $t("event.classes.edit_class.title") : $t("event.classes.new_class.title") }}
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="name"
          :label="$t('event.classes.form.name.label')"
          :rules="[$form.fieldRequired, $form.noExistingAttribute(names, name)]"
        />
        <v-text-field
          v-model="tag"
          :label="$t('event.classes.form.tag.label')"
          counter="6"
          :rules="[
            $form.fieldRequired,
            $form.maxCharacterCount(6),
            $form.noExistingAttribute(tags, tag)
          ]"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{ edit ? $t("event.classes.edit_class.submit") : $t("event.classes.new_class.submit") }}
        </v-btn>
        <v-btn text @click="close">
          {{ $t("general.cancel") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
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
      valid: false,
      loading: false,
      name: this.dancing_class ? this.dancing_class.name : "",
      tag: this.dancing_class ? this.dancing_class.tag : ""
    };
  },
  computed: {
    edit() {
      return this.dancing_class;
    },
    names() {
      return this.edit
        ? []
        : this.$store.state.dependencies.classes
            .map(d => d.name.toLowerCase())
            .filter(n => n === this.name.toLowerCase());
    },
    tags() {
      return this.edit
        ? []
        : this.$store.state.dependencies.classes
            .map(d => d.tag.toLowerCase())
            .filter(t => t === this.tag.toLowerCase());
    }
  },
  methods: {
    newDance() {
      this.loading = true;
      if (this.edit) {
        Vue.axios
          .patch(`dependencies/class/${this.dancing_class.dancing_class_id}`, {
            name: this.name,
            tag: this.tag,
            discipline: this.discipline,
            order: this.order
          })
          .then(response => {
            store.commit(SET_CLASSES, response.data.classes);
            this.close();
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        Vue.axios
          .post("dependencies/class", {
            name: this.name,
            tag: this.tag,
            discipline_id: this.discipline,
            order: this.order
          })
          .then(response => {
            store.commit(SET_CLASSES, response.data.classes);
            this.close();
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    close() {
      this.name = "";
      this.tag = "";
      this.$refs.form.resetValidation();
      this.$emit("close");
    }
  }
};
</script>
