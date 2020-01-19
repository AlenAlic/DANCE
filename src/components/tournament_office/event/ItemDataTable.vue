<template>
  <v-card>
    <v-card-title>
      {{ title }}
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        :label="$t('general.search')"
        single-line
        hide-details
        clearable
      ></v-text-field>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="openNewItem">
        {{ newItemButtonText }}
      </v-btn>
      <modal :show="modalNewItem" v-if="modalNewItem">
        <slot name="new-item" />
      </modal>
      <modal :show="modalEditItem" v-if="modalEditItem">
        <slot name="edit-item" v-bind:item="item" />
      </modal>
      <modal :show="modalDeleteItem" v-if="modalDeleteItem">
        <slot name="delete-item" v-bind:item="item" />
      </modal>
    </v-card-title>
    <v-divider />
    <v-data-table
      :key="items.length"
      :loading="$store.state.dependencies.loadingDances"
      :headers="headers"
      :search="search"
      :items="items"
      :items-per-page="hideFooter ? items.length : 10"
      :hide-default-footer="hideFooter"
      :footer-props="
        hideFooter
          ? undefined
          : {
              itemsPerPageOptions: [5, 10, 15],
              showCurrentPage: true,
              showFirstLastPage: true,
              itemsPerPageText: $t('general.rows_per_page')
            }
      "
    >
      <template v-slot:item.dances="{ item }" v-if="showDances">
        <div class="py-3" v-if="item.dances">
          <div v-for="dance in item.dances" :key="dance.dance_id">{{ dance.name }}</div>
        </div>
      </template>
      <template v-slot:item.competitions="{ item }" v-if="showCompetitions">
        <div class="py-3" v-if="item.competitions">
          <div v-for="competition in item.competitions" :key="competition.competition_id">
            {{ competition.name }}
          </div>
        </div>
      </template>
      <template v-slot:item.action="{ item }">
        <v-btn icon class="mx-2" v-if="showEdit" @click="openEditItem(item)">
          <v-icon>{{ editIcon }}</v-icon>
        </v-btn>
        <v-btn
          icon
          class="mx-2"
          v-if="showDelete"
          :disabled="!item.deletable"
          @click="openDeleteItem(item)"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import Modal from "@/components/general/modal/Modal";
export default {
  components: { Modal },
  props: {
    editIcon: { type: String, default: "mdi-pencil" },
    title: { type: String, default: "Title" },
    newItemButtonText: { type: String, default: "New Item" },
    items: { type: Array, default: () => [] },
    loadingItems: { type: Boolean, default: false },
    headers: { type: Array, default: () => [] },
    showEdit: { type: Boolean, default: true },
    showDelete: { type: Boolean, default: true },
    hideFooter: { type: Boolean, default: true },
    showDances: { type: Boolean, default: false },
    showCompetitions: { type: Boolean, default: false }
  },
  data: function() {
    return {
      search: "",
      modalNewItem: false,
      modalEditItem: false,
      modalDeleteItem: false,
      item: null
    };
  },
  methods: {
    openNewItem() {
      this.modalNewItem = true;
    },
    closeNewItem() {
      this.modalNewItem = false;
    },
    openEditItem(item) {
      this.modalEditItem = true;
      this.item = item;
    },
    closeEditItem() {
      this.modalEditItem = false;
      this.item = null;
    },
    openDeleteItem(item) {
      this.modalDeleteItem = true;
      this.item = item;
    },
    closeDeleteItem() {
      this.modalDeleteItem = false;
      this.item = null;
    }
  }
};
</script>
