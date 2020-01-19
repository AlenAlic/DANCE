<template>
  <v-row>
    <v-col cols="12" xl="4">
      <switch-user :users="users" />
    </v-col>
    <v-col cols="12" xl="4">
      <access-database />
    </v-col>
  </v-row>
</template>

<script>
import Vue from "vue";
import SwitchUser from "@/components/tournament_office/dashboard/SwitchUser";
import AccessDatabase from "@/components/tournament_office/dashboard/AccessDatabase";
export default {
  components: { AccessDatabase, SwitchUser },
  data: function() {
    return {
      loading: false,
      users: []
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get("event/dashboard")
        .then(response => {
          this.users = response.data.users;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
