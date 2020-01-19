<template>
  <tr class="highlighted-col">
    <th>
      {{ $t("public.results.competition_listing.rank") }}
    </th>
    <th>
      {{ $t("public.results.competition_listing.number") }}
    </th>
    <th class="text-left pl-1">
      {{
        changePartnerMode
          ? $t("public.results.competition_listing.dancer")
          : $t("public.results.competition_listing.couple")
      }}
    </th>
    <th class="text-left pl-1">
      {{
        changePartnerMode
          ? $t("public.results.competition_listing.team")
          : $t("public.results.competition_listing.teams")
      }}
    </th>
  </tr>
</template>

<script>
export default {
  props: {
    changePartnerMode: { type: Boolean, default: false }
  }
};
</script>
