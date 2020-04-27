<template>
  <div>
    <div @click="goHome()">
      돌아가기
    </div>
    <div>
      뭘 적어야하나
    </div>
    <div>
      <a href="http://127.0.0.1:8000/admin">
        여기로 보낼까
      </a>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import router from "../router"

export default {
  async mounted() {
    await this.checkNavbar()
  },
  destroyed() {
    this.checkNavbar()
  },
  methods: {
    ...mapActions("data", ["checkNavbar"]),
    goHome() {
      router.push("/")
    }
  },
}
</script>

<style scoped>

</style>