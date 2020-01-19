<template>
  <v-form ref="form" v-model="valid" @submit.prevent="newDance">
    <v-card>
      <v-card-title>
        {{ edit ? $t("event.dances.edit_dance.title") : $t("event.dances.new_dance.title") }}
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="name"
          :label="$t('event.dances.form.name.label')"
          :rules="[$form.fieldRequired, $form.noExistingAttribute(names, name)]"
        />
        <v-text-field
          v-model="tag"
          :label="$t('event.dances.form.tag.label')"
          counter="6"
          :rules="[
            $form.fieldRequired,
            $form.maxCharacterCount(6),
            $form.noExistingAttribute(tags, tag)
          ]"
        />
        <v-select
          v-model="discipline"
          :items="$store.state.dependencies.disciplines"
          :label="$t('event.dances.form.discipline.label')"
          item-value="discipline_id"
          item-text="name"
          :disabled="edit && !dance.deletable"
        />
        <v-text-field
          v-model="order"
          type="number"
          :label="$t('event.dances.form.order.label')"
          :hint="$t('event.dances.form.order.hint')"
          persistent-hint
          :rules="[$form.fieldRequired, $form.min(0)]"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{ edit ? $t("event.dances.edit_dance.submit") : $t("event.dances.new_dance.submit") }}
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
import { SET_DANCES, SET_DISCIPLINES } from "@/store/modules/dependencies";
export default {
  props: {
    dance: { type: Object, default: () => null }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      name: this.dance ? this.dance.name : "",
      tag: this.dance ? this.dance.tag : "",
      discipline: this.dance ? this.dance.discipline.discipline_id : null,
      order: this.dance ? this.dance.order : null
    };
  },
  computed: {
    edit() {
      return this.dance;
    },
    names() {
      return this.edit
        ? []
        : this.$store.state.dependencies.dances
            .map(d => d.name.toLowerCase())
            .filter(n => n === this.name.toLowerCase());
    },
    tags() {
      return this.edit
        ? []
        : this.$store.state.dependencies.dances
            .map(d => d.tag.toLowerCase())
            .filter(t => t === this.tag.toLowerCase());
    }
  },
  methods: {
    newDance() {
      this.loading = true;
      if (this.edit) {
        Vue.axios
          .patch(`dependencies/dance/${this.dance.dance_id}`, {
            name: this.name,
            tag: this.tag,
            discipline: this.discipline,
            order: this.order
          })
          .then(response => {
            store.commit(SET_DISCIPLINES, response.data.disciplines);
            store.commit(SET_DANCES, response.data.dances);
            this.close();
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        Vue.axios
          .post("dependencies/dance", {
            name: this.name,
            tag: this.tag,
            discipline_id: this.discipline,
            order: this.order
          })
          .then(response => {
            store.commit(SET_DISCIPLINES, response.data.disciplines);
            store.commit(SET_DANCES, response.data.dances);
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
      this.discipline = null;
      this.order = null;
      this.$refs.form.resetValidation();
      this.$emit("close");
    }
  }
};
</script>
