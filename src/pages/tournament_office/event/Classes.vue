<template>
  <v-row>
    <v-col cols="12">
      <item-data-table
        ref="classes"
        :title="$t('event.classes.title')"
        :new-item-button-text="$t('event.classes.add_button')"
        :headers="headers"
        :items="$store.state.dependencies.classes"
        :loading-items="$store.state.dependencies.loadingDisciplines"
        show-dances
      >
        <template v-slot:new-item>
          <create-update-class @close="$refs.classes.closeNewItem()" />
        </template>
        <template v-slot:edit-item="item">
          <create-update-class @close="$refs.classes.closeEditItem()" :dancing_class="item.item" />
        </template>
        <template v-slot:delete-item="item">
          <delete-class @close="$refs.classes.closeDeleteItem()" :dancing_class="item.item" />
        </template>
      </item-data-table>
    </v-col>
  </v-row>
</template>

<script>
import ItemDataTable from "@/components/tournament_office/event/ItemDataTable";
import CreateUpdateClass from "@/components/tournament_office/event/classes/CreateUpdateClass";
import DeleteClass from "@/components/tournament_office/event/classes/DeleteClass";
export default {
  components: { DeleteClass, CreateUpdateClass, ItemDataTable },
  data: function() {
    return {
      headers: [
        {
          text: this.$t("event.classes.table.headers.name"),
          value: "name"
        },
        {
          text: this.$t("event.classes.table.headers.tag"),
          value: "tag"
        },
        { value: "action", align: "right" }
      ]
    };
  }
};
</script>
