<template>
  <v-form ref="form" v-model="valid" @submit.prevent="newDance">
    <v-card>
      <v-card-title>
        {{ edit ? $t("event.dancers.edit_dancer.title") : $t("event.dancers.new_dancer.title") }}
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="number"
          typ="number"
          :label="$t('event.dancers.form.number.label')"
          :rules="[$form.fieldRequired, $form.noExistingAttribute(numbers, number)]"
        />
        <v-text-field
          v-model="name"
          :label="$t('event.dancers.form.name.label')"
          :rules="[$form.fieldRequired]"
        />
        <v-select
          v-model="role"
          :items="$store.state.config.config.roles"
          :label="$t('event.dancers.form.role.label')"
        />
        <v-text-field
          v-model="team"
          :label="$t('event.dancers.form.team.label')"
          :rules="[$form.fieldRequired]"
        />
        <v-select
          v-model="competitions"
          :items="possibleCompetitions"
          :label="$t('event.dancers.form.competitions.label')"
          :hint="$t('event.dancers.form.competitions.hint')"
          persistent-hint
          multiple
          item-value="competition_id"
          item-text="name"
        ></v-select>
        <v-progress-linear v-if="loading" indeterminate />
        <template v-if="extendedDancer && extendedDancer.partners.length > 0">
          <v-list>
            <v-subheader>
              {{ $t("event.dancers.form.partners") }}
            </v-subheader>
            <v-list-item v-for="partner in extendedDancer.partners" :key="partner.dancer_id" dense>
              <v-list-item-content>
                <v-list-item-title>{{ partner.name }}</v-list-item-title>
                <v-list-item-subtitle
                  class="caption"
                  v-for="competition in partner.competitions"
                  :key="competition.competition_id"
                >
                  {{ competition }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </template>
        <modal :show="modalDelete" v-if="modalDelete">
          <delete-dancer @close="close()" :dancer="dancer" />
        </modal>
      </v-card-text>
      <v-card-actions>
        <v-btn
          v-if="edit"
          :disabled="!deletable"
          :loading="deletable && updating"
          text
          color="error"
          @click="modalDelete = true"
        >
          {{ $t("event.dancers.delete_dancer.submit") }}
        </v-btn>
        <v-spacer />
        <v-btn :disabled="!valid" :loading="updating" color="primary" text type="submit">
          {{
            edit ? $t("event.dancers.edit_dancer.submit") : $t("event.dancers.new_dancer.submit")
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
import { SET_DANCERS, UPDATE_DANCER } from "@/store/modules/dancers";
import { SET_COMPETITIONS } from "@/store/modules/competitions";
import DeleteDancer from "@/components/tournament_office/event/dancers/DeleteDancer";
import Modal from "@/components/general/modal/Modal";
export default {
  components: { Modal, DeleteDancer },
  props: {
    dancer: { type: Object, default: () => null }
  },
  data: function() {
    return {
      valid: false,
      updating: false,
      number: this.dancer ? this.dancer.number : null,
      name: this.dancer ? this.dancer.name : "",
      team: this.dancer ? this.dancer.team : "",
      role: this.dancer ? this.dancer.role : "",
      loading: this.edit,
      extendedDancer: null,
      competitions: [],
      modalDelete: false
    };
  },
  created() {
    if (this.edit) {
      this.loading = true;
      Vue.axios
        .get(`dancers/${this.dancer.dancer_id}`)
        .then(response => {
          this.extendedDancer = response.data;
          this.competitions = response.data.competitions.map(c => c.competition_id);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  computed: {
    edit() {
      return !!this.dancer;
    },
    numbersSource() {
      return this.$store.state.dancers.dancers;
    },
    numbers() {
      return this.edit
        ? []
        : this.numbersSource.map(d => d.number).filter(n => n === Number(this.number));
    },
    possibleCompetitions() {
      return this.$store.state.competitions.competitions
        .filter(c => c.dancing_class.name !== this.$constants.TEST && c.qualification_id === null)
        .filter(
          c =>
            (c.mode !== this.$constants.SINGLE_PARTNER && !c.has_rounds) ||
            (this.extendedDancer &&
              this.extendedDancer.competitions
                .map(c => c.competition_id)
                .includes(c.competition_id))
        );
    },
    deletable() {
      return this.extendedDancer ? this.extendedDancer.deletable : false;
    }
  },
  methods: {
    newDance() {
      this.updating = true;
      if (this.edit) {
        Vue.axios
          .patch(`dancers/${this.dancer.dancer_id}`, {
            number: this.number,
            name: this.name,
            role: this.role,
            team: this.team,
            competitions: this.competitions
          })
          .then(response => {
            store.commit(UPDATE_DANCER, response.data.dancer);
            store.commit(SET_COMPETITIONS, response.data.competitions);
            this.close();
          })
          .finally(() => {
            this.updating = false;
          });
      } else {
        Vue.axios
          .post("dancers", {
            number: this.number,
            name: this.name,
            role: this.role,
            team: this.team,
            competitions: this.competitions
          })
          .then(response => {
            store.commit(SET_DANCERS, response.data.dancers);
            store.commit(SET_COMPETITIONS, response.data.competitions);
            this.close();
          })
          .finally(() => {
            this.updating = false;
          });
      }
    },
    close() {
      this.number = null;
      this.name = "";
      this.team = "";
      this.role = "";
      this.competitions = [];
      this.$refs.form.resetValidation();
      this.$emit("close");
    }
  }
};
</script>
