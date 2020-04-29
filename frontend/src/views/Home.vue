<template>
  <div id="home">
    <div id="home_header">
      <homeHeader />
    </div>
    <div id="home_side">
      <homeSide />
    </div>
    <div id="home_side_mobile" @click="goReport()">
      <div style="border: 1px solid white;">
        <div style="display: inline-block; font-size: 20px; margin-right: 10px;">F.C.A.R</div>
        <div style="display: inline-block; font-size: 16px;">최고의 분석 리포트</div>
      </div>
    </div>
    <div id="home_body">
      <div v-if="isMobile == false">
        <!-- algo기반 추천 -->
        <div v-if="check" id="home_body_recommand_algo">
          For You
        </div>
        <div v-if="check" id="home_body_recommand_algo_outter">
          <VueSlickCarousel v-bind="settings">
            <div v-for="i in userStores.length" :key="i">
              <homeBody
                :id="userStores[i-1].id"
                :name="userStores[i-1].name"
                :review-count="userStores[i-1].reviewCount"
                :area="userStores[i-1].area"
                :images="userStores[i-1].url"
                :avg-score="userStores[i-1].avgScore"
              />
            </div>
          </VueSlickCarousel>
        </div>
        <!-- 전체 추천 -->
        <div id="home_body_recommand_whole">
          Of You
        </div>
        <div v-if="mainEmptyFlag" class="home_body_recommand_whole_sub">
          반경 5km이내에 리뷰수가 10개 이상인 음식점이 없습니다.
        </div>
        <div v-if="location == 1" class="home_body_recommand_whole_sub">
          위치 정보 수집 허용을 해주세요.
        </div>
        <div v-if="allFlag == true" id="home_body_recommand_whole_outer">
          <VueSlickCarousel v-bind="settings">
            <div v-for="i in allStores.length" :key="i">
              <homeBody 
                :id="allStores[i-1].id"
                :name="allStores[i-1].name"
                :review-count="allStores[i-1].reviewCount"
                :area="allStores[i-1].area"
                :images="allStores[i-1].url"
                :avg-score="allStores[i-1].avgScore"
              />
            </div>
          </VueSlickCarousel>
        </div>
      </div>
      <div v-else>
        <div v-if="check" id="home_body_recommand_algo">
          For You
        </div>
        <VueSlickCarousel v-if="check" v-bind="settings_mobile">
          <div v-for="i in userStores.length" :key="i">
            <homeBody
              :id="userStores[i-1].id"
              :name="userStores[i-1].name"
              :review-count="userStores[i-1].reviewCount"
              :area="userStores[i-1].area"
              :images="userStores[i-1].url"
              :avg-score="userStores[i-1].avgScore"
            />
          </div>
        </VueSlickCarousel>
        <div id="home_body_recommand_whole">
          Of You
        </div>
        <div v-if="mainEmptyFlag" class="home_body_recommand_whole_sub">
          반경 5km이내에 리뷰수가 10개 이상인 음식점이 없습니다.
        </div>
        <div v-if="location == 1" class="home_body_recommand_whole_sub">
          위치 정보 수집 허용을 해주세요.
        </div>
        <div v-if="allFlag == true">
          <VueSlickCarousel v-bind="settings_mobile">
            <div v-for="i in allStores.length" :key="i">
              <homeBody 
                :id="allStores[i-1].id"
                :name="allStores[i-1].name"
                :review-count="allStores[i-1].reviewCount"
                :area="allStores[i-1].area"
                :images="allStores[i-1].url"
                :avg-score="allStores[i-1].avgScore"
              />
            </div>
          </VueSlickCarousel>
        </div>
      </div>
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
import HomeSide from "../components/HomeSide"
import { mapState, mapActions } from "vuex";
import router from "../router"

import VueSlickCarousel from 'vue-slick-carousel'
import 'vue-slick-carousel/dist/vue-slick-carousel.css'
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'

