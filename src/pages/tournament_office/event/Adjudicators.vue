<template>
  <v-row>
    <v-col cols="12">
      <item-data-table
        ref="adjudicators"
        :title="$t('event.adjudicators.title')"
        :new-item-button-text="$t('event.adjudicators.add_button')"
        :headers="headers"
        :items="$store.state.adjudicators.adjudicators"
        :loading-items="$store.state.adjudicators.loading"
        show-competitions
        hide-footer
      >
        <template v-slot:new-item>
          <create-update-adjudicator @close="$refs.adjudicators.closeNewItem()" />
        </template>
        <template v-slot:edit-item="item">
          <create-update-adjudicator
            @close="$refs.adjudicators.closeEditItem()"
            :adjudicator="item.item"
          />
        </template>
        <template v-slot:delete-item="item">
          <delete-adjudicator
            @close="$refs.adjudicators.closeDeleteItem()"
            :adjudicator="item.item"
          />
        </template>
      </item-data-table>
    </v-col>
  </v-row>
</template>

<script>
import ItemDataTable from "@/components/tournament_office/event/ItemDataTable";
import CreateUpdateAdjudicator from "@/components/tournament_office/event/adjudicators/CreateUpdateAdjudicator";
import DeleteAdjudicator from "@/components/tournament_office/event/adjudicators/DeleteAdjudicator";
export default {
  components: { DeleteAdjudicator, CreateUpdateAdjudicator, ItemDataTable },
  data: function() {
    return {
      headers: [
        {
          text: this.$t("event.adjudicators.table.headers.name"),
          value: "name"
        },
        {
          text: this.$t("event.adjudicators.table.headers.tag"),
          value: "tag"
        },
        {
          text: this.$t("event.adjudicators.table.headers.competitions"),
          value: "competitions"
        },
        { value: "action", align: "right" }
      ]
    };
  }
};
</script>
