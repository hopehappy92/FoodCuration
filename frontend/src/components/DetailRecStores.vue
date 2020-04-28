<template>
  <div v-if="flag" class="container">
    <p id="rec_title">"이 식당들은 어때요??"</p>
    <div v-for="(store, i) in recStores" :key="i">
      <!-- <img class="recImages" :src="store.images[0]" alt="이미지" /> -->
      <div style="display: flex; flex-flow: row;">
        <div>
          <img
            v-if="store.url === ''"
            class="recImages"
            src="../../public/images/noImage1.jpg"
            alt="gg"
          >
          <img v-else class="recImages" :src="store.url" alt="이미지">
        </div>
        <div class="store_summary">
          <div class="summary_top">
            <span id="rec_name">{{ store.store_name }}</span>
            <span id="rec_score">{{ store.avg_score.toFixed(1) }}</span>
          </div>
          <div class="summary_bottom">
            <div class="sb_container">
              <span class="sb">지역:</span>
              <span class="sb_content">{{ store.area }}</span>
            </div>
            <div class="sb_container">
              <span class="sb">리뷰 개수:</span>
              <span class="sb_content">{{ store.review_count }}</span>
            </div>
            <div>
              <i class="fas fa-arrow-right" />
              <button @click.prevent="moveToStore(store.id)">상세보기</button>
            </div>
          </div>
        </div>
      </div>
      <br v-if="i < 2">
      <hr v-if="i < 2" id="line">
      <br v-if="i < 2">
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
  data() {
    return {
      recStores: Array,
      noImage: "../../public/images/noImage1",
      flag: false
    };
  },
  mounted() {
    const params = this.storeId;
    api.getRecommendStore(params).then(res => {
      var picked = [];
      var max_length = res.data.length;
      var cnt = false;
      var flag = true;
      console.log(res);
      console.log("굿굿");
      while (cnt === false) {
        var ranNum = Math.floor(Math.random() * max_length);
        if (ranNum > 0 && ranNum < max_length-1) {
          console.log(ranNum);
          picked.push(ranNum);
          picked.push(ranNum + 1);
          picked.push(ranNum - 1);
          cnt = true;
        } else {
          continue;
        }
      }
      console.log(picked);
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
  font-size: 30px;
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
#rec_name {
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
  -webkit-animation: fadeIn 1s 1s infinite linear normal;
  -moz-animation: fadeIn 1s 1s infinite linear normal;
  -ms-animation: fadeIn 1s 1s infinite linear normal;
  -o-animation: fadeIn 1s 1s infinite linear normal;
  animation: fadeIn 1s 1s infinite linear normal;
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
@keyframes fadeIn {
  from {
    background: rgb(185, 185, 185);
  }
  to {
    background: rgb(121, 121, 121);
  }
}
@media screen and (max-width: 600px) {
  #rec_name {
    display: inline-block;
    width: 24vw;
    overflow: hidden;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  #rec_title {
    font-size: 10vw;
  }
  .recImages {
    width: 45vw;
    height: 150px;
  }
}
</style>