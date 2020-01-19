<template>
  <v-form ref="form" v-model="valid" @submit.prevent="newDance">
    <v-card>
      <v-card-title>
        {{ edit ? $t("event.couples.edit_couple.title") : $t("event.couples.new_couple.title") }}
      </v-card-title>
      <v-card-text>
        <v-select
          v-model="lead"
          :items="possibleLeads"
          :label="$t('event.couples.form.lead.label')"
          item-value="dancer_id"
          item-text="name"
          :disabled="edit"
        />
        <v-select
          v-model="follow"
          :items="possibleFollows"
          :label="$t('event.couples.form.follow.label')"
          item-value="dancer_id"
          item-text="name"
          :disabled="edit"
        />
        <v-select
          v-model="competitions"
          :items="possibleCompetitions"
          :label="$t('event.couples.form.competitions.label')"
          :hint="$t('event.couples.form.competitions.hint')"
          persistent-hint
          multiple
          item-value="competition_id"
          item-text="name"
          item-disabled="has_rounds"
        ></v-select>
        <v-progress-linear v-if="loading" load indeterminate />
        <modal :show="modalDelete" v-if="modalDelete">
          <delete-couple @close="close()" :couple="couple" />
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
          {{ $t("event.couples.delete_couple.submit") }}
        </v-btn>
        <v-spacer />
        <v-btn :disabled="!valid" :loading="updating" color="primary" text type="submit">
          {{
            edit ? $t("event.couples.edit_couple.submit") : $t("event.couples.new_couple.submit")
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
import { SET_COUPLES, UPDATE_COUPLE } from "@/store/modules/couples";
import { SET_COMPETITIONS } from "@/store/modules/competitions";
import DeleteCouple from "@/components/tournament_office/event/couples/DeleteCouple";
import Modal from "@/components/general/modal/Modal";
export default {
  components: { Modal, DeleteCouple },
  props: {
    couple: { type: Object, default: () => null }
  },
  data: function() {
    return {
      valid: false,
      updating: false,
      lead: this.couple ? this.couple.lead.dancer_id : null,
      follow: this.couple ? this.couple.follow.dancer_id : null,
      loading: this.edit,
      extendedCouple: null,
      competitions: [],
      modalDelete: false
    };
  },
  created() {
    if (this.edit) {
      this.loading = true;
      Vue.axios
        .get(`couples/${this.couple.couple_id}`)
        .then(response => {
          this.extendedCouple = response.data;
          this.competitions = response.data.competitions.map(c => c.competition_id);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  computed: {
    edit() {
      return !!this.couple;
    },
    possibleCompetitions() {
      return this.$store.state.competitions.competitions
        .filter(c => c.show_starting_list && c.qualification_id === null)
        .filter(
          c =>
            (c.mode === this.$constants.SINGLE_PARTNER && !c.has_rounds) ||
            (this.extendedCouple &&
              this.extendedCouple.competitions
                .map(c => c.competition_id)
                .includes(c.competition_id))
        );
    },
    possibleLeads() {
      if (this.edit) return [this.couple.lead];
      let couples = this.$store.state.couples.couples.filter(
        c => c.follow.dancer_id === this.follow
      );
      let leads = couples.map(c => c.lead.dancer_id);
      return this.$store.state.dancers.leads.filter(l => !leads.includes(l.dancer_id));
    },
    possibleFollows() {
      if (this.edit) return [this.couple.follow];
      let couples = this.$store.state.couples.couples.filter(c => c.lead.dancer_id === this.lead);
      let follows = couples.map(c => c.follow.dancer_id);
      return this.$store.state.dancers.follows.filter(f => !follows.includes(f.dancer_id));
    },
    deletable() {
      return this.extendedCouple ? this.extendedCouple.deletable : false;
    }
  },
  methods: {
    newDance() {
      this.updating = true;
      if (this.edit) {
        Vue.axios
          .patch(`couples/${this.couple.couple_id}`, {
            lead: this.lead,
            follow: this.follow,
            competitions: this.competitions
          })
          .then(response => {
            store.commit(UPDATE_COUPLE, response.data.couple);
            store.commit(SET_COMPETITIONS, response.data.competitions);
            this.close();
          })
          .finally(() => {
            this.updating = false;
          });
      } else {
        Vue.axios
          .post("couples", {
            lead: this.lead,
            follow: this.follow,
            competitions: this.competitions
          })
          .then(response => {
            store.commit(SET_COUPLES, response.data.couples);
            store.commit(SET_COMPETITIONS, response.data.competitions);
            this.close();
          })
          .finally(() => {
            this.updating = false;
          });
      }
    },
    close() {
      this.lead = null;
      this.follow = null;
      this.competitions = [];
      this.$refs.form.resetValidation();
      this.$emit("close");
    }
  }
};
</script>
