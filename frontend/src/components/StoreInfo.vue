<template>
  <div>
    <div class="content_top">
      <div class="content_top_title">
        <div class="content_top_title_inner">
          <h1 class="store_title">{{ storeName }}</h1>
          <div id="card_rating">{{ storeScore }}</div>
        </div>
      </div>
      <div class="content_top_right">
        <button class="icon_review" @click="write">
          <i class="fas fa-pencil-alt" />
          <p>리뷰작성</p>
        </button>
        <button v-if="like" class="icon_like" @click="pushLike">
          <i class="fas fa-heart" />
          <p>취소</p>
        </button>
        <button v-else class="icon_like" @click="pushLike">
          <i class="far fa-heart" />
          <p>좋아요</p>
        </button>
      </div>
    </div>
    <p class="area">{{ storeArea }}</p>
    <table>
      <tbody>
        <tr>
          <th>주소</th>
          <td class="info_content">{{ storeAddress }}</td>
        </tr>
        <tr>
          <th>전화번호</th>
          <td class="info_content">{{ storeTel }}</td>
        </tr>
        <tr>
          <th>카테고리</th>
          <span v-for="(category, index) in storeCategories" :key="index">
            <span v-if="index > 0">/</span>
            <span class="info_content">{{ category }}</span>
          </span>
        </tr>
        <tr v-for="(menu, index) in storeMenuList" v-if="index < 5" :key="index">
          <th v-if="index == 0">메뉴</th>
          <th v-else />
          <div class="menu">
            <span class="info_content">{{ menu.menu_name }}</span>
            <span class="info_content">{{ menu.price }}원</span>
          </div>
        </tr>
      </tbody>
    </table>
    <form v-show="dialog" id="review_form" @submit.prevent="submit">
      <textarea v-model="content" class="message" placeholder="리뷰를 작성해주세요" rows="5" />
      <div class="review_update">
        <v-select
          id="my_page_head_option"
          v-model="score"
          :items="options"
          dense
          item-color="black"
          color="rgba(0, 0, 0, 1)"
          placeholder="평점"
        />
        <button type="submit" class="edit_btn">작성</button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import http from "../api/http"
// import { mdiHanger } from "@mdi/js";
import axios from "axios";

export default {
  props: {
    storeName: String,
    storeScore: Number,
    reviewCnt: Number,
    storeArea: String,
    storeTel: String,
    storeAddress: String,
    storeCategories: Array,
    storeMenuList: Array
  },
  data() {
    return {
      dialog: false,
      store: this.$route.params.storeId,
      score: 1,
      content: "",
      userId: localStorage.getItem("pk"),
      like: false,
      options: [
        { text: "1점!", value: 1 },
        { text: "2점!", value: 2 },
        { text: "3점!", value: 3 },
        { text: "4점!", value: 4 },
        { text: "5점!", value: 5 }
      ],
      options_value: 3
    };
  },
  methods: {
    ...mapActions("data", ["writeReview"]),
    submit: async function() {
      const params = {
        store: this.$route.params.storeId,
        user: this.userId,
        score: this.score,
        content: this.content
      };
      await this.writeReview(params)
        .then(this.$emit("add-to-review"))
        .then((this.dialog = false));
    },
    write() {
      if (this.dialog == false) {
        this.dialog = true;
      } else {
        this.dialog = false;
      }
    },
    submit() {
      console.log(this.userId, this.$route.params.storeId);
      const headers = {
        Authorization: "jwt" + localStorage.getItem("token")
      };
      http
        .post(
          `https://i02d106.p.ssafy.io:8765/api/store_reviews`,
          {
            store: this.$route.params.storeId,
            user: this.userId,
            score: this.score,
            content: this.content
          },
          {headers}
        )
        .then(this.$emit("add-to-review"))
        .then((this.dialog = false));
    },
    pushLike() {
      console.log(localStorage.getItem("pk"));
      console.log(this.$route.params.storeId);
      const headers = {
        Authorization: "jwt" + localStorage.getItem("token")
      };
      http
        .post(
          `/api/like_store`,
          {
            customuser_id: localStorage.getItem("pk"),
            store_id: this.$route.params.storeId
          },
          {headers}
        )
        .then(res => {
          console.log(res);
        });
      if (this.like == false) {
        this.like = true;
      } else {
        this.like = false;
      }
    },
    selectOption(value) {
      this.options_value = value;
    }
  }
};
</script>

<style scoped>
.main_content {
  width: 60%;
  display: flex;
  flex-flow: column nowrap;
  margin-left: 50px;
}
.area {
  font-size: 23px;
  border-bottom: solid #a5a79a 1px;
  padding-bottom: 10px;
  margin-left: 10px;
  font-family: "Jua", sans-serif;
  color: rgb(156, 155, 155);
}
.content_top {
  display: flex;
  flex-flow: row nowrap;
  align-items: baseline;
}
.menu {
  border-bottom: solid #d9d9d9 1px;
  width: max-content;
  margin-bottom: 5px;
}
.menu > :nth-child(2) {
  margin-left: 20px;
}
.store_title {
  display: inline-block;
  font-family: "Do Hyeon", sans-serif;
  font-size: 38px;
}
.store_title ~ span {
  font-size: 35px;
  color: orange;
  margin-left: 10px;
}
.content_top_title {
  width: 100%;
  display: flex;
  align-items: baseline;
  flex-direction: row nowrap;
  justify-content: left;
}
.content_top_title_inner {
  display: flex;
  align-items: baseline;
  margin-left: 10px;
}
.content_top_right {
  width: 20%;
  margin-right: 20px;
  display: flex;
  flex-flow: row nowrap;
}
.icon_review {
  margin-right: 30px;
}
.icon_review > i {
  font-size: 28px;
}
.icon_like > i {
  font-size: 30px;
  color: rgb(209, 18, 18);
}
.icon_like > p {
  font-size: 10px;
  color: rgb(155, 155, 155);
}
.icon_review > p {
  font-size: 10px;
  color: rgb(155, 155, 155);
}
table {
  width: 100%;
  margin-left: 10px;
}
th {
  text-align: left;
  padding-bottom: 10px;
  font-family: "Yeon Sung", cursive;
  font-size: 25px;
}
td {
  margin-left: 20px;
  padding-bottom: 10px;
  font-family: "Yeon Sung", cursive;
  font-size: 20px;
}
.info_content {
  font-family: "Yeon Sung", cursive;
  font-size: 20px;
}
.message {
  width: 100%;
  border: solid 1px black;
  font-family: "Jua", sans-serif;
}
#card_rating {
  display: inline-block;
  text-align: center;
  padding: 1px;
  font-size: 26px;
  border: 1px solid black;
  border-radius: 15%;
  background-color: black;
  color: silver;
  margin: 10px 10px 10px 10px;
  min-width: 40px;
  height: 40px;
}
.review_update {
  display: flex;
  align-items: baseline;
}
.edit_btn {
  width: 5rem;
  height: 2rem;
  letter-spacing: 0.5px;
  font-family: "Yeon Sung", cursive;
  background: rgb(219, 219, 219);
  border-radius: 15%;
}
.edit_btn:hover {
  width: 5rem;
  height: 2rem;
  letter-spacing: 0.5px;
  font-family: "Yeon Sung", cursive;
  background: rgb(173, 173, 173);
  border-radius: 15%;
}
.my_page_head_option {
  display: inline-block;
  width: 40px;
  font-size: 15px;
  transform: translateY(-7.5%);
  margin-left: 10px;
}
#review_form {
  margin-left: 10px;
  margin-right: 10px;
}
</style>