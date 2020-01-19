<template>
  <v-card class="fill-height" v-if="!loading">
    <v-card-text>
      <v-btn
        v-for="comp in competitions"
        :key="comp.competition_id"
        class="mb-3"
        block
        color="primary"
        :disabled="!comp.round"
        :to="{
          name: 'heat_lists.competition',
          params: { competition_id: comp.competition_id }
        }"
      >
        <span v-if="!!comp.round"> {{ comp.name }} {{ comp.round.name }} </span>
        <span v-else>{{ comp.name }}</span>
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
        .get("competition/heat_lists")
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
