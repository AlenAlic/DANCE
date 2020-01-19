<template>
  <v-card class="fill-height" v-if="$auth.isAuthenticated">
    <v-card-title>{{ $auth.currentUser.username }} ({{ $auth.currentUser.tag }})</v-card-title>
    <v-card-subtitle class="text--wrap">
      {{ $t("adjudicator.start.subtitle") }}
    </v-card-subtitle>
    <v-card-text>
      <div class="my-2" v-for="comp in competitions" :key="comp.competition_id">
        <v-btn
          width="100%"
          color="primary"
          :to="{
            name: 'adjudicator.dance',
            params: {
              round_id: comp.last_round.round_id,
              dance_id: comp.last_round.first_dance.dance_id
            }
          }"
          >{{ comp.name }}</v-btn
        >
      </div>
      <v-progress-linear indeterminate v-if="loading" />
    </v-card-text>
    <v-card-text>
      <v-btn width="100%" class="mt-4" color="success" outlined @click="getData">
        {{ $t("adjudicator.start.reload") }}
      </v-btn>
    </v-card-text>
    <v-card-subtitle class="font-weight-black">
      {{ $t("adjudicator.start.competitions") }}
    </v-card-subtitle>
    <v-card-text>
      <v-list dense v-for="day in days" :key="day.date">
        <v-subheader v-if="days.length > 1">
          {{ $util.dateTime(day.date).toFormat("DDDD") }}
        </v-subheader>
        <v-list-item dense v-for="comp in day.competitions" :key="comp.competition_id">
          <v-list-item-content>
            <v-list-item-subtitle>{{ comp.name }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-text>
      <v-btn width="100%" color="error" outlined @click="signOut()">
        {{ $t("auth.log_out") }}
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
import Vue from "vue";
export default {
  data: function() {
    return {
      loading: false,
      days: []
    };
  },
  created() {
    this.getData();
  },
  computed: {
    competitions() {
      return this.days
        .map(d => d.competitions)
        .flat()
        .filter(c => !!c.last_round && c.last_round.is_active)
        .filter(c => !!c.last_round.first_dance && c.last_round.first_dance.dance_id);
    }
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get("adjudication/dashboard")
        .then(response => {
          this.days = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    signOut: function() {
      this.$auth.signOut().then(() => {
        this.$router.push({
          name: "home"
        });
      });
    }
  }
};
</script>
