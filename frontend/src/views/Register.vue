<template>
  <div id="register">
    <RegisterForm id="regiform" />
  </div>

</template>

<script>
import RegisterForm from "../components/RegisterForm"
import { mapActions } from "vuex";

export default {
  components: {
    RegisterForm
  },
  methods: {
    ...mapActions("data", ["checkNavbar"])
  },
  mounted() {
    // console.log("aaa")
    this.checkNavbar()
  },
  destroyed() {
    // console.log("bbb")
    this.checkNavbar()
  }
}
</script>

<style scoped>
#register {
  background-image: url("../../public/images/regi_bg.jpg");
  /* Add the blur effect */
  /* filter: blur(8px);
  -webkit-filter: blur(8px); */

  /* Full height */
  height: 100%;

  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
#regiform {
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(255, 255, 255, 0.9); /* Black w/opacity/see-through */
  color: white;
  font-weight: bold;
  border: 3px solid #f1f1f1;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
  padding: 20px;
  text-align: center;
}

@media screen and (max-width: 600px) {
  #register {
    background-image: none;
    background-color: black;
  }
  #regiform {
    padding: 10px;
    width: 80%;
  }

}
</style>