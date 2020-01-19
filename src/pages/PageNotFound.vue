<template>
  <v-container class="fill-height login_container">
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <v-card max-width="400">
          <v-card-title>{{ $t("navigation.page_not_found") }}</v-card-title>
          <v-card-actions>
            <v-spacer />
            <router-link tag="span" :to="{ name: 'home' }">
              <v-btn text color="primary">
                {{ $t("navigation.go_back") }}
              </v-btn>
            </router-link>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
