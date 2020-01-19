<template>
  <v-form ref="form" v-model="valid" @submit.prevent="newDance">
    <v-card>
      <v-card-title>
        {{
          edit
            ? $t("event.disciplines.edit_discipline.title")
            : $t("event.disciplines.new_discipline.title")
        }}
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="name"
          :label="$t('event.disciplines.form.name.label')"
          :rules="[$form.fieldRequired, $form.noExistingAttribute(names, name)]"
        />
        <v-text-field
          v-model="tag"
          :label="$t('event.disciplines.form.tag.label')"
          counter="6"
          :rules="[
            $form.fieldRequired,
            $form.maxCharacterCount(6),
            $form.noExistingAttribute(tags, tag)
          ]"
        />
        <v-select
          v-model="dances"
          :items="filteredDances"
          :label="$t('event.disciplines.form.dances.label')"
          :no-data-text="$t('event.disciplines.form.dances.no_data')"
          item-value="dance_id"
          item-text="name"
          :rules="[$form.fieldRequired]"
          :disabled="edit && !discipline.deletable"
          multiple
        ></v-select>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{
            edit
              ? $t("event.disciplines.edit_discipline.submit")
              : $t("event.disciplines.new_discipline.submit")
          }}
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
    discipline: { type: Object, default: () => null }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      name: this.discipline ? this.discipline.name : "",
      tag: this.discipline ? this.discipline.tag : "",
      dances: this.discipline ? this.discipline.dances.map(d => d.dance_id) : []
    };
  },
  computed: {
    edit() {
      return this.discipline;
    },
    names() {
      return this.edit
        ? []
        : this.$store.state.dependencies.disciplines
            .map(d => d.name.toLowerCase())
            .filter(n => n === this.name.toLowerCase());
    },
    tags() {
      return this.edit
        ? []
        : this.$store.state.dependencies.disciplines
            .map(d => d.tag.toLowerCase())
            .filter(t => t === this.tag.toLowerCase());
    },
    filteredDances() {
      return this.$store.state.dependencies.dances.filter(
        d =>
          !d.discipline ||
          (d.discipline &&
            this.discipline &&
            d.discipline.discipline_id === this.discipline.discipline_id)
      );
    }
  },
  methods: {
    newDance() {
      this.loading = true;
      if (this.edit) {
        Vue.axios
          .patch(`dependencies/discipline/${this.discipline.discipline_id}`, {
            name: this.name,
            tag: this.tag,
            dances: this.dances
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
          .post("dependencies/discipline", {
            name: this.name,
            tag: this.tag,
            dances: this.dances
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
      this.dances = [];
      this.$refs.form.resetValidation();
      this.$emit("close");
    }
  }
};
</script>
