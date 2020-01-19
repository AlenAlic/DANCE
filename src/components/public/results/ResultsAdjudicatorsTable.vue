<template>
  <div class="table-skating-wrapper">
    <table class="table-skating table-skating--light">
      <thead>
        <tr class="dance-col">
          <th colspan="2" class="text-left pl-1">
            {{ $t("public.results.competition_report.adjudicators.title") }}
          </th>
        </tr>
        <tr>
          <th class="text-left pl-1 highlighted-col">
            <span class="mr-4">{{ $t("public.results.competition_report.adjudicators.tag") }}</span>
          </th>
          <th class="text-left pl-1">
            {{ $t("public.results.competition_report.adjudicators.name") }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="adj in adjudicators" :key="adj.adjudicator_id">
          <td class="text-left pl-1 highlighted-col">{{ adj.tag }}</td>
          <td class="text-left pl-1">{{ adj.name }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    adjudicators: { type: Array, default: () => [] }
  }
};
</script>
