<template>
  <v-container class="fill-height">
    <transition name="fade" mode="out-in">
      <router-view></router-view>
    </transition>
  </v-container>
</template>

<script>
export default {
  created() {
    if (this.$auth.currentUser !== null) {
      let redirect = this.$route.query.redirect;
      if (redirect) {
        this.$router.replace(redirect);
      } else {
        this.$router.replace({
          name: "dashboard"
        });
      }
    }
  }
};
</script>
