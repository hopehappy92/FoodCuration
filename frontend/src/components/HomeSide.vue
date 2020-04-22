<template>
  <div id="home_side_main">
    <div id="home_side_imgs" @click="goReport()">
      <img class="home_side_img" src="../../public/images/side_bg1.png" alt="side_ad">
      <img class="home_side_img" src="../../public/images/side_bg2.png" alt="side_ad">
      <img class="home_side_img" src="../../public/images/side_bg1.png" alt="side_ad">
      <img class="home_side_img" src="../../public/images/side_bg2.png" alt="side_ad">
    </div>
  </div>
</template>

<script>
import router from "../router"

export default {
  methods: {
    goReport() {
      router.push("/report")
    }
  }
}
</script>

<style scoped>
#home_side_main {
  /* background-color: white; */
  z-index: 10;
  color: white;
  overflow: hidden;
  border: 1px solid white;
  cursor: pointer;
}
#home_side_imgs {
  display: flex;
  width: 100%;
  height: 100%;
  -webkit-animation: macCarousell 20s linear infinite;
	-moz-animation: macCarousell 20s linear infinite;
	-ms-animation: macCarousel 20s linear infinite;
	animation: macCarousel 20s linear infinite;
}
.home_side_img {
  width: 100%;
  height: 100%;
}
@-webkit-keyframes macCarousel {
	0%,
	23% {
		margin-left: 0%;
	}
	25%,
	48% {
		margin-left: -100%;
	}
	50%,
	73% {
		margin-left: -200%;
	}
	75%,
	98% {
		margin-left: -300%;
	}
	100% {
		margin-left: 0%;
	}
}
@-moz-keyframes macCarousel {
	0%,
	23% {
		margin-left: 0%;
	}
	25%,
	48% {
		margin-left: -100%;
	}
	50%,
	73% {
		margin-left: -200%;
	}
	75%,
	98% {
		margin-left: -300%;
	}
	100% {
		margin-left: 0%;
	}
}
@-ms-keyframes macCarousel {
	0%,
	23% {
		margin-left: 0%;
	}
	25%,
	48% {
		margin-left: -100%;
	}
	50%,
	73% {
		margin-left: -200%;
	}
	75%,
	98% {
		margin-left: -300%;
	}
	100% {
		margin-left: 0%;
	}
}
@keyframes macCarousel {
	0%,
	23% {
		margin-left: 0%;
	}
	25%,
	48% {
		margin-left: -100%;
	}
	50%,
	73% {
		margin-left: -200%;
	}
	75%,
	98% {
		margin-left: -300%;
	}
	100% {
		margin-left: 0%;
	}
}
</style>