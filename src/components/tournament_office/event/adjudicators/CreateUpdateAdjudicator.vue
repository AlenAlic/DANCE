<template>
  <v-form ref="form" v-model="valid" @submit.prevent="newAdjudicator">
    <v-card>
      <v-card-title>
        {{
          edit
            ? $t("event.adjudicators.edit_adjudicator.title")
            : $t("event.adjudicators.new_adjudicator.title")
        }}
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="name"
          :label="$t('event.adjudicators.form.name.label')"
          :rules="[$form.fieldRequired, $form.noExistingAttribute(names, name)]"
        />
        <v-text-field
          v-model="tag"
          :label="$t('event.adjudicators.form.tag.label')"
          counter="6"
          :rules="[
            $form.fieldRequired,
            $form.maxCharacterCount(6),
            $form.noExistingAttribute(tags, tag)
          ]"
        />
        <v-text-field
          v-model="password"
          :label="$t('event.adjudicators.form.password.label')"
          :hint="edit ? $t('event.adjudicators.form.password.hint') : ''"
          persistent-hint
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[
            !edit
              ? $form.fieldRequired
              : () => {
                  return true;
                },
            !!password
              ? $form.minCharacterCount(8)
              : () => {
                  return true;
                }
          ]"
          :type="showPassword ? 'text' : 'password'"
          @click:append="showPassword = !showPassword"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn :disabled="!valid" :loading="loading" color="primary" text type="submit">
          {{
            edit
              ? $t("event.adjudicators.edit_adjudicator.submit")
              : $t("event.adjudicators.new_adjudicator.submit")
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
import { SET_ADJUDICATORS, UPDATE_ADJUDICATOR } from "@/store/modules/adjudicators";
export default {
  props: {
    adjudicator: { type: Object, default: () => null }
  },
  data: function() {
    return {
      valid: false,
      loading: false,
      name: this.adjudicator ? this.adjudicator.name : "",
      tag: this.adjudicator ? this.adjudicator.tag : "",
      password: "",
      showPassword: false
    };
  },
  computed: {
    edit() {
      return !!this.adjudicator;
    },
    names() {
      return this.edit
        ? []
        : this.$store.state.adjudicators.adjudicators
            .map(a => a.name.toLowerCase())
            .filter(n => n === this.name.toLowerCase());
    },
    tags() {
      return this.edit
        ? []
        : this.$store.state.adjudicators.adjudicators
            .map(a => a.tag.toLowerCase())
            .filter(t => t === this.tag.toLowerCase());
    }
  },
  methods: {
    newAdjudicator() {
      this.loading = true;
      if (this.edit) {
        Vue.axios
          .patch(`adjudicators/${this.adjudicator.adjudicator_id}`, {
            name: this.name,
            tag: this.tag,
            password: this.password !== "" ? this.password : null
          })
          .then(response => {
            store.commit(UPDATE_ADJUDICATOR, response.data);
            this.close();
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        Vue.axios
          .post("adjudicators", {
            name: this.name,
            tag: this.tag,
            password: this.password
          })
          .then(response => {
            store.commit(SET_ADJUDICATORS, response.data);
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
      this.password = "";
      this.$refs.form.resetValidation();
      this.$emit("close");
    }
  }
};
</script>
