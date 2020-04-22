<template>
  <v-app id="app">
    <!-- <toolbar /> -->
    <!-- <drawer /> -->
    <Nav v-if="onNav == false" style="height: 86px;" />
    <!-- <HomeHeader v-if="onNav == false" style="height: 200px;"></HomeHeader> -->
    <route-view />
    <!-- <go-top /> -->
  </v-app>
</template>

<script>
// import Drawer from "@/components/Drawer";
// import Toolbar from "@/components/Toolbar";
import RouteView from "@/components/RouteView";
import Nav from "@/components/Nav";
import HomeHeader from "@/components/HomeHeader";
// import GoTop from "@/components/GoTop";
import { mapState } from "vuex";

export default {
  components: {
    // Drawer,
    // Toolbar,
    RouteView,
    Nav,
    HomeHeader
    // GoTop
  },
  computed: {
    ...mapState({
      onNav: state => state.data.onNavFlag
    })
  }
};
</script>


