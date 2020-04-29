<template>
  <div>
    <v-dialog v-if="isMobile == false" v-model="dialog1" width="50vw">
      <template v-slot:activator="{ on }">
        <div v-on="on"><slot name="click" /></div>
      </template>
      <v-card
        id="check_fav"
        color="raba(0,0,0,0.6)"
        dark
      >
        <div id="like_store">
          <div v-if="flag == true">
            <div v-for="(value, i) in likeList" :key="i">
              <div class="like_store_card" @click="goDetail(value['id'])">
                <div class="like_store_desc like_store_name">
                  {{ value["store_name"] }}
                </div>
                <div class="like_store_desc">
                  ( {{ value["area"] }} )
                </div>
                <div class="like_store_desc">
                  평점 : {{ String(value["avg_score"]).slice(0,3) }}점  |
                </div>
                <div class="like_store_desc">
                  리뷰 : {{ value["review_count"] }}개
                </div>
              </div>
            </div>
          </div>
          <div v-else style="text-align: center; font-size: 24px;">
            좋아요한 가게가 없습니다.
          </div>
        </div>
      </v-card>
    </v-dialog>
    <v-dialog v-else v-model="dialog1" width="90vw">
      <template v-slot:activator="{ on }">
        <div v-on="on"><slot name="click" /></div>
      </template>
      <v-card
        id="check_fav"
        color="raba(0,0,0,0.6)"
        dark
      >
        <div id="like_store">
          <div v-if="flag == true">
            <div v-for="(value, i) in likeList" :key="i">
              <div class="like_store_card" @click="goDetail(value['id'])">
                <div class="like_store_desc like_store_name">
                  {{ value["store_name"] }}
                </div>
                <div class="like_store_desc">
                  ( {{ value["area"] }} )
                </div>
                <div class="like_store_desc">
                  평점 : {{ String(value["avg_score"]).slice(0,3) }}점  |
                </div>
                <div class="like_store_desc">
                  리뷰 : {{ value["review_count"] }}개
                </div>
              </div>
            </div>
          </div>
          <div v-else style="text-align: center; font-size: 24px;">
            좋아요한 가게가 없습니다.
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import router from "../router"
export default {
  props: {
    userLikeList: {}
  },
  data () {
    return {
      dialog1: false,
      isMobile: false,
      flag: true,
    }
  },
  computed: {
    likeList: v => v.userLikeList
  },
  watch: {
    userLikeList: function() {
      // console.log(this.userLikeList.length)
      if (this.userLikeList.length == 0) {
        this.flag = false
      }
    }
  },
  mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  methods: {
    goDetail(store_pk) {
      router.push("/StoreDetail/" + store_pk)
    },
    onResponsiveInverted() {
      if (window.innerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    },
  }
}
</script>

<style scoped>
#like_store {
  padding: 20px;
  max-height: 80vh;
}
.like_store_card {
  margin: 10px 0;
  background-color: white;
  border-radius: 15px;
  color: black;
  text-align: center;
  padding: 10px;
  cursor: pointer;
}
.like_store_card:hover {
  color: white;
  background-color: black;
}
.like_store_desc {
  display: inline-block;
  margin-right: 10px;
  font-family: "Yeon Sung", cursive;
  font-size: 18px;
}
.like_store_name {
  font-size: 24px;
  font-weight: 600;
  font-family: "Do Hyeon", sans-serif;
}
</style>