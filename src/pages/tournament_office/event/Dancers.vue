<template>
  <v-row>
    <v-col cols="12" md="6">
      <c-s-v-dancer />
    </v-col>
    <v-col cols="12">
      <item-data-table
        ref="dancers"
        :title="$t('event.dancers.title')"
        :new-item-button-text="$t('event.dancers.add_button')"
        :headers="headers"
        :items="$store.state.dancers.dancers"
        :loading-items="$store.state.dancers.loading"
        :hide-footer="false"
        :show-delete="false"
        edit-icon="mdi-eye"
      >
        <template v-slot:new-item>
          <dancer @close="$refs.dancers.closeNewItem()" />
        </template>
        <template v-slot:edit-item="item">
          <dancer @close="$refs.dancers.closeEditItem()" :dancer="item.item" />
        </template>
      </item-data-table>
    </v-col>
  </v-row>
</template>

<script>
import ItemDataTable from "@/components/tournament_office/event/ItemDataTable";
import Dancer from "@/components/tournament_office/event/dancers/Dancer";
import CSVDancer from "@/components/tournament_office/event/dancers/CSVDancer";
export default {
  components: { CSVDancer, Dancer, ItemDataTable },
  data: function() {
    return {
      headers: [
        {
          text: this.$t("event.dancers.table.headers.number"),
          value: "number"
        },
        {
          text: this.$t("event.dancers.table.headers.name"),
          value: "name"
        },
        {
          text: this.$t("event.dancers.table.headers.role"),
          value: "role"
        },
        {
          text: this.$t("event.dancers.table.headers.team"),
          value: "team"
        },
        { value: "action", align: "right" }
      ]
    };
  }
};
</script>
