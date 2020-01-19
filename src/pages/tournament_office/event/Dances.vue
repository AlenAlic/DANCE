<template>
  <v-row>
    <v-col cols="12">
      <item-data-table
        ref="dances"
        :title="$t('event.dances.title')"
        :new-item-button-text="$t('event.dances.add_button')"
        :headers="headers"
        :items="$store.state.dependencies.dances"
        :loading-items="$store.state.dependencies.loadingDances"
      >
        <template v-slot:new-item>
          <create-update-dance @close="$refs.dances.closeNewItem()" />
        </template>
        <template v-slot:edit-item="item">
          <create-update-dance @close="$refs.dances.closeEditItem()" :dance="item.item" />
        </template>
        <template v-slot:delete-item="item">
          <delete-dance @close="$refs.dances.closeDeleteItem()" :dance="item.item" />
        </template>
      </item-data-table>
    </v-col>
  </v-row>
</template>

<script>
import ItemDataTable from "@/components/tournament_office/event/ItemDataTable";
import CreateUpdateDance from "@/components/tournament_office/event/dances/CreateUpdateDance";
import DeleteDance from "@/components/tournament_office/event/dances/DeleteDance";
export default {
  components: { DeleteDance, CreateUpdateDance, ItemDataTable },
  data: function() {
    return {
      headers: [
        {
          text: this.$t("event.dances.table.headers.name"),
          value: "name"
        },
        {
          text: this.$t("event.dances.table.headers.tag"),
          value: "tag"
        },
        {
          text: this.$t("event.dances.table.headers.discipline"),
          value: "discipline.name"
        },
        {
          text: this.$t("event.dances.table.headers.order"),
          value: "order",
          filterable: false
        },
        { value: "action", align: "right" }
      ]
    };
  }
};
</script>
