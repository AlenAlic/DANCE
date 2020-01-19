<template>
  <v-card class="fill-height" v-if="!loading">
    <v-card-text>
      <v-btn
        v-for="event in inactiveEvents"
        :key="event.events_id"
        class="mb-3"
        block
        color="primary"
        :to="{
          name: 'events.results',
          params: { event_id: event.event_id }
        }"
      >
        {{ event.name }} ({{ event.date }})
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
      events: []
    };
  },
  computed: {
    inactiveEvents() {
      return this.events.filter(e => !e.is_active);
    }
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.loading = true;
      Vue.axios
        .get("event")
        .then(response => {
          this.events = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>
