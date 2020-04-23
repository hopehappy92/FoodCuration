<template>
  <div id="report_main" :style="flag == true ? mainStyleTrue : mainStyleFalse">
    <div v-if="flag==true" id="report_box">
      <div class="container-text">
        Report
      </div>
      <div id="report_desc">
        월 1$로 지역별 상권분석부터 업종별 경향까지 <br>
        다양한 분석 알고리즘으로 당신의 성공적인 창업을 도와드립니다.
      </div>
      <div>
        <div id="report_free" class="report_add" @click="goReportPage()">
          무료 체험판
        </div>
        <div class="report_add">
          |
        </div>
        <div class="report_add" @click="goHome()">
          돌아가기
        </div>
      </div>
    </div>
    <div v-else id="report_report">
      <reportPage />
    </div>
  </div>
</template>

<script>
import ReportPage from "../components/ReportPage"

import router from "../router"
import { mapActions } from "vuex";

export default {
  components: {
    ReportPage
  },
  data() {
    return {
      flag: true,
      mainStyleTrue: {
        backgroundColor: "black"
      },
      mainStyleFalse: {
        backgroundColor: "white"
      }
    }
  },
  mounted() {
    // console.log("aaa")
    this.checkNavbar()
  },
  destroyed() {
    // console.log("bbb")
    this.checkNavbar()
  },
  methods: {
    ...mapActions("data", ["checkNavbar"]),
    goHome() {
      router.push("/")
    },
    goReportPage() {
      this.flag = false
    }
  },
}
</script>

<style scoped>
#report_main {
  text-align: center;
  height: 100%;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
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
.report_add {
  display: inline-block;
  cursor: pointer;
  margin-right: 14px;
  margin-top: 20px;
}
#report_free {
  color: yellowgreen;
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
</style>