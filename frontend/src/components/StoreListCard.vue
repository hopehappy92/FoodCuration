<template>
  <div class="search_card">
    <div class="search_card_main">
      <div class="search_card_tags">
        {{ tags }}
      </div>
      <div class="search_card_name">
        {{ name }}
      </div>
      <div class="search_card_etc">
        {{ address }} / 📞 {{ tel }}
      </div>
    </div>
    <img v-if="`${url}`" :src="`${url}`" alt="images" class="search_card_img">
    <img v-else src="../../public/images/noImage1.jpg" alt="no_images" class="search_card_img">
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      default: 0,
    },
    name: {
      type: String,
      default: ""
    },
    categories: {
      type: Array,
      default: () => new Array()
    },
    address: {
      type: String,
      default: ""
    },
    tel: {
      type: String,
      default: ""
    },
    url: {
      type: String,
      default: ""
    }
  },
  computed: {
    tags: function() {
      return this.categories.reduce((acc, v) => {
        return `${acc} #${v}`;
      }, "");
    }
  }
};
</script>

<style scoped>
.search_card {
  display: flex;
}
.search_card_main {
  flex: 1;
}
.search_card_img {
  width: 20vw;
}
.search_card {
  border: 1px solid white;
  background-color: white;
  text-align: center;
  padding: 10px;
  border-radius: 5px;
  width: 100%;
}
.search_card_tags {
  color: gray;
  text-align: start;
  height: 20px;
}
.search_card_name {
  font-size: 4vw;
  margin: 20px;
  font-weight: 500;
  /* line-height: 4.6vw; */
  /* margin-bottom: px; */
}
.search_card_etc {
  color: gray
}
@media screen and (max-width: 600px) {
  .search_card_img {
    /* width: 20vw; */
    display: none;
  }
  .search_card_name {
    font-size: 10vw;
    margin: 0px;
    font-weight: 400;
  }
}
</style>
