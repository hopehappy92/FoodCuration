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
      <div id="section1">
        <div id="section1Header">
          개요
        </div>
        
      </div>
      


      <div id="section2">
        <div class="sectionHeader">
          지역별순위
        </div>
        <img src="../../public/images/report/consumption_gender.png" alt="consumption_gender" class="report_box_location_imgs">
        <img src="../../public/images/report/consumption_top3.png" alt="consumption_top3" class="report_box_location_imgs">
        <div v-for="(value, i) in locationTabs" id="report_box_location_btn" :key="i">
          <div :id="`locationBtn${i}`" class="report_box_location_btn_text" @click="showLocation(i)">
            {{ value }} 지역순위
          </div>
        </div>
        <div id="report_box_location_btn_reset">
          <div id="report_box_location_btn_text_reset" @click="deleteLocation()">
            초기화
          </div>
        </div>
        <canvas v-if="locationFlag == true && locationReset == false" id="locationchart0" />
        <canvas v-else-if="locationFlag == false && locationReset == false" id="locationchart1" />
      </div>




      <div id="section3">
        <div class="sectionHeader">
          상권 추천
        </div>
      </div>



      <div id="section4">
        <div class="sectionHeader">
          체인점 비교
        </div>
        <div v-for="(value, i) in chainTabs" id="report_box_chain_btn" :key="i">
          <div :id="`chainBtn${i}`" class="report_box_chain_btn_text" @click="showChain(i)">
            {{ value }}
          </div>
        </div>
        <div id="report_box_chain_btn_text_detail" @click="showChainDetail()">
          그래프 보는법
        </div>
        <div id="report_box_chain_btn" class="report_box_chain_btn_text" @click="deleteChain()">
          초기화
        </div>
        <div v-if="chainDetail">
          <div id="report_box_chain_read_box">
            <b style="font-size: 32px; color: white;">비체인 / 체인 / 전체 평점비교</b><br>
            <!-- <br> -->
            <div style="text-align: start; font-size: 18px; line-height: 30px;">
              - 개인사업자, 체인점, 전체 음식점 사이 평점 비교
            </div>
            <br>
            <br>
            <b style="font-size: 32px; color: white;">체인점 평점 순위</b><br>
            <!-- <br> -->
            <div style="text-align: start; font-size: 18px; line-height: 30px;">
              - 체인점 평점 1위 부터 10위 까지의 순위
            </div>
          </div>
        </div>
        <canvas v-if="chainFlag == true && chainReset == false" id="chainchart1" class="report_box_chain_chart" />
        <canvas v-else-if="chainFlag == false && chainReset == false" id="chainchart2" class="report_box_chain_chart" />
      </div>

      <div id="section5">
        <div class="sectionHeader">
          업종별 경향 비교
        </div>
        <div v-for="(value, i) in trendTabs" id="report_box_trend_btn" :key="i">
          <div :id="`trendBtn${i}`" class="report_box_trend_btn_text" @click="showTrends(value)">
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
          <canvas v-if="trendFlag == false && trendreset == false" :id="`trendchart${trendNumber}`" class="report_box_trend_chart" />
          <div v-else-if="trendFlag == true && trendreset == false">
            <div v-for="(value, i) in trendTabs" id="report_box_trend_all_chart" :key="i">
              <canvas :id="`trendchart${i}`" class="report_box_trend_chart" />
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import router from "../router"
import { mapActions, mapState } from "vuex"

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
      lowerLine: [],
      upperLine: [],
      trendNumber: -1,
      trendFlag: -1,
      trendreset: false,
      trendsDetail: false,
      chainFlag: -1,
      chainReset: true,
      chainDetail: false,
      locationFlag: -1,
      locationReset: false,
      locationDetail: false,
    }
  },
  computed: {
    ...mapState({
      trendChartData: state => state.data.trendChartData,
      trendTabs: state => state.data.trendTabs,
      chainChartData: state => state.data.chainChartData,
      chainTabs: state => state.data.chainTabs,
      locationChartData: state => state.data.locationChartData,
      locationTabs: state => state.data.locationTabs
    })
  },
  async mounted() {
    for (let i = 0; i < 60; ++i) {
      this.lowerLine.push(20)
      this.upperLine.push(80)
    }
    await this.goTrendChartData()
    await this.goChainChartData()
    await this.goLocationChartData()
  },
  methods: {
    ...mapActions("data", ["goTrendChartData"]),
    ...mapActions("data", ["goChainChartData"]),
    ...mapActions("data", ["goLocationChartData"]),
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
    drawLineChart(i) {
      var ctx = document.getElementById(`trendchart${this.trendNumber}`).getContext('2d');
      var chart = new Chart(ctx, {
          // The type of chart we want to create
          type: 'line',
          // The data for our dataset
          data: {
              labels: this.trendChartData[`${this.trendTabs[i]}`]["label"],
              datasets: [{
                label: 'Slow K',
                backgroundColor: 'blue',
                borderColor: 'blue',
                data: this.trendChartData[`${this.trendTabs[i]}`]["data1"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0.5,
              },{
                label: 'Slow D',
                backgroundColor: 'red',
                borderColor: 'red',
                data: this.trendChartData[`${this.trendTabs[i]}`]["data2"],
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
        let target = document.getElementById(`trendBtn${i}`)
        target.style = ""
        target = document.getElementById("report_box_trend_btn_all")
        target.style = ""
      }
    },
    setTrendReset() {
      this.trendreset = true
    },
    async showTrends(value) {
      await this.setTrendReset()
      this.trendreset = false
      // console.log(this.chartData)
      if (value == "all") {
        this.trendFlag = true
        for (let i = 0; i < this.trendTabs.length; ++i) {
          // console.log(i)
          await this.changeTrendNumber(i)
          this.drawLineChart(i)
        }
        let target = document.getElementById("report_box_trend_btn_all")
        // console.log(target)
        if (target.style.length == 0) {
          target.style.color = "white"
          target.style.backgroundColor = "black"
        }
        for (let i = 0; i < this.trendTabs.length; ++i) {
          target = document.getElementById(`trendBtn${i}`)
          target.style = ""
        }
      } else {
        this.trendFlag = false
        for (let i = 0; i < this.trendTabs.length; ++i) {
          if (this.trendTabs[i] == value) {
            await this.changeTrendNumber(i)
            this.drawLineChart(i)
            let target = document.getElementById(`trendBtn${i}`)
            // console.log(target)
            if (target.style.length == 0) {
              target.style.color = "white"
              target.style.backgroundColor = "black"
            }
          } else {
            let target = document.getElementById(`trendBtn${i}`)
            target.style = ""
            target = document.getElementById("report_box_trend_btn_all")
            target.style = ""
          }
        }
      }
    },
    showChainDetail() {
      if (this.chainDetail == false) {
        this.chainDetail = true
      } else {
        this.chainDetail = false
      }
    },
    changeChainFlag(idx) {
      if (idx == 0) {
        this.chainFlag = true
      } else {
        this.chainFlag = false
      }
    },
    setChainReset() {
      this.chainReset = true
    },
    deleteChain() {
      this.chainReset = true
      for (let i = 0; i < this.chainTabs.length; ++i) {
        let target = document.getElementById(`chainBtn${i}`)
        target.style = ""
        target = document.getElementById("report_box_chain_btn")
        target.style = ""
      }
    },
    async showChain(idx) {
      await this.setChainReset()
      this.chainReset = false
      // console.log(idx)

      if (idx == 0) {
        var target = document.getElementById(`chainBtn0`)
        var nontarget = document.getElementById(`chainBtn1`)
      } else {
        target = document.getElementById(`chainBtn1`)
        nontarget = document.getElementById(`chainBtn0`)
      }
      target.style.color = "white"
      target.style.backgroundColor = "black"
      nontarget.style = ""
      
      if (idx === 0) {
        await this.changeChainFlag(idx)
        var ctx = document.getElementById(`chainchart1`).getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                datasets: [{
                  label: '비체인',
                  backgroundColor: 'red',
                  borderColor: 'red',
                  data: [this.chainChartData[`${this.chainTabs[0]}`]["score"][0]],
                }, {
                  label: '체인',
                  backgroundColor: 'blue',
                  borderColor: 'blue',
                  data: [this.chainChartData[`${this.chainTabs[0]}`]["score"][1]],
                }, {
                  label: '전체',
                  backgroundColor: 'green',
                  borderColor: 'green',
                  data: [this.chainChartData[`${this.chainTabs[0]}`]["score"][2]],
                }],
            },
            // Configuration options go here
            options: {
              scales: {
                yAxes: [{
                    ticks: {
                        max: 3.90,
                        min: 3.50,
                        stepSize: 0.02
                    }
                }]
              }
            }
        });
      } else {
        await this.changeChainFlag(idx)
        var ctx2 = document.getElementById(`chainchart2`).getContext('2d');
        var chart2 = new Chart(ctx2, {
            type: 'bar',
            data: {
                datasets: [{
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][0],
                  backgroundColor: 'red',
                  borderColor: 'red',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][0]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][1],
                  backgroundColor: 'orange',
                  borderColor: 'orange',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][1]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][2],
                  backgroundColor: 'yellow',
                  borderColor: 'yellow',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][2]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][3],
                  backgroundColor: 'green',
                  borderColor: 'green',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][3]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][4],
                  backgroundColor: 'blue',
                  borderColor: 'blue',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][4]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][5],
                  backgroundColor: 'navy',
                  borderColor: 'navy',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][5]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][6],
                  backgroundColor: 'purple',
                  borderColor: 'purple',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][6]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][7],
                  backgroundColor: 'black',
                  borderColor: 'black',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][7]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][8],
                  backgroundColor: 'gray',
                  borderColor: 'gray',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][8]],
                }, {
                  label: this.chainChartData[`${this.chainTabs[1]}`]["store_name"][9],
                  backgroundColor: 'pink',
                  borderColor: 'pink',
                  data: [this.chainChartData[`${this.chainTabs[1]}`]["score"][9]],
                }],
            },
            // Configuration options go here
            options: {
              scales: {
                yAxes: [{
                    ticks: {
                        max: 4.10,
                        min: 3.60,
                        stepSize: 0.05
                    }
                }]
              }
            }
        });
      }
    },
    
    // showChainDetail() {
    //   if (this.chainDetail == false) {
    //     this.chainDetail = true
    //   } else {
    //     this.chainDetail = false
    //   }
    // },
    changeLocationFlag(idx) {
      if (idx == 0) {
        this.locationFlag = true
      } else {
        this.locationFlag = false
      }
    },
    setLocationReset() {
      this.locationReset = true
    },
    deleteLocation() {
      this.locationReset = true
      for (let i = 0; i < this.locationTabs.length; ++i) {
        let target = document.getElementById(`locationBtn${i}`)
        target.style = ""
        target = document.getElementById("report_box_location_btn")
        target.style = ""
      }
    },

    drawLocationChart(i) {
      var ctx = document.getElementById(`locationchart${i}`).getContext('2d');
      var chart = new Chart(ctx, {
          // The type of chart we want to create
          type: 'line',
          // The data for our dataset
          data: {
              labels: this.locationChartData[`${this.locationTabs[i]}`]["index"],
              datasets: [{
                label: '강남구',
                backgroundColor: 'red',
                borderColor: 'red',
                data: this.locationChartData[`${this.locationTabs[i]}`]["강남구"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0.5,
              },{
                label: '구로구',
                backgroundColor: 'orange',
                borderColor: 'orange',
                data: this.locationChartData[`${this.locationTabs[i]}`]["구로구"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0.5,
              },{
                label: '마포구',
                backgroundColor: 'yellow',
                borderColor: 'yellow',
                data: this.locationChartData[`${this.locationTabs[i]}`]["마포구"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0.5,
              },{
                label: '용산구',
                backgroundColor: 'green',
                borderColor: 'green',
                data: this.locationChartData[`${this.locationTabs[i]}`]["용산구"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0.5,
              },{
                label: '중구',
                backgroundColor: 'blue',
                borderColor: 'blue',
                data: this.locationChartData[`${this.locationTabs[i]}`]["중구"],
                fill: false,
                borderWidth: 2,
                pointBorderWidth: 0,
              }
              ],
          },
          // Configuration options go here
          options: {
            title: {
                display: true,
                text: this.locationTabs[i],
                fontSize: 24,
                padding: 20,
            },
            scales: {
              xAxes: [{
                gridLines: {
                  borderDash: [5]
                },
              }],
              yAxes: [{
                // display: false,
                gridLines: {
                  borderDash: [5]
                },
                  ticks: {
                      max: 6,
                      min: 0,
                      stepSize: 1,
                      reverse: true
                  }
              }]
            },
            elements: {
                line: {
                    tension: 0 // disables bezier curves
                }
            }
          }
      });
    },

    async showLocation(idx) {
      await this.setLocationReset()
      this.locationReset = false
      await this.changeLocationFlag(idx)
      if (idx == 0) {
        var target = document.getElementById(`locationBtn0`)
        var nontarget = document.getElementById(`locationBtn1`)
      } else {
        target = document.getElementById(`locationBtn1`)
        nontarget = document.getElementById(`locationBtn0`)
      }
      target.style.color = "white"
      target.style.backgroundColor = "black"
      nontarget.style = ""
      // console.log(this.locationReset)
      // console.log(this.locationChartData)
      // console.log(this.locationTabs)
      this.drawLocationChart(idx)
    },
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
.report_tab:hover {
  background-color: gray;
}
.report_tab_a:hover {
  color: white;
}
#report_box {
  border: 1px solid black;
  width: 80vw;
  margin: auto;
  height: 100%;
  padding: 20px;
}
#section1Header {
  text-align: start;
  font-size: 2.5vw;
  font-weight: 600;
  margin: 0 0 10px 0
}
.sectionHeader {
  text-align: start;
  font-size: 2.5vw;
  font-weight: 600;
  margin: 40px 0 10px 0
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

#report_box_trend_all_chart {
  display: inline-block;
  width: 38vw;
}
#report_box_chain_btn {
  display: inline-block;
  border: 1px solid black;
  width: 18vw;
  font-size: 1.3vw;
  padding: 2px;
}
.report_box_chain_btn_text {
  cursor: pointer;
}
.report_box_chain_btn_text:hover {
  background-color: black;
  color: white;
}
.report_box_chain_chart {
  border: 1px solid black;
  margin: 10px auto;
}
#report_box_chain_btn_text_detail {
  display: inline-block;
  border: 1px solid black;
  width: 18vw;
  font-size: 1.3vw;
  padding: 2px;
  background-color: gray;
  color: white;
  cursor: pointer;
}
#report_box_chain_read_box {
  border: 1px solid black;
  width: 30vw;
  margin: auto;
  background-color: gray;
  padding: 30px 20px;
}
#report_box_location_btn {
  display: inline-block;
  border: 1px solid black;
  width: 25vw;
  font-size: 1.3vw;
  padding: 2px;
}
.report_box_location_btn_text {
  cursor: pointer;
}
.report_box_location_btn_text:hover {
  background-color: black;
  color: white;
}
#report_box_location_btn_reset {
  display: inline-block;
  border: 1px solid black;
  width: 25vw;
  font-size: 1.3vw;
  padding: 2px;
  background-color: gray;
  color: white;
}
#report_box_location_btn_text_reset {
  cursor: pointer;
}
.report_box_location_imgs {
  width: 35vw;
  margin: 1vw;
}
</style>