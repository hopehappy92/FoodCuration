<template>
  <div id="report_main">
    <div id="report_box">
      <div class="container-text">
        Report
      </div>
      <div id="report_desc">
        월 1$로 지역별 상권분석부터 업종별 경향까지 <br>
        다양한 분석 알고리즘으로 당신의 성공을 도와드립니다.
      </div>
      <div id="report_link">
        <div v-if="isMobile == false" id="report_free" class="report_add" @click="goReportPage()">
          무료 체험판
        </div>
        <div v-else id="report_mobile" class="report_add">
          모바일은 지원하지 않습니다.
        </div>
        <div class="report_add">
          |
        </div>
        <div class="report_add" @click="goHome()">
          돌아가기
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../router"
import { mapActions } from "vuex";

export default {
  data() {
    return {
      isMobile: false
    }
  },
  mounted() {
    this.onResponsiveInverted();
    window.addEventListener("resize", this.onResponsiveInverted);
    this.checkNavbar()
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResponsiveInverted);
  },
  destroyed() {
    this.checkNavbar()
  },
  methods: {
    ...mapActions("data", ["checkNavbar"]),
    goHome() {
      router.push("/")
    },
    goReportPage() {
      router.push("/reportpage")
    },
    onResponsiveInverted() {
      if (window.innerWidth < 600) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    }
  },
}
</script>

<style scoped>
#report_main {
  text-align: center;
  height: 100%;
  background-color: black;
}
#report_box {
  border: 5px solid;
  color: white;
  width: 60vw;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 30px;
}
#report_desc {
  font-size: 24px;
  animation: text 3s 1;
}
#report_link {
  animation: showup 4s ease-in-out;
}
.report_add {
  display: inline-block;
  cursor: pointer;
  margin-right: 14px;
  margin-top: 20px;
}
#report_free {
  color: yellowgreen;
  animation: showupfree 4s ease-in-out;
}
#report_mobile {
  color: red;
  animation: showupfree 4s ease-in-out;
}
.container-text {
  background-image:  url(https://static.pexels.com/photos/4827/nature-forest-trees-fog.jpeg);
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  color:  #FFFFFF;
  font-size: 200px;
  font-weight: 1000;
  font-family: 'Bungee', cursive;
  animation: filling 3s ease forwards;
}
@keyframes showup {
  0% {
    color: black;
  }
  80% {
    color: black;
  }
  100% {
    color: white;
  }
}
@keyframes showupfree {
  0% {
    color: black;
  }
  80% {
    color: black;
  }
  100% {
    color: yellowgreen;
  }
}
@keyframes filling {
  from{
    background-position: center 25%;
  }
  to {
    background-position: center 50%;
  }
}
@keyframes text {
  0%{
    color: black;
    margin-bottom: -40px;
  }
  30%{
    letter-spacing: 25px;
    margin-bottom: -40px;
  }
  85%{
    letter-spacing: 8px;
    margin-bottom: -40px;
  }
}

@media screen and (max-width: 600px) {
  #report_box {
    width: 80vw;
    height: 90%;
  }
  #report_desc {
    font-size: 20px;
  }
  .container-text {
    font-size: 50px;
    margin-top: 50vw;
  }
}
</style>