export default {
  components: {
    CheckFavorite,
    HomeHeader,
    HomeBody,
    VueSlickCarousel,
    HomeFooter,
    HomeSide
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
        focusOnSelect: true,
        infinite: true,
        slidesToShow: 4,
        speed: 500,
        swipeToSlide: true,
        arrows: false,
      },
      settings_mobile: {
        centerMode: true,
        focusOnSelect: true,
        infinite: true,
        slidesToShow: 1,
        speed: 500,
        swipeToSlide: true,
        arrows: false,
      },
      check: false,
      isMobile: false,
      allFlag: false,
      lon: 0,
      lat: 0,
      location: 1,
    }
  },
  computed: {
    ...mapState({
      islogined: state => state.data.isloggined,
      userStores: state => state.data.userBasedList,
      allStores: state => state.data.mainAllList,
      mainEmptyFlag: state => state.data.mainEmptyFlag
    }),
  },
  watch: {
    islogined: async function() {
      if (this.islogined == true) {
        if (localStorage.getItem("category_list").length == 0) {
          this.dialog = true
          document.getElementById("checkFav").click();
        }
      }
      this.check = true
    },
    allStores: async function() {
      this.allFlag = true
    }
  },
  async mounted() {
    await this.allRecommand()
    const that = this;
    await navigator.geolocation.getCurrentPosition(function(pos) {
      that.lat = Number(pos.coords.latitude);
      that.lon = Number(pos.coords.longitude);
      that.location = 0;
      const params = {
        latitude: that.lat,
        longitude: that.lon,
      }
      that.allRecommand(params)
    });
    
    await this.checkNavbar()
    await this.userBasedCheck()
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
    
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  destroyed() {
    this.checkNavbar() 
  },
  methods: {
    ...mapActions("data", ["checkNavbar"]),
    ...mapActions("data", ["userBasedRecommand"]),
    ...mapActions("data", ["allRecommand"]),
    async userBasedCheck() {
      if (localStorage.getItem("pk")) {
        await this.userBasedRecommand()
        this.check = true
      }
    },
    goReport() {
      router.push("/report")
    },
    onResponsiveInverted() {
      if (window.innerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    }
  },
};
</script>

<style scoped>
#home {
  background-color: black;
  /* background-color: white; */
  height: 100%;
}
#home_header {
  height: 250px;
}
#home_body {
  color: white;
  font-weight: bold;
  z-index: 2;
  padding: 20px;
  width: 70vw;
  margin: 0 auto;
}
#home_body_recommand_algo {
  font-size: 30px;
}
#home_body_recommand_whole {
  font-size: 30px;
  margin-top: 20px;
}
#home_footer {
  height: 200px;
}
#home_side {
  float: right;
  width: 12vw;
  position: sticky;
  right: 2vw;
  top: 1vw;
  margin-top: 10px;
  height: 500px;
}
#home_side_mobile {
  display: none;
}
#home_body_recommand_algo_outter {
  border: 3px solid white;
  padding: 20px;
}
#home_body_recommand_whole_outer {
  border: 3px solid white;
  padding: 20px;
}
.home_body_recommand_whole_sub {
  color: gray;
}
@media screen and (max-width: 600px) {
  #home_header {
    height: 150px;
  }
  #home_body {
    padding: 5px;
    width: 90vw;
  }
  #home_body_recommand_algo {
    font-size: 20px;
  }
  #home_body_recommand_whole {
    font-size: 20px;
    margin-top: 10px;
  }
  #home_footer {
    height: 100px;
  }
  #home_side {
    display:none;
  }
  #home_side_mobile {
    display: block;
    width: 80vw;
    margin: 20px auto 0 auto;
    border: 1px solid black;
    background-color: black;
    color: white;
    text-align: center;
  }
  .home_body_recommand_whole_sub {
    font-size: 12px;
    color: gray;
  }
}
</style>