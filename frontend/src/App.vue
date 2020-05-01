<template>
  <v-app id="app">
    <Nav v-if="onNav == false" style="height: 83px;" />
    <route-view :key="$route.fullPath" />
    <go-top />
  </v-app>
</template>

<script>
import RouteView from "@/components/RouteView";
import Nav from "@/components/Nav";
import GoTop from "@/components/GoTop";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    RouteView,
    Nav,
    GoTop
  },
  computed: {
    ...mapState({
      onNav: state => state.data.onNavFlag
    })
  },
  mounted() {
    if (localStorage.getItem("token")) {
      const params = {
        token: localStorage.getItem("token")
      }
      this.tokenVerify(params)
    }
  },
  methods: {
    ...mapActions("data", ["tokenVerify"])
  }
};
</script>


