<template>
  <v-card class="fill-height" v-if="!loading">
    <v-card-title class="justify-center">{{ event.name }} ({{ event.date }})</v-card-title>
    <v-card-text>
      <v-btn
        v-for="result in event_results"
        :key="result.event_result_id"
        class="mb-3"
        block
        color="primary"
        :to="{
          name: 'events.results.result',
          params: { event_result_id: result.event_result_id }
        }"
      >
        {{ result.competition }}
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
      event_results: [],
      event: null
    };
  },
  created() {
    this.getEventData();
  },
  methods: {
    getEventData() {
      this.loading = true;
      Vue.axios
        .get(`event/${this.$route.params.event_id}/results`)
        .then(response => {
          this.event = response.data.event;
          this.event_results = response.data.results;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
