<template>
  <v-row>
    <v-col cols="12" md="6">
      <c-s-v-couple />
    </v-col>
    <v-col cols="12">
      <item-data-table
        ref="couples"
        :title="$t('event.couples.title')"
        :new-item-button-text="$t('event.couples.add_button')"
        :headers="headers"
        :items="$store.state.couples.couples"
        :loading-items="$store.state.couples.loading"
        :hide-footer="false"
        :show-delete="false"
        edit-icon="mdi-eye"
      >
        <template v-slot:new-item>
          <couple @close="$refs.couples.closeNewItem()" />
        </template>
        <template v-slot:edit-item="item">
          <couple @close="$refs.couples.closeEditItem()" :couple="item.item" />
        </template>
      </item-data-table>
    </v-col>
  </v-row>
</template>

<script>
import ItemDataTable from "@/components/tournament_office/event/ItemDataTable";
import Couple from "@/components/tournament_office/event/couples/Couple";
import CSVCouple from "@/components/tournament_office/event/couples/CSVCouple";
export default {
  components: { CSVCouple, Couple, ItemDataTable },
  data: function() {
    return {
      headers: [
        {
          text: this.$t("event.couples.table.headers.number"),
          value: "number"
        },
        {
          text: this.$t("event.couples.table.headers.lead"),
          value: "lead.name"
        },
        {
          text: this.$t("event.couples.table.headers.follow"),
          value: "follow.name"
        },
        {
          text: this.$t("event.couples.table.headers.team"),
          value: "team"
        },
        { value: "action", align: "right" }
      ]
    };
  }
};
</script>
