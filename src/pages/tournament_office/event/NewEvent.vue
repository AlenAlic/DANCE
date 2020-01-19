<template>
  <v-row>
    <v-col cols="12" xl="6">
      <new-event-form />
    </v-col>
    <v-col cols="12" xl="6" v-if="!!$store.state.events.activeEvent">
      <reset-database-card />
    </v-col>
  </v-row>
</template>

<script>
import ResetDatabaseCard from "@/components/tournament_office/event/ResetDatabaseCard";
import NewEventForm from "@/components/tournament_office/event/new_event/NewEventForm";
export default {
  components: { NewEventForm, ResetDatabaseCard },
  created() {
    if (this.$store.state.events.activeEvent) {
      this.$router.push({ name: "tournament_office.event.setup" });
    }
  }
};
</script>
