<template>
  <div v-if="round && !printModal">
    <v-row>
      <v-col cols="12" md="8" v-if="round">
        <v-card v-if="round">
          <v-card-title>
            {{ round.competition.name }} ({{ round.mode }}) / {{ round.name }}
          </v-card-title>
          <v-card-text>
            <table>
              <tbody>
                <tr v-for="d in data" :key="d">
                  <td>
                    <v-checkbox
                      v-model="prints"
                      class="mr-4"
                      :label="$t(`round.reports.labels.${d}`)"
                      :value="d"
                      color="primary"
                    />
                  </td>
                  <td>
                    <print-copies v-model="printCopies" :prints="printCopies" :id="d" />
                  </td>
                </tr>
              </tbody>
            </table>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              text
              color="primary"
              @click="printModal = true"
              :disabled="printData.length === 0"
            >
              {{ $t("round.reports.show_preview") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" v-if="round">
        <v-card>
          <v-card-title>
            <span class="mr-2">{{ $t("round.reports.publish.title") }}</span>
            <v-icon v-if="round.heat_list_published">
              mdi-check-circle-outline
            </v-icon>
            <v-icon v-else>mdi-close-circle-outline</v-icon>
          </v-card-title>
          <v-card-text v-if="round.heat_list_published">
            {{ $t("round.reports.publish.is_published") }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text :loading="loading" @click="togglePublication">
              {{
                round.heat_list_published
                  ? $t("round.reports.publish.hide")
                  : $t("round.reports.publish.publish")
              }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
  <v-card v-else-if="printModal" class="card--print">
    <v-toolbar dark color="primary" class="mb-3">
      <v-toolbar-items>
        <v-btn dark text @click="print">{{ $t("round.reports.print") }}</v-btn>
      </v-toolbar-items>
      <v-spacer />
      <v-toolbar-title>{{ $t("round.reports.preview") }}</v-toolbar-title>
      <v-spacer />
      <v-btn icon dark @click="printModal = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text>
      <div class="printing-container" v-if="printModal">
        <print-preview :round="round" :print-data="printData" />
      </div>
    </v-card-text>
  </v-card>
  <loading v-else />
</template>

<script>
import Vue from "vue";
import Loading from "@/components/general/loading/Loading";
import PrintCopies from "@/components/tournament_office/round/reports/PrintCopies";
import PrintPreview from "@/components/tournament_office/round/reports/PrintPreview";
export default {
  components: { PrintPreview, PrintCopies, Loading },
  data: function() {
    return {
      loading: false,
      round: null,
      data: null,
      printModal: false,
      prints: [],
      printCopies: []
    };
  },
  created() {
    this.getRound();
  },
  computed: {
    printData() {
      return this.printCopies.filter(c => this.prints.includes(c.id));
    }
  },
  methods: {
    getRound() {
      Vue.axios.get(`round/${this.$route.params.round_id}/reports`).then(response => {
        const res = response.data;
        this.round = res.round;
        this.data = res.data;
        this.printCopies = res.data.map(d => ({ id: d, copies: 1 }));
      });
    },
    togglePublication() {
      this.loading = true;
      Vue.axios
        .patch(`round/${this.$route.params.round_id}/reports`)
        .then(() => {
          this.round.heat_list_published = !this.round.heat_list_published;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    print() {
      window.print();
    }
  }
};
</script>

<style scoped lang="scss">
.printing-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
</style>
