<template>
  <div id="home_footer_main">
    <div id="home_footer_inner">
      <div id="a">
        <div class="home_footer_text">
          <img src="../../public/images/logo.png" alt="logo" style="width: 100px;">
        </div>
        <div class="home_footer_text">
          <PolicyPrivacy class="policy">
            <div slot="PP">
              개인정보 취급 방침
            </div>
          </PolicyPrivacy>
        </div>
        <div id="home_footer_bar" class="home_footer_text policy">
          |
        </div>
        <div class="home_footer_text">
          <PolicyService class="policy">
            <div slot="PS">
              이용 약관
            </div>
          </PolicyService>
        </div>
      </div>
      <div id="b">
        <div class="home_footer_text">
          상호: (주)푸드큐레이션
        </div>
        <div class="home_footer_text">
          주소: SSAFY
        </div>
      </div>
      <div id="c">
        <div class="home_footer_text">
          Email: contact@foodcuration.com
        </div>
        <div class="home_footer_text">
          Tel: 054-ssafy-ssafy
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PolicyPrivacy from "../components/PolicyPrivacy"
import PolicyService from "../components/PolicyService"

export default {
  components: {
    PolicyPrivacy,
    PolicyService
  },
  data() {
    return {
      dialog1: false,
      dialog2: false,
    }
  },
}
</script>

<style scoped>
#home_footer_main {
  background-color: rgb(31, 31, 31);
  height: 200px;
  color: white;
  padding: 20px 70px;
}
#a {
  display: flex;
}
#b {
  display: flex;
}
#c {
  display: flex;
}
.home_footer_text {
  margin-right: 10px;
}
.policy {
  cursor: pointer;
  transform: translateY(30%);
}
@media screen and (max-width: 600px) {
  #home_footer_main {
    height: 100px;
    padding: 5px 10px;
  }
  .home_footer_text {
    font-size: 10px;
  }
  .policy {
    cursor: pointer;
    transform: translateY(100%);
  }
  #home_footer_bar {
    transform: translateY(45%);
  }
}
</style>