<template>
  <v-row>
    <v-col cols="12">
      <item-data-table
        ref="disciplines"
        :title="$t('event.disciplines.title')"
        :new-item-button-text="$t('event.disciplines.add_button')"
        :headers="headers"
        :items="$store.state.dependencies.disciplines"
        :loading-items="$store.state.dependencies.loadingDisciplines"
        show-dances
      >
        <template v-slot:new-item>
          <create-update-discipline @close="$refs.disciplines.closeNewItem()" />
        </template>
        <template v-slot:edit-item="item">
          <create-update-discipline
            @close="$refs.disciplines.closeEditItem()"
            :discipline="item.item"
          />
        </template>
        <template v-slot:delete-item="item">
          <delete-discipline @close="$refs.disciplines.closeDeleteItem()" :discipline="item.item" />
        </template>
      </item-data-table>
    </v-col>
  </v-row>
</template>

<script>
import ItemDataTable from "@/components/tournament_office/event/ItemDataTable";
import CreateUpdateDiscipline from "@/components/tournament_office/event/disciplines/CreateUpdateDiscipline";
import DeleteDiscipline from "@/components/tournament_office/event/disciplines/DeleteDiscipline";
export default {
  components: { DeleteDiscipline, CreateUpdateDiscipline, ItemDataTable },
  data: function() {
    return {
      headers: [
        {
          text: this.$t("event.disciplines.table.headers.name"),
          value: "name"
        },
        {
          text: this.$t("event.disciplines.table.headers.tag"),
          value: "tag"
        },
        {
          text: this.$t("event.disciplines.table.headers.dances"),
          value: "dances",
          sortable: false
        },
        { value: "action", align: "right" }
      ]
    };
  }
};
</script>
