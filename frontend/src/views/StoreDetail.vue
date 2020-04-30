<template>
  <div>
    <Nav />
    <div class="header" />
    <div class="main">
      <!-- 음식점 정보 -->
      <div id="moveToWrite" class="main_content">
        <StoreInfo
          ref="write"
          :store-name="storeName"
          :store-score="storeScore"
          :review-cnt="reviewCnt"
          :store-area="storeArea"
          :store-tel="storeTel"
          :store-address="storeAddress"
          :store-categories="storeCategories"
          :store-menu-list="storeMenuList"
          :store-like="storeLike"
          @add-to-review="updatedReview"
        />
        <!-- 식당 태그 -->
        <!-- 리뷰 테이블 -->
        <StoreReview ref="updateReview" @avg="avgScore" @writeReview="writeReview" />
        <br>
        <br>
      </div>
      <!-- 오른쪽 기능 메뉴 -->
      <div class="aside">
        <div>
          <StoreLocation :longitude="longitude" :latitude="latitude" />
        </div>
        <br>
        <div v-if="tags !== null">
          <StoreWC :tags="tags" :store-name="storeName" />
        </div>
        <div v-else id="wordCloud">
          리뷰를 작성해서 <br> <i style="color:skyblue;"><b>워드클라우드</b></i> 의 <br> 주인공이 되어 보세요
        </div>
        <br>
        <DetailRecStores :store-id="storeId" />
      </div>
    </div>
    <div class="footer">
      <HomeFooter />
    </div>
  </div>
</template>

<script>
import Nav from "@/components/Nav.vue";
// import router from "@/router";
import StoreLocation from "@/components/StoreLocation";
import StoreInfo from "@/components/StoreInfo";
import StoreReview from "@/components/StoreReview";
import HomeFooter from "@/components/HomeFooter";
import DetailRecStores from "@/components/DetailRecStores";
import StoreWC from "@/components/StoreWC";
import { mapState, mapActions, mapMutations } from "vuex";
import http from "../api/http"
export default {
  components: {
    Nav,
    StoreLocation,
    StoreInfo,
    StoreReview,
    DetailRecStores,
    HomeFooter,
    StoreWC
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
      storeId: Number(this.$route.params.storeId),
      tags: "",
      storeLike: 0
    };
  },
  mounted(res) {
    const headers = {
      Authorization: "jwt " + localStorage.getItem("token")
    }
    http
      .get(
        `/api/store_info/${this.$route.params.storeId}`, {headers}
      )
      .then(res => {
        // console.log(res);
        this.storeName = res.data.store_name;
        this.storeArea = res.data.area;
        this.storeAddress = res.data.address;
        this.storeTel = res.data.tel;
        this.storeCategories = res.data.category_list;
        this.latitude = Number(res.data.latitude);
        this.longitude = Number(res.data.longitude);
        this.reviewCnt = res.data.review_count;
        this.storeMenuList = res.data.menues;
        this.tags = res.data.tag;
        this.storeLike = res.data.like;
      })
      .then(this.checkNavSearch(0));
  },
  methods: {
    ...mapMutations("data", ["checkNavSearch"]),
    updatedReview() {
      this.$refs.updateReview.reRoad();
    },
    avgScore(avgScore) {
      this.storeScore = Number(avgScore);
    },
    writeReview() {
      // console.log("clicked");
      this.$refs.write.write();
      document.getElementById("moveToWrite").scrollIntoView();
    }
  }
};
</script>

<style scoped>
.header {
  background: url("../../public/images/header.jpg");
  /* height: 200px;; */
  height: 100px;
  background-position: center;
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
  height: 100%;
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
.mobile_map {
  display: none;
}
#wordCloud {
  border: 1px solid white;
  background-color: white;
  border-radius: 10px;;
  font-size: 24px;
  text-align: center;
  padding: 10px;
}
@media screen and (max-width: 600px) {
  .mobile_map {
    display: block;
  }
  .main {
    display: flex;
    flex-flow: column nowrap;
  }
  .main_content {
    width: 100%;
    margin: 0;
    margin-bottom: 40px;
  }
  .aside {
    width: 100%;
    margin: 0;
  }
}
</style>