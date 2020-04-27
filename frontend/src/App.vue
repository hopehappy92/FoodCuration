<template>
  <v-app id="app">
    <!-- <toolbar /> -->
    <!-- <drawer /> -->
    <Nav v-if="onNav == false" style="height: 83px;" />
    <!-- <HomeHeader v-if="onNav == false" style="height: 200px;"></HomeHeader> -->
    <route-view :key="$route.fullPath" />
    <go-top />
  </v-app>
</template>

<script>
// import Drawer from "@/components/Drawer";
// import Toolbar from "@/components/Toolbar";
import RouteView from "@/components/RouteView";
import Nav from "@/components/Nav";
import GoTop from "@/components/GoTop";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    // Drawer,
    // Toolbar,
    RouteView,
    Nav,
    GoTop
  },
  destroyed() {
    this.logout()
  },
  computed: {
    ...mapState({
      onNav: state => state.data.onNavFlag
    })
  },
  methods: {
    ...mapActions("data", ["logout"])
  }
};
</script>


