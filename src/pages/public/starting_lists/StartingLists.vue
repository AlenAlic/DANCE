<template>
  <v-card class="fill-height" v-if="!loading">
    <v-card-text>
      <v-btn
        v-for="comp in competitions"
        :key="comp.competition_id"
        class="mb-3"
        block
        color="primary"
        :disabled="!comp.starting_list_visible"
        :to="{
          name: 'starting_lists.competition',
          params: { competition_id: comp.competition_id }
        }"
      >
        {{ comp.name }}
      </v-btn>
    </v-card-text>
  </v-card>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
export default {
  components: { Loading },
  data: function() {
    return {
      loading: false,
      competitions: []
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get("competition/starting_lists")
        .then(response => {
          this.competitions = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
