<template>
  <div class="home_body_card">
    <div class="container">
      <img src="../../public/images/icons/user.png" alt="image" class="home_body_card_img">
      <div class="home_body_card_hover">
        <div class="home_body_card_text">
          <div>가게명</div>
          <div>평점</div>
          <div>리뷰수</div>
          <div>지역</div>
        </div>
        <button class="home_body_card_btn" @click.prevent="goDetail()">Go Detail</button>
      </div>
    </div>
  </div>
</template>
 
<script>
  export default {
    data() {
      return {
      }
    },
    methods: {
      goDetail() {
        console.log("aaaaaaaaaaaaaaaaaa")
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
  height: 100%;
  transition: .5s ease;
  backface-visibility: hidden;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
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
  padding-top: 4vw;
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
}
</style>