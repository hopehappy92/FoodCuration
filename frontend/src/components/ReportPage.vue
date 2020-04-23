<template>
  <div id="report_docs">
    <div id="FC_logo">
      <img id="FC_logo_img" src="../../public/images/logo_black.png" alt="logo" @click="goHome()">
    </div>
    <div id="FCAR_logo">
      <img id="FCAR_logo_img" src="../../public/images/FCAR.png" alt="food curation analistic report">
    </div>
    <div id="report_header">
      <!-- Food Curation Analistic Report -->
      경제 경향 보고서
    </div>
    <div id="report_tabbox">
      <div v-for="(value, i) in tabs" :key="i" class="report_tab">
        <a :href="`#section${i+1}`" class="report_tab_a">
          {{ value }}
        </a>
      </div>
    </div>
    <div id="report_box">
      Detail Box
      이것은 글이다
      글이고
      <div id="section1">
        section1
      </div>
      
      이것은 글이다
      글이고
      <div id="section2">
        section2
      </div>
      이것은 글이다
      글이고
      <div id="section3">
        section3
      </div>
      이것은 글이다
      글이고
      <div id="section4">
        section4
      </div>
      이것은 글이다
      글이고

      <div id="section5">
        <div v-for="(value, i) in trendTabs" id="report_box_trend_btn" :key="i">
          <div :id="`btn${i}`" class="report_box_trend_btn_text" @click="showTrends(value)">
            {{ value }}
          </div>
        </div>
        <div id="report_box_trend_btn_all">
          <div class="report_box_trend_btn_text" @click="showTrends('all')">
            전체 비교
          </div>
        </div>
        <div id="report_box_trend_btn_all">
          <div id="report_box_trend_btn_text_detail" @click="showTrendsDetail()">
            그래프 보는법
          </div>
        </div>
        <div id="report_box_trend_btn_all">
          <div class="report_box_trend_btn_text" @click="deleteTrends()">
            초기화
          </div>
        </div>
        <div v-if="trendsDetail == true" id="report_box_trends_read">
          <div id="report_box_trends_read_box">
            <b style="font-size: 32px; color: white;">Stochastic</b><br>
            <div style="text-align: start; font-size: 18px; line-height: 30px;">
              <br>- 정의 : 최근 N일간의 최고 소비량와 최저 소비량의 범위 내에서 현재 소비량의 위치를 백분율로 표시한 지표(여기서 N=15)
              <br>- 주로 주식시장에서 변화를 민감하게 확인하기 위해 쓰이는 분석방법
              <br>- 지표는 Fast와 Slow로 나뉘고, 각각 %K, %D가 존재
              <br> &nbsp; &nbsp; - Fast는 민감하게 반응하기 때문에 아주 짧은 주기에 대해서 예측할 때 사용하고, 일반적으로 Slow를 사용함
              <br> &nbsp; &nbsp; - Slow %K : 어느정도 가까운 시일까지 반영되어 나온 데이터
              <br> &nbsp; &nbsp; - Slow %D : 조금 먼 시일까지 반영되어 나온 데이터
              <br>- 만약 K와 D가 꾸준히 상승을 그린다면, 호황기라고 볼 수 있음
              <br>- 만약 K와 D가 꾸준히 하락을 그리다가 K가 갑자기 반등한다면, 근래에 주목받았다고 볼 수 있음
              <br> &nbsp; &nbsp; - 반대로 K와 D가 꾸준히 상승을 그리다가 K가 갑자기 하락한다면, 근래에 사건이 있었다고 볼 수 있음
              <br>- K의 흐름에 따라서 D의 흐름이 따라갈 가능성이 있음
            </div>
          </div>
        </div>
        <div>
          <canvas v-if="trendFlag == false && trendreset == false" :id="`chart${trendNumber}`" class="report_box_trend_chart" />
          <div v-else-if="trendFlag == true && trendreset == false">
            <div v-for="(value, i) in trendTabs" :key="i">
              <canvas :id="`chart${i}`" class="report_box_trend_chart" />
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import router from "../router"

export default {
  data() {
    return {
      tabs: [
        "개요",
        "지역별",
        "상권 추천",
        "체인점",
        "업종별 경향"
      ],
      trendTabs: [
        "의류",
        "악세사리류",
        "제과점/아이스크림점",
        "커피/음료전문점",
        "패스트푸드점",
        "한식",
        "일식/생선회집",
        "중식",
        "양식",
        "주점",
        "편의점",
        "숙박",
        "헬스장",
        "미용원/피부미용원",
        "화장품점",
      ],
      chartData: {
        의류: {label: [], data1: [], data2: []},
        악세사리류: {label: [], data1: [], data2: []},
        "제과점/아이스크림점": {label: [], data1: [], data2: []},
        "커피/음료전문점": {label: [], data1: [], data2: []},
        패스트푸드점: {label: [], data1: [], data2: []},
        한식: {label: [], data1: [], data2: []},
        "일식/생선회집": {label: [], data1: [], data2: []},
        중식: {label: [], data1: [], data2: []},
        양식: {label: [], data1: [], data2: []},
        주점: {label: [], data1: [], data2: []},
        편의점: {label: [], data1: [], data2: []},
        숙박: {label: [], data1: [], data2: []},
        헬스장: {label: [], data1: [], data2: []},
        "미용원/피부미용원": {label: [], data1: [], data2: []},
        화장품점: {label: [], data1: [], data2: []},
      },
      lowerLine: [],
      upperLine: [],
      trendNumber: -1,
      trendFlag: -1,
      trendIndex: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      trendreset: false,
      trendsDetail: false,
    }
  },
  mounted() {
    for (let i = 0; i < 60; ++i) {
      this.lowerLine.push(20)
      this.upperLine.push(80)
    }
    axios.get(`http://127.0.0.1:8000/api/trend_by_tob`)
    .then(res => {
      // console.log(res.data)
      const dataset = res.data
      for (let i = 0; i < this.trendTabs.length; ++i) {
        for (let j = 0; j < dataset[`${this.trendTabs[i]}`]["new_date"].length; ++j) {
          this.chartData[`${this.trendTabs[i]}`]["label"].push(dataset[`${this.trendTabs[i]}`]["new_date"][i].slice(5,10))
        }
        this.chartData[`${this.trendTabs[i]}`]["data1"] = dataset[`${this.trendTabs[i]}`]["kdj_d"]
        this.chartData[`${this.trendTabs[i]}`]["data2"] = dataset[`${this.trendTabs[i]}`]["kdj_j"]
      }
    })
    .catch(err => {
      console.log(err)
    })
  },
  methods: {
    goHome() {
      router.push("/")
    },
    showTrendsDetail() {
      if (this.trendsDetail == false) {
        this.trendsDetail = true
      } else {
        this.trendsDetail = false
      }
    },
    changeTrendNumber(i) {
      this.trendNumber = i
    },
    drawChart(i) {
      var ctx = document.getElementById(`chart${this.trendNumber}`).getContext('2d');
      var chart = new Chart(ctx, {
          // The type of chart we want to create
          type: 'line',
          // The data for our dataset
          data: {
              labels: this.chartData[`${this.trendTabs[i]}`]["label"],
              datasets: [{
                label: 'Slow K',
                backgroundColor: 'blue',
                borderColor: 'blue',
                data: this.chartData[`${this.trendTabs[i]}`]["data1"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0.5,
              },{
                label: 'Slow D',
                backgroundColor: 'red',
                borderColor: 'red',
                data: this.chartData[`${this.trendTabs[i]}`]["data2"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0.5,
              }, {
                label: "LowerLine",
                borderColor: 'black',
                backgroundColor: 'black',
                data: this.lowerLine,
                fill: false,
                borderWidth: 3,
                pointStyle: "dash",
              }, {
                label: "UpperLine",
                borderColor: 'black',
                backgroundColor: 'black',
                data: this.upperLine,
                fill: false,
                borderWidth: 3,
                pointStyle: "dash",
              }
              ],
          },
          // Configuration options go here
          options: {
            title: {
                display: true,
                text: this.trendTabs[i],
                fontSize: 24,
                padding: 20,

            },
            scales: {
              yAxes: [{
                  ticks: {
                      max: 100,
                      min: 0,
                      stepSize: 10
                  }
              }]
            }
          }
      });
    },
    deleteTrends() {
      // console.log("aaaaaaaaaaa")
      this.trendreset = true
      for (let i = 0; i < this.trendTabs.length; ++i) {
          let target = document.getElementById(`btn${i}`)
          target.style = ""
          target = document.getElementById("report_box_trend_btn_all")
          target.style = ""
        }
    },
    async showTrends(value) {
      this.trendreset = false
      // console.log(this.chartData)
      if (value == "all") {
        this.trendFlag = true
        for (let i = 0; i < this.trendTabs.length; ++i) {
          // console.log(i)
          await this.changeTrendNumber(i)
          this.drawChart(i)
        }
        let target = document.getElementById("report_box_trend_btn_all")
        // console.log(target)
        if (target.style.length == 0) {
          target.style.color = "white"
          target.style.backgroundColor = "black"
        }
        for (let i = 0; i < this.trendTabs.length; ++i) {
          target = document.getElementById(`btn${i}`)
          target.style = ""
        }
      } else {
        this.trendFlag = false
        for (let i = 0; i < this.trendTabs.length; ++i) {
          if (this.trendTabs[i] == value) {
            await this.changeTrendNumber(i)
            this.drawChart(i)
            let target = document.getElementById(`btn${i}`)
            // console.log(target)
            if (target.style.length == 0) {
              target.style.color = "white"
              target.style.backgroundColor = "black"
            }
          } else {
            let target = document.getElementById(`btn${i}`)
            target.style = ""
            target = document.getElementById("report_box_trend_btn_all")
            target.style = ""
          }
        }
        
      }
    }
  }
}
</script>

<style scoped>
#FC_logo {
  float: left;
}
#FC_logo_img {
  width: 200px;
  height: 100px;
  cursor: pointer;
}
#FCAR_logo {
  float: right;
}
#FCAR_logo_img {
  width: 200px;
}
#report_docs {
  padding: 40px;
}
#report_header {
  border: 5px solid black;
  width: 50vw;
  height: 100px;
  margin: 10px auto;
  font-size: 48px;
  padding: 10px;
}
.report_tab {
  display: inline-block;
  width: 200px;
  height: 60px;
  font-size: 24px;
  padding: 10px;
  border: 1px solid black;
  /* cursor: pointer; */
}
.report_tab_a {
  text-decoration: none;
  color: black;
}
#report_box {
  border: 1px solid black;
  width: 80vw;
  margin: auto;
  height: 100%;
  padding: 20px;
}
#report_box_trend_btn_all {
  display: inline-block;
  width: 25vw;
  border: 1px solid black;
  padding: 2px;
  font-size: 1.3vw;
  margin: auto;
}
#report_box_trend_btn {
  display: inline-block;
  border: 1px solid black;
  width: 15vw;
  font-size: 1.3vw;
  padding: 2px;
}
.report_box_trend_btn_text {
  cursor: pointer;
}
.report_box_trend_btn_text:hover {
  background-color: black;
  color: white;
}
.report_box_trend_chart {
  border: 1px solid black;
  margin: 10px auto;
}
#report_box_trend_btn_text_detail {
  cursor: pointer;
  background-color: gray;
  color: white;
}
#report_box_trends_read_box {
  border: 1px solid black;
  width: 60vw;
  margin: auto;
  background-color: gray;
  padding: 20px;
}
</style>