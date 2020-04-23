<template>
  <div class="home_body_card">
    <div class="container">
      <img v-if="images == ''" src="../../public/images/icons/user.png" class="home_body_card_img" alt="image">
      <img v-else :src="images" alt="image" class="home_body_card_img">
      <div class="home_body_card_hover">
        <div class="home_body_card_text">
          <div style="font-size: 1.4vw; margin-bottom: 5px;">{{ name }}</div>
          <div class="home_body_card_desc">평점 : {{ avgScore.toFixed(1) }}</div>
          <div class="home_body_card_desc">리뷰 갯수 : {{ reviewCount }}</div>
          <div class="home_body_card_desc">지역 : {{ area }}</div>
        </div>
        <button class="home_body_card_btn" @click.prevent="goDetail()">Go Detail</button>
      </div>
    </div>
  </div>
</template>
 
<script>
import router from "../router"

  export default {
    props: {
      id: {
        type: Number,
        default: 0
      },
      name: {
        type: String,
        default: ""
      },
      reviewCount: {
        type: Number,
        default: 0
      },
      area: {
        type: String,
        default: ""
      },
      images: {
        type: String,
        default: ""
      },
      avgScore: {
        type: Number,
        default: 0
      }
    },
    data() {
      return {
        image: ""
      }
    },
    methods: {
      goDetail() {
        router.push("/StoreDetail/" + this.id)
      }
    }
  }
</script>

<style scoped>
.home_body_card {
  height: 250px;
}
.container {
  position: relative;
}

.home_body_card_img {
  opacity: 1;
  display: block;
  width: 100%;
  height: 15vw;
  /* height: 100%; */
  transition: .5s ease;
  /* backface-visibility: hidden; */
  /* background-position: center;
  background-repeat: no-repeat; */
  /* background-size: 100% 100%; */
}

.home_body_card_hover {
  transition: .5s ease;
  opacity: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
  height: 100%;
  padding-top: 3vw;
}

.container:hover .home_body_card_img {
  opacity: 0.3;
}

.container:hover .home_body_card_hover {
  opacity: 1;
}

.home_body_card_text {
  /* background-color: black; */
  color: white;
  font-size: 16px;
}
.home_body_card_btn {
  border: 2px solid white;
  padding: 4px 8px;
  margin-top: 2px;
}
.home_body_card_desc {
  margin-bottom: 2px;
}
</style>