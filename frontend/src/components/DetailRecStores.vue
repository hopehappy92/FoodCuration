<template>
  <div class="container" v-if="flag">
    <p id="rec_title">"이 식당들은 어때요??"</p>
    <div v-for="(store, i) in recStores" :key="i">
      <!-- <img class="recImages" :src="store.images[0]" alt="이미지" /> -->
      <div style="display: flex; flex-flow: row;">
        <img
          v-if="store.url === ''"
          class="recImages"
          src="../../public/images/noImage1.jpg"
          alt="gg"
          style="width:300px;"
        />
        <img v-else class="recImages" :src="store.url" alt="이미지" style="width:200px;" />
        <div class="store_summary">
          <div class="summary_top">
            <span>{{store.store_name}}</span>
            <span id="rec_score">{{store.avg_score.toFixed(1)}}</span>
          </div>
          <div class="summary_bottom">
            <div class="sb_container">
              <span class="sb">지역:</span>
              <span class="sb_content">{{store.area}}</span>
            </div>
            <div class="sb_container">
              <span class="sb">리뷰 개수:</span>
              <span class="sb_content">{{store.review_count}}</span>
            </div>
            <div>
              <i class="fas fa-arrow-right"></i>
              <button @click.prevent="moveToStore(store.id)">상세보기</button>
            </div>
          </div>
        </div>
      </div>
      <br v-if="i < 2" />
      <hr id="line" v-if="i < 2" />
      <br v-if="i < 2" />
    </div>
  </div>
</template>

<script>
import api from "../api";
import router from "../router";
export default {
  props: {
    storeId: Number
  },
  mounted() {
    const params = this.storeId;
    api.getRecommendStore(params).then(res => {
      var picked = [];
      var max_length = res.data.length;
      var cnt = 0;
      var flag = true;
      while (cnt < 3) {
        var ranNum = Math.floor(Math.random() * max_length);
        if (picked.includes(ranNum)) {
          continue;
        } else {
          picked.push(ranNum);
          cnt++;
        }
      }
      const recStores = [];
      for (var number of picked) {
        recStores.push(res.data[number]);
      }
      this.recStores = recStores;
      this.flag = true;
      console.log("ddd");
      console.log(recStores);
    });
  },
  data() {
    return {
      recStores: Array,
      noImage: "../../public/images/noImage1",
      flag: false
    };
  },
  methods: {
    moveToStore(storeId) {
      console.log(storeId);
      this.$router.push("/StoreDetail/" + storeId);
    }
  }
};
</script>

<style scoped>
.container {
  background: whitesmoke;
  border-radius: 5%;
  width: 100%;
}
.recImages {
  width: 200px;
  height: 150px;
}
.store_summary {
  display: flex;
  flex-flow: column;
  width: 100%;
}
#rec_title {
  text-align: center;
  font-family: "Do Hyeon", sans-serif;
  font-size: 40px;
  font-style: italic;
}
.summary_top {
  margin-left: 20px;
  display: flex;
  flex-wrap: nowrap;
}
.summary_top:nth-child(1) {
  font-size: 25px;
  font-family: "Do Hyeon", sans-serif;
}
#rec_score {
  font-size: 25px;
  font-family: "Do Hyeon", sans-serif;
  margin-left: 10px;
  color: grey;
}
.summary_bottom {
  margin-top: 10px;
  margin-left: 20px;
}
.sb_container {
  margin-bottom: 10px;
}
.sb {
  font-size: 15px;
  color: rgb(170, 170, 170);
  font-family: "Jua", sans-serif;
}
.sb_content {
  font-size: 15px;
  margin-left: 10px;
  font-family: "Jua", sans-serif;
}
.summary_bottom > div > button {
  margin-left: 10px;
  width: 100px;
  height: 40px;
  background: rgb(185, 185, 185);
  border-radius: 20%;
  font-family: "Jua", sans-serif;
  color: rgb(241, 241, 241);
}
.summary_bottom > div > button:hover {
  transition: background-color 0.5s;
  background: rgb(121, 121, 121);
}
.summary_bottom > div > i {
  font-size: 20px;
  color: rgb(94, 93, 93);
  -webkit-animation: fadeOut 1s 1s infinite linear normal;
  -moz-animation: fadeOut 1s 1s infinite linear normal;
  -ms-animation: fadeOut 1s 1s infinite linear normal;
  -o-animation: fadeOut 1s 1s infinite linear normal;
  animation: fadeOut 1s 1s infinite linear normal;
}
@keyframes fadeOut {
  from {
    opacity: 1;
    transform: translateX(-10px);
  }
  to {
    opacity: 0;
    transform: translateX(10px);
  }
}
</style>