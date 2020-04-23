<template>
  <div>
    <div class="nav">
      <div class="nav_inner_left" @click="goHome()">
        <img id="home_header_header_logo_img" src="../../public/images/logo_black.png" alt="Logo" />
        <!-- <i class="fab fa-drupal" />
        <span>Food Curation</span>-->
      </div>
      <div v-if="$store.state.data.navSearch" class="nav_innder_middle">
        <input
          v-model="storeName"
          type="text"
          placeholder="  식당명으로 맛집을 검색해보세요"
          v-model="storeName"
          @keyup="enterKey(storeName)"
        >
        <i class="fas fa-search" @click="goSearchPage(storeName)" />
      </div>
      <div v-if="islogined == false">
        <ul class="nav_inner_right">
          <li>
            <login>
              <button slot="click" class="nav_menu">로그인</button>
            </login>
          </li>
          <li>
            <button class="nav_menu" @click="goRegi()">회원가입</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <ul class="nav_inner_right">
          <li>
            <button class="nav_menu" @click="dologout()">로그아웃</button>
          </li>
          <li>
            <button class="nav_menu" @click="goMypage()">마이페이지</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../router";
import Login from "../components/Login";
import { mapState, mapActions, mapMutations } from "vuex";
// import { mdiHanger } from "@mdi/js";

export default {
  components: {
    Login
  },
  data() {
    return {
      storeName: ""
    };
  },
  computed: {
    ...mapState({
      islogined: state => state.data.isloggined
    })
  },
  methods: {
    ...mapActions("data", ["logout"]),
    ...mapActions("data", ["checkLogin"]),
    ...mapMutations("data", ["searchFromNav"]),
    goRegi() {
      router.push("/register");
    },
    goMypage() {
      const location = "/mypage/" + localStorage.getItem("pk");
      router.push(location);
    },
    dologout() {
      this.logout();
    },
    goHome() {
      router.push("/");
    },
    goSearchPage(storeName) {
      this.searchFromNav(storeName);
      router.push("/search");
    },
    enterKey(storeName) {
      if (window.event.keyCode == 13) {
        this.goSearchPage(storeName);
      }
    }
  },
  mounted() {
    this.checkLogin();
  }
};
</script>

<style scoped>
.nav {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  align-content: center;
  position: fixed;
  background: white;
  top: 0px;
  z-index: 100;
  width: 100%;
  padding-top: 15px;
  padding-bottom: 20px;
  border-bottom: black solid 3px;
}
.nav_inner_left:hover {
  cursor: pointer;
}
.nav_inner_left > i {
  color: black;
  padding-left: 24px;
  font-size: 40px;
}
.nav_inner_left > span {
  color: black;
  padding-left: 18px;
  font-size: 25px;
  font-family: "Comic Neue", cursive;
}
.nav_innder_middle {
  width: 30%;
  display: flex;
  margin-left: 200px;
}
.nav_innder_middle > input {
  background: #f1f1f1;
  width: 100%;
  height: 40px;
  border-radius: 10px;
}
.nav_innder_middle > i {
  font-size: 20px;
  padding: 5px;
  display: flex;
  align-items: center;
  position: relative;
  right: 30px;
}
.nav_innder_middle > i:hover {
  cursor: pointer;
}
.nav_inner_right {
  display: flex;
  list-style: none;
  padding-right: 24px;
}
.nav_inner_right > li {
  display: flex;
  align-items: center;
  padding: 12px 8px;
}
.nav_inner_right > li > div {
  display: flex;
  align-items: center;
}
.nav_inner_right > li > div > div > button {
  color: black;
  text-decoration-style: none;
}
.nav_inner_right > li > button {
  color: black;
}
input:focus::-webkit-input-placeholder {
  color: transparent;
  outline: none;
}
input:focus {
  outline: none;
}
.nav_menu {
  font-family: "Do Hyeon", sans-serif;
  font-size: 18px;
}
#home_header_header_logo_img {
  width: 150px;
  position: absolute;
  top: -6px;
  left: 0px;
}
</style>