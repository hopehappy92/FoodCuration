<template>
  <div id="report_docs">
    <div id="FC_logo">
      <img id="FC_logo_img" src="../../public/images/logo_black.png" alt="logo">
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
      <pre>
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
          section5
        </div>
      </pre>
      <div id="section6">asdf</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tabs: [
        "개요",
        "지역별",
        "상권 추천",
        "체인점",
        "업종별 경향"
      ]
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
  border: 1px solid black;
  width: 50vw;
  height: 100px;
  margin: 10px auto;
  font-size: 48px;
  padding: 10px;
}
#report_tabbox {
  /* margin-right: 10.7vw; */
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
  height: 100%
}
</style>