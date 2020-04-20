<template>
  <div id="home">
    <div id="home_header">
      <homeHeader />
    </div>
    <div id="home_body">
      <!-- algo기반 추천 -->
      <div id="home_body_recommand_algo">
        For You
      </div>
      <VueSlickCarousel v-bind="settings">
        <div v-for="i in 5" :key="i">
          <homeBody />
        </div>
      </VueSlickCarousel>
      <!-- 전체 추천 -->
      <div id="home_body_recommand_whole">
        Of You
      </div>
      <VueSlickCarousel v-bind="settings">
        <div v-for="i in 5" :key="i">
          <homeBody />
        </div>
      </VueSlickCarousel>
    </div>
    <checkFavorite>
      <div id="checkFav" slot="load" />
    </checkFavorite>
    <div id="home_footer">
      <homeFooter />
    </div>
  </div>
</template>

<script>
import CheckFavorite from "../components/CheckFavorite"
import HomeHeader from "../components/HomeHeader"
import HomeBody from "../components/HomeBody"
import HomeFooter from "../components/HomeFooter"
import { mapState, mapActions } from "vuex";

import VueSlickCarousel from 'vue-slick-carousel'
import 'vue-slick-carousel/dist/vue-slick-carousel.css'
// optional style for arrows & dots
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'

export default {
  components: {
    CheckFavorite,
    HomeHeader,
    HomeBody,
    VueSlickCarousel,
    HomeFooter
  },
  data() {
    return {
      dialog: false,
      checkfav_on: {
        display: "block"
      },
      checkfav_off: {
        display: "none"
      },
      settings: {
        centerMode: true,
        // centerPadding: "20px",
        focusOnSelect: true,
        infinite: true,
        slidesToShow: 4,
        speed: 500,
        swipeToSlide: true,
        arrows: false,
      }
    }
  },
  methods: {
    ...mapActions("data", ["checkNavbar"]),
  },
  mounted() {
    this.checkNavbar()
    const flag = true
    if (flag == true) {
      this.dialog = true
      window.onload=function(){
        document.getElementById("checkFav").click();
      };
    }
  },
  destroyed() {
    this.checkNavbar()
  }
};
</script>

<style scoped>
#home {
  /* background-image: url("../../public/images/home_bg2.jpg"); */
  background-color: #303536;
  height: 100%;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
#home_header {
  height: 250px;
}
#home_body {
  /* background-color: rgb(0,0,0); */
  /* background-color: #020202;  */
  color: white;
  font-weight: bold;
  /* border: 3px solid #f1f1f1; */
  z-index: 2;
  padding: 20px;
  /* text-align: center; */
  width: 80vw;
  margin: 0 auto;
}
#home_body_recommand_algo {
  font-size: 24px;
}
#home_body_recommand_whole {
  font-size: 24px;
  margin-top: 20px;
}
#home_footer {
  height: 200px;
}
</style>