<template>
  <v-container class="fill-height login_container">
    <v-row no-gutters justify="center" align="start">
      <div class="text-center">
        <h2>{{ $t("home.title") }}</h2>
        <p class="body-2">{{ $t("home.text") }}</p>
      </div>
    </v-row>
    <v-row no-gutters justify="center" align="start">
      <login />
    </v-row>
  </v-container>
</template>

<script>
import Login from "@/components/auth/Login";
export default {
  components: { Login },
  created() {
    if (this.$auth.isAuthenticated) {
      this.$router.push({
        name: "dashboard"
      });
    }
  }
};
</script>

<style scoped lang="scss">
@import "../assets/css/general/flex";
.login_container {
  @extend .align-items-stretch;
}
</style>
