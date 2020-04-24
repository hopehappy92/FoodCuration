<template>
  <div>
    <Nav />
    <div class="header">
      <!-- 가게 사진들  -->
    </div>
    <div class="main">
      <!-- 음식점 정보 -->
      <div class="main_content">
        <StoreInfo
          :store-name="storeName"
          :store-score="storeScore"
          :review-cnt="reviewCnt"
          :store-area="storeArea"
          :store-tel="storeTel"
          :store-address="storeAddress"
          :store-categories="storeCategories"
          :store-menu-list="storeMenuList"
          @add-to-review="updatedReview"
        />
        <!-- 리뷰 테이블 -->
        <StoreReview ref="updateReview" @avg="avgScore" />
        <br />
        <br />
      </div>
      <!-- 오른쪽 기능 메뉴 -->
      <div class="aside">
        <StoreLocation :longitude="longitude" :latitude="latitude" />
        <br />
        <br />
        <DetailRecStores :storeId="storeId" />
      </div>
    </div>
    <HomeFooter></HomeFooter>
  </div>
</template>

<script>
import Nav from "@/components/Nav.vue";
import router from "@/router";
import axios from "axios";
import StoreLocation from "@/components/StoreLocation";
import StoreInfo from "@/components/StoreInfo";
import StoreReview from "@/components/StoreReview";
import HomeFooter from "@/components/HomeFooter";
import DetailRecStores from "@/components/DetailRecStores";
import { mapState, mapActions, mapMutations } from "vuex";
export default {
  components: {
    Nav,
    StoreLocation,
    StoreInfo,
    StoreReview,
    DetailRecStores,
    HomeFooter
  },
  mounted(res) {
    axios
      .get(
        `https://i02d106.p.ssafy.io:8765/api/stores/${this.$route.params.storeId}`
      )
      .then(res => {
        console.log(res);
        this.storeName = res.data.store_name;
        this.storeArea = res.data.area;
        this.storeAddress = res.data.address;
        this.storeTel = res.data.tel;
        this.storeCategories = res.data.category_list;
        this.latitude = Number(res.data.latitude);
        this.longitude = Number(res.data.longitude);
        this.reviewCnt = res.data.review_count;
        this.storeMenuList = res.data.menues;
      })
      .then(this.checkNavSearch(0));
  },
  data() {
    return {
      storeName: "",
      storeScore: 0,
      reviewCnt: 0,
      storeArea: "",
      storeTel: "",
      storeAddress: "",
      storeCategories: [],
      storeMenuList: [],
      latitude: 0,
      longitude: 0,
      storeId: Number(this.$route.params.storeId)
    };
  },
  methods: {
    ...mapMutations("data", ["checkNavSearch"]),
    updatedReview() {
      this.$refs.updateReview.reRoad();
    },
    avgScore(avgScore) {
      this.storeScore = Number(avgScore);
    }
  }
};
</script>

<style scoped>
.header {
  background: url("../../public/images/header.jpg");
  height: 200px;
  filter: brightness(30%);
}
.main {
  display: flex;
  background-color: rgb(15, 15, 15);
}
.aside {
  width: 30%;
  margin-left: 20px;
  background-color: rgb(15, 15, 15);
  height: fit-content;
  display: flex;
  flex-flow: column;
}
.main_content {
  width: 50%;
  display: flex;
  flex-flow: column nowrap;
  margin-left: 140px;
  background-color: whitesmoke;
  border-radius: 1%;
}
h2 {
  margin-top: 20px;
}
footer {
  height: 300px;
  width: 100%;
  background-color: rgb(15, 15, 15);
}
</style>