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
        <a :href="`#section${i}`" class="report_tab_a">
          {{ value }}
        </a>
      </div>
    </div>
    <div id="report_box">
      <div id="section0">
        <div id="section0Header">
          개요
        </div>
        <div class="sectionDetail">
          최근 리뷰를 기반으로 TF-IDF 분석을 하였으며, 최근 두드러지는 단어를 워드클라우드로 표현하였다.
        </div>
        <div id="WC" style="width: 100%; height: 500px;" />
      </div>


      <div id="section1">
        <div class="sectionHeader">
          나이별 소비 순위
        </div>
        <b />
        <div class="sectionDetail">
          <b>20대</b> : 패션, 미용, 취미, 유흥, 등 여가활동에 많은 금액을 투자함. 자기 보유 차량이 없는 특징때문에 택시비에 많은 지출을 함. 자기개발, 타다, 카카오 모빌리티 등에 높은 관심도를 보일 것. <br>
          <b>30대</b> : 보험, 자차관련 지출이 폭발적으로 증가하고 생활 관련 지출이 증가함. 사회인으로서 생활이 안정되면서 서비스들에 갖는 관심도가 증가함. <br>
          <b>40대</b> : 20대에 관심을 가졌던 부분들에서 가장 큰 폭으로 하락한 나이대. 교육비, 보험료 지출이 다시 한 번 상승하는 모습이며, 이는 자식들의 지출을 대변함. 가족을 자극하는 마케팅이 필요함. <br>
          <b>50대</b> : 전체적으로 40대와 비슷한 양상을 보이지만 소득이 감소하며 이는 통신비, 취미, 미용 관련 비용이 하락함.
        </div>
        <div v-for="(value, i) in generationTabs" id="report_box_generation_btn" :key="value">
          <div :id="`generationBtn${i}`" class="report_box_generation_btn_text" @click="showGeneration(i)">
            {{ value }}
          </div>
        </div>
        <div v-for="(value, i) in generationTabs" id="report_box_generation_charts" :key="i">
          <canvas :id="`generationChart${i}`" class="report_box_generation_chart" />
        </div>
      </div>
      


      <div id="section2">
        <div class="sectionHeader">
          지역별 소비 순위
        </div>
        <div class="sectionDetail">
          지역별 소비량을 성별, 나이대별, 시간대별로 분석하였고, 서울내 소비 지역 top3를 산출하였다.  <br>
          <b>성별 최대 소비 지역</b>의 차이는 지역에 따른 직장인 성별의 비중이 이유였다. <br>
          또한 서울 내 <b>소비 지역 Top3</b>의 경우 대기업의 본사가 몰려있는 중구가 소비량이 가장 높았고, 강남구, 구로구 순이었다.
          강남구의 경우 많은 유동인구와 높은 경제 수준이 이유였고, 구로구는 각종 공단이 위치해 있어서 국내 최대 유동인구 덕분이었다.  <br>
          서울 소비 Top5의 지역의 <b>나이대별 소비 순위</b>는, 중구의 경우 20대 ~ 40대의 직장인들이 주 고객층이었고,
          강남의 경우 10대, 20대의 소비량은 적었지만, 어느정도 경제력이 뒷받침 되기 시작하는 30대 이후로는 큰손들이 몰려 있어서 가파른 상승을 이루었다.
          반면 용산의 경우 각종 놀이 시설과 전자상가, 아이파크몰 등으로 인해 10대의 소비량이 강세였으나, 20대 이후 부터는 소비량이 하락하였다.  <br>
          <b>시간대별 순위</b>로는 중구와 강남이 대부분의 시간에서 1, 2위를 양분하였으나 일반적인 소비가 줄고 유흥의 소비 비중이 증가하는 새벽에는 구로구가 2위를 차지하였다.
        </div>
        <img src="../../public/images/report/consumption_gender.png" alt="consumption_gender" class="report_box_location_imgs">
        <img src="../../public/images/report/consumption_top3.png" alt="consumption_top3" class="report_box_location_imgs">
        <div v-for="(value, i) in locationTabs" id="report_box_location_btn" :key="i">
          <div :id="`locationBtn${i}`" class="report_box_location_btn_text" @click="showLocation(i)">
            {{ value }} 지역순위
          </div>
        </div>
        <canvas id="locationchart0" class="report_box_location_chart" />
        <canvas id="locationchart1" class="report_box_location_chart" />
      </div>




      <div id="section3">
        <div class="sectionHeader">
          상권 분석
        </div>
        <div class="sectionDetail">
          슈퍼마켓, 편의점 등 음식점과 소매업을 제외하고 업종 형태별 매출 순위를 지역별로 분석하였다. <br>
          <b>도봉구</b>는 농, 수, 축협 판매장이 최대 매출을 보였고,
          <b>동대문구</b>는 의류 도매시장의 존재로 기타의류가 최대 매출을 보였다. 
          <b>동작구</b>는 특이하게 택시의 매출이 가장 높았다.
          <b>은평구</b>는 비디오/게임방, 
          <b>강북구</b>는 미용실,
          <b>강동구</b>는 대형마트의 매출이 가장 높았다. <br>
          <b>강남구</b>는 대형 사교육 업체가 몰려 있는 만큼 입시, 고시학원의 매출이 가장 높았고,
          <b>강서구</b>는 김포공항을 옆에 두고 있어서 항공사의 매출이 가장 높았다. 
          <b>금천구</b>는 가산디지털단지를 끼고 있어서 대형 쇼핑센터의 매출이 가장 높고,
          <b>구로구</b>는 음식점과 소매업을 제외후엔 일반, 치과, 한방병원의 매출이 가장 높았다. <br>
          <b>관악구</b>는 서울대를 끼고 있어서인지, 학습지의 매출이 가장 높고,
          <b>광진구</b>는 건국대 주변으로 번화가가 형성되어 있어서 기성복의 매출이 가장 높았다. 
          <b>종로구</b>는 구로구와 마찬가지로 일반, 치과, 한방병원의 매출이 가장 높았다.
          <b>중랑구</b>는 비디오/게임방의 매출이 가장 높았고,
          <b>중구</b>는 택시의 매출이 가장 높았다. 이를 토대로 강북의 택시 집합소는 중구, 강남은 동작구로 예상 할 수 있었다. <br>
          <b>마포구</b>는 홍익대를 기점으로 기성복의 매출이 가장 높았고,
          <b>노원구</b>는 서울 시내 가장 많은 인구수를 보유하고 있어서 대형마트의 매출이 가장 높았다.
          <b>서초구</b>는 고속버스터미널, 센트럴시티, 남부터미널을 기반으로 고속/시외버스의 매출이 가장 높았고,
          <b>서대문구</b>는 연세 세브란스 병원 덕분에 종합병원의 매출이 가장 높았다. <br>
          <b>성북구</b>는 비디오/게임방이 가장 높고,
          <b>송파구</b>는 롯데시티를 기반으로 백화점의 매출이 가장 높았다. 
          <b>성동구</b>는 성수 공단을 제치고 입시, 고시학원의 매출이 가장 높았다. 
          <b>양천구</b>는 목동을 기반으로 입시, 고시학원의 매출이 가장 높고,
          <b>용산구</b>는 역시 전자제품의 메출이 가장 높았으며,
          <b>영등포구</b>는 여의도와 타임스퀘어를 기반으로 전자제품의 매출이 두드러졌다.
        </div>
        <div v-for="i in top3Location.length" :key="top3Location[i-1][0]" style="display: inline-block;">
          <div :id="`top3Btn${i}`" class="report_box_top3_location_text" @click="showTop3Location(i)">
            {{ top3Location[i-1][0] }}
          </div>
        </div>
        <div v-for="i in top3Location.length" :key="top3Location[i-1][2]" style="display: inline-block;">
          <img :id="`top3Location${i}`" :src="`${top3Location[i-1][1]}`" :alt="`${top3Location[i-1][2]}`" class="report_box_top3_location_imgs">
        </div>
        <div class="sectionHeader">
          상권 추천
        </div>
        <div class="sectionDetail">
          각 지역 총 결제 금액을 가게수로 나누어, 지역 내 가게의 평균 결제 금액이 높은 순으로 나열하였다.<br>
          서울시 내 인구 수가 가장 높은 노원구가 전체적인 부분에서 1위에 위치했다. <br>
          <b>패스트푸드점</b>은 직장인들이 많이 위치한 종로에서 강세를 보였고,
          <b>한식</b>은 고급화가 많이 이루어진 만큼, 서초구와 강남구에서 높은 평균 매출을 기록했다. 
          특히 강남구는 패스트푸드를 제외한 모든 분야에서 순위권에 위치하였으며, 일반 주점에서는 1위를 기록하였다.<br>
          <b>양식</b>은 여의도가 위치한 영등포에서 강세를 보였고,
          <b>일식</b>은 예상외로 관악구가 2위에 자리잡았다. <br>
          <b>주점</b>,
          <b>제과점</b>에서는 서초구가 2위에 위치하였고, 
          <b>중식</b>은 노원, 강남, 서초의 순서를 띄었다.
          <b>커피/음료전문점</b>은 기업이 몰려있는 중구가 8개의 분야중 유일하게 나타났으며, 1위를 차지했다.
        </div>
        <div v-for="i in top3Cate.length" :key="top3Cate[i-1][0]" style="display: inline-block;">
          <div :id="`top3CateBtn${i}`" class="report_box_top3_cate_text" @click="showTop3Cate(i)">
            {{ top3Cate[i-1][0] }}
          </div>
        </div>
        <div v-for="i in top3Cate.length" :key="top3Cate[i-1][2]" style="display: inline-block;">
          <img :id="`top3Cate${i}`" :src="`${top3Cate[i-1][1]}`" :alt="`${top3Cate[i-1][2]}`" class="report_box_top3_cate_imgs">
        </div>
      </div>



      <div id="section4">
        <div class="sectionHeader">
          체인점 비교
        </div>
        <div class="sectionDetail">
          사업 형태별 평점과 체인 사업자의 평점 순위를 비교하였다. <br>
          <b>형태별 분석</b>에서 체인점의 경우 대중화와 수익성을 목표로 두었기에 평점은 낮은 경향을 보였다. <br>
          <b>체인점</b>의 경우 선택지가 다양하고 불호가 낮은 타는 베스킨라빈스가 4.0으로 1위를 차지하였고, 명랑핫도그가 3.8로 10위에 자리잡았다.
          상위 10개 중 5개가 카페, 디저트류인걸로 보아 후식류 체인점의 강세가 두드러졌다. 그리고 미스사이공의 경우 가성비에서 고점을 받은걸로 보인다.
        </div>
        <div v-for="(value, i) in chainTabs" id="report_box_chain_btn" :key="i">
          <div :id="`chainBtn${i}`" class="report_box_chain_btn_text" @click="showChain(i)">
            {{ value }}
          </div>
        </div>
        <div id="report_box_chain_btn_text_detail" @click="showChainDetail()">
          그래프 보는법
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
        <canvas id="chainchart1" class="report_box_chain_chart" />
        <canvas id="chainchart2" class="report_box_chain_chart" />
      </div>

      <div id="section5">
        <div class="sectionHeader">
          업종별 경향 비교
        </div>
        <div class="sectionDetail">
          초단기, 단기 경향을 수치화하여 그래프로 나타낸 것으로 업종별 경향을 파악할 수 있게 하였다. <br>
          모든 업종에서 두드러지게 나타나는 특성은 9/13 추석을 기점으로 하락세에서 상승세로 변한다는 점이다. <br>
          <b>한식, 양식, 일식, 중식, 패스트푸드</b>의 경우 단기간 초회복을 이루었고, <b>제과/아이스크림, 커피/음료</b>의 경우 꾸준한 회복세를 보였다.
          <b>헬스장</b>의 경우 추석을 기점으로 수직상승을 이루었고, 정확히 한달 후 비슷한 경향을 보였다.
          그리고 <b>숙박, 미용/피부</b>의 경우 추석 이후 두드러지는 성장은 없었지만 주단위의 규칙성을 보여주었다.
        </div>
        <div v-for="(value, i) in trendTabs" id="report_box_trend_btn" :key="i">
          <div :id="`trendBtn${i}`" class="report_box_trend_btn_text" @click="showTrends(i)">
            {{ value }}
          </div>
        </div>
        <div id="report_box_trend_btn_all">
          <div id="report_box_trend_btn_text_detail" @click="showTrendsDetail()">
            그래프 보는법
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
        <div v-for="(value, i) in trendTabs" id="report_box_trend_all_chart" :key="value">
          <canvas :id="`trendchart${i}`" class="report_box_trend_chart" />
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
        "나이별",
        "지역별",
        "상권",
        "체인점",
        "업종별 경향"
      ],
      top3Location: [
        ["도봉구", "/images/report/dobong_top3.png", "dobong_top3"],
        ["동대문구", "/images/report/dongdaemoon_top3.png", "dongdaemoon_top3"],
        ["동작구", "/images/report/dongjak_top3.png", "dongjak_top3"],
        ["은평구", "/images/report/eunpeong_top3.png", "eunpeong_top3"],
        ["강북구", "/images/report/gangbook_top3.png", "gangbook_top3"],
        ["강동구", "/images/report/gangdong_top3.png", "gangdong_top3"],
        ["강남구", "/images/report/gangnam_top3.png", "gangnam_top3"],
        ["강서구", "/images/report/gangseo_top3.png", "gangseo_top3"],
        ["금천구", "/images/report/geumcheon_top3.png", "geumcheon_top3"],
        ["구로구", "/images/report/guro_top3.png", "guro_top3"],
        ["관악구", "/images/report/gwanak_top3.png", "gwanak_top3"],
        ["광진구", "/images/report/gwangjin_top3.png", "gwangjin_top3"],
        ["종로구", "/images/report/jongro_top3.png", "jongro_top3"],
        ["중랑구", "/images/report/joongrang_top3.png", "joongrang_top3"],
        ["중구", "/images/report/joongu_top3.png", "joongu_top3"],
        ["마포구", "/images/report/mapo_top3.png", "mapo_top3"],
        ["노원구", "/images/report/nowon_top3.png", "nowon_top3"],
        ["서초구", "/images/report/seocho_top3.png", "seocho_top3"],
        ["서대문구", "/images/report/seodaemoon_top3.png", "seodaemoon_top3"],
        ["성북구", "/images/report/seongbook_top3.png", "seongbook_top3"],
        ["송파구", "/images/report/songpa_top3.png", "songpa_top3"],
        ["성동구", "/images/report/sungdong_top3.png", "sungdong_top3"],
        ["양천구", "/images/report/yangcheon_top3.png", "yangcheon_top3"],
        ["용산구", "/images/report/yongsan_top3.png", "yongsan_top3"],
        ["영등포구", "/images/report/youngdeungpo_top3.png", "youngdeungpo_top3"],
      ],
      top3Cate: [
        ["패스트푸드", "/images/report/fastfood_top3.png", "fastfood_top3"],
        ["한식", "/images/report/korea_top3.png", "korea_top3"],
        ["양식", "/images/report/pasta_top3.png", "pasta_top3"],
        ["일반주점", "/images/report/alchol_top3.png", "alchol_top3"],
        ["일식/생선회집", "/images/report/sasimi_top3.png", "sasimi_top3"],
        ["제과/아이스크림점", "/images/report/bread_top3.png", "bread_top3"],
        ["중식", "/images/report/chinese_top3.png", "chinese_top3"],
        ["커피/음료전문점", "/images/report/cafe_top3.png", "cafe_top3"],
      ],
      lowerLine: [],
      upperLine: [],
      trendsDetail: false,
      chainDetail: false,
    }
  },
  computed: {
    ...mapState({
      trendChartData: state => state.data.trendChartData,
      trendTabs: state => state.data.trendTabs,
      chainChartData: state => state.data.chainChartData,
      chainTabs: state => state.data.chainTabs,
      locationChartData: state => state.data.locationChartData,
      locationTabs: state => state.data.locationTabs,
      generationChartData: state => state.data.generationChartData,
      generationTabs: state => state.data.generationTabs,
    })
  },
  async mounted() {
    this.checkNavbar()
    setTimeout(() => {
      var tags = [
        '카페', '커피', '빵', '돈', '돈까스', '마카롱', '케이크', '떡볶이',  '인테리어', '비빔밥', '술', '닭', '막창',
        '향', '만두', '국수', '티', '밀떡', '순대', '칼국수', '맥주', '냉면', '라떼', '주차', '파스타', '해물', '양념', '위치', '김치', 
        '수육', '테이블', '백종원', '크림', '갈비', '덮밥', '디저트', '삼겹살', '튀김', '사진', '곱창',  '예약', 
        '국밥', '우동', '구이', '육수', '제주', '카레', '회', '안주', '데이트','볶음', '짬뽕', 
        '쌀떡', '정식', '짜장', '고급', '동네', '볶음밥', '찜', '새우', '찌개', '기본','신선', '점심', '간이', '김밥', '메밀', 
        '치즈', '골목', '전문', '된장', '돼지', '쪽갈비', '코스', '퀄리티', '탕', '바지락', '포장', '조림', '가족', '탕수육',  '죽'
      ]
      var word_array = [];
      for (var i = 0; i < tags.length; i++) {
        let tmp = { text: tags[i], weight: tags.length - i * 5 };
        word_array.push(tmp);
      }
      $(function() {
        $("#WC").jQCloud(word_array);
      });
    }, 1000)

    for (let i = 0; i < 60; ++i) {
      this.lowerLine.push(20)
      this.upperLine.push(80)
    }
    await this.goTrendChartData()
    await this.goChainChartData()
    await this.goLocationChartData()
    await this.goGenerationChartData()
      
  },
  destroyed() {
    this.checkNavbar()
  },
  methods: {
    ...mapActions("data", ["checkNavbar"]),
    ...mapActions("data", ["goTrendChartData"]),
    ...mapActions("data", ["goChainChartData"]),
    ...mapActions("data", ["goLocationChartData"]),
    ...mapActions("data", ["goGenerationChartData"]),
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
    drawLineChart(i) {
      var ctx = document.getElementById(`trendchart${i}`).getContext('2d');
      var chart = new Chart(ctx, {
          type: 'line',
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
    async showTrends(idx) {
      // console.log(idx)
      var target = document.getElementById(`trendBtn${idx}`)
      if (target.style.color == "") {
        target.style.color = "white"
        target.style.backgroundColor = "black"
        document.getElementById(`trendchart${idx}`).style.display = "block"
      } else {
        target.style.color = ""
        target.style.backgroundColor = ""
        document.getElementById(`trendchart${idx}`).style.display = "none"
      }
      await this.drawLineChart(idx)
    },
    
    showChainDetail() {
      if (this.chainDetail == false) {
        this.chainDetail = true
      } else {
        this.chainDetail = false
      }
    },
    async showChain(idx) {
      var target = document.getElementById(`chainBtn${idx}`)
      if (target.style.color == "") {
        target.style.color = "white"
        target.style.backgroundColor = "black"
        document.getElementById(`chainchart${idx+1}`).style.display = "block"
      } else {
        target.style.color = ""
        target.style.backgroundColor = ""
        document.getElementById(`chainchart${idx+1}`).style.display = "none"
      }      
      if (idx === 0) {
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

    drawLocationChart(i) {
      var ctx = document.getElementById(`locationchart${i}`).getContext('2d');
      var chart = new Chart(ctx, {
          type: 'line',
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
                    tension: 0
                }
            }
          }
      });
    },

    async showLocation(idx) {
      var target = document.getElementById(`locationBtn${idx}`)
      if (target.style.color == "") {
        target.style.color = "white"
        target.style.backgroundColor = "black"
        document.getElementById(`locationchart${idx}`).style.display = "block"
      } else {
        target.style.color = ""
        target.style.backgroundColor = ""
        document.getElementById(`locationchart${idx}`).style.display = "none"
      }
      this.drawLocationChart(idx)
    },
    showTop3Location(i) {
      var target = document.getElementById(`top3Location${i}`)
      var target2 = document.getElementById(`top3Btn${i}`)
      if (target2.style.color == "") {
        target2.style.color = "white"
        target2.style.backgroundColor = "black"
      } else {
        target2.style.color = ""
        target2.style.backgroundColor = ""
      }
      if (target.style.display) {
        target.style.display = ""
      } else {
        target.style.display = "inline-block"
      }
    },
    showTop3Cate(idx) {
      var target2 = document.getElementById(`top3CateBtn${idx}`)
      var target = document.getElementById(`top3Cate${idx}`)
      if (target2.style.color == "") {
        target2.style.color = "white"
        target2.style.backgroundColor = "black"
      } else {
        target2.style.color = ""
        target2.style.backgroundColor = ""
      }
      if (target.style.display) {
        target.style.display = ""
      } else {
        target.style.display = "inline-block"
      }
    },

    drawGenerationChart(idx) {
      var ctx = document.getElementById(`generationChart${idx}`).getContext('2d');
      var chart = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: [
              "교육비", "미용", "보험료", "생활용품", "세금 및 기타 요금", "식생활", "여행 및 숙박", "유흥",
              "의료", "자동차/주유", "취미", "택시비", "통신비", "패션잡화"
            ],
              datasets: [{
                backgroundColor: [
                  "rgb(255, 50, 100)",
                  "rgb(255, 175, 100)",
                  "rgb(239, 252, 101)",
                  "rgb(149, 250, 99)",
                  "rgb(112, 250, 120)",
                  "rgb(113, 252, 207)",
                  "rgb(106, 207, 255)",
                  "rgb(95, 105, 255)",
                  "rgb(147, 106, 255)",
                  "rgb(239, 110, 255)",
                  "rgb(255, 105, 176)",
                  "rgb(255, 105, 220)",
                  "rgb(170, 61, 250)",
                  "rgb(0, 0, 100)",
                ],
                data: [
                  (this.generationChartData[`${this.generationTabs[idx]}`]["교육비"][0]),
                  this.generationChartData[`${this.generationTabs[idx]}`]["미용"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["보험료"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["생활용품"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["세금 및 기타 요금"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["식생활"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["여행 및 숙박"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["유흥"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["의료"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["자동차/주유"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["취미"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["택시비"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["통신비"][0],
                  this.generationChartData[`${this.generationTabs[idx]}`]["패션잡화"][0]
                ],
              },
              {
                backgroundColor: [
                  "rgb(255, 50, 100)",
                  "rgb(255, 175, 100)",
                  "rgb(239, 252, 101)",
                  "rgb(149, 250, 99)",
                  "rgb(112, 250, 120)",
                  "rgb(113, 252, 207)",
                  "rgb(106, 207, 255)",
                  "rgb(95, 105, 255)",
                  "rgb(147, 106, 255)",
                  "rgb(239, 110, 255)",
                  "rgb(255, 105, 176)",
                  "rgb(255, 105, 220)",
                  "rgb(170, 61, 250)",
                  "rgb(0, 0, 100)",
                ],
                data: [
                  (this.generationChartData[`${this.generationTabs[idx]}`]["교육비"][1]),
                  this.generationChartData[`${this.generationTabs[idx]}`]["미용"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["보험료"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["생활용품"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["세금 및 기타 요금"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["식생활"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["여행 및 숙박"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["유흥"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["의료"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["자동차/주유"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["취미"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["택시비"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["통신비"][1],
                  this.generationChartData[`${this.generationTabs[idx]}`]["패션잡화"][1]
                ],
              }],
          },
          options: {
            title: {
                display: true,
                text: this.generationTabs[idx],
                fontSize: 24,
                padding: 20,
            },
          }
      });
    },
    showGeneration(idx) {
      var target = document.getElementById(`generationBtn${idx}`)
      if (target.style.color == "") {
        target.style.color = "white"
        target.style.backgroundColor = "black"
        document.getElementById(`generationChart${idx}`).style.display = "block"
      } else {
        target.style.color = ""
        target.style.backgroundColor = ""
        document.getElementById(`generationChart${idx}`).style.display = "none"
      }
      this.drawGenerationChart(idx)
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
  text-align: center;
  background-color: white;
}
#report_header {
  border: 5px solid black;
  width: 50vw;
  height: 100px;
  margin: 10px auto;
  font-size: 3vw;
  padding: 10px;
}
.report_tab {
  display: inline-block;
  width: 13vw;
  height: 4vw;
  font-size: 1.8vw;
  font-weight: 500;
  padding: 10px;
  border: 1px solid black;
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
#section0Header {
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
.sectionDetail {
  text-align: start;
  font-size: 1.5vw;
  margin-left: 20px;
}
#report_box_trend_btn_all {
  display: inline-block;
  width: 18vw;
  border: 1px solid black;
  padding: 2px;
  font-size: 1.3vw;
  margin: auto;
}
#report_box_trend_btn {
  display: inline-block;
  border: 1px solid black;
  width: 18vw;
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
/* #report_box_trend_all_chart {
  width: 100%;
} */
.report_box_trend_chart {
  display: none;
  width: 100%;
  border: 1px solid black;
  margin-top: 10px;
}
#report_box_trend_btn_text_detail {
  width: 18vw;
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
#report_box_chain_btn {
  display: inline-block;
  border: 1px solid black;
  width: 25vw;
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
  display: none;
  width: 100%;
  border: 1px solid black;
  margin-top: 10px;
}
#report_box_chain_btn_text_detail {
  display: inline-block;
  border: 1px solid black;
  width: 25vw;
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
  width: 35vw;
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
.report_box_top3_location_imgs {
  width: 35vw;
  margin: 1vw;
  display: none;
}
.report_box_top3_location_text {
  border: 1px solid black;
  width: 15vw;
  display: inline-block;
}
.report_box_top3_location_text:hover {
  color: white;
  background-color: black;
  cursor: pointer;
}
.report_box_top3_cate_imgs {
  width: 35vw;
  margin: 1vw;
  display: none;
}
.report_box_top3_cate_text {
  border: 1px solid black;
  width: 18vw;
  display: inline-block;
}
.report_box_top3_cate_text:hover {
  color: white;
  background-color: black;
  cursor: pointer;
}
#report_box_generation_btn {
  display: inline-block;
  border: 1px solid black;
  width: 18vw;
  font-size: 1.3vw;
  padding: 2px;
}
.report_box_generation_btn_text {
  cursor: pointer;
}
.report_box_generation_btn_text:hover {
  background-color: black;
  color: white;
}
#report_box_generation_charts {
  width: 100%;
}
.report_box_generation_chart {
  display: none;
  border: 1px solid black;
  margin-top: 10px;
  width: 100%;
}
.report_box_location_chart {
  display: none;
  width: 100%;
  border: 1px solid black;
  margin-top: 10px;
}
</style>