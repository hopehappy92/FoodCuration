<template>
  <div id="WC" style="width:100%;">
    <h1>"{{ storeName }} 관련 태그"</h1>
    <!-- <hr class="line" />   -->
  </div>
</template>

<script>
export default {
  props: {
    tags: String,
    storeName: String
  },
  mounted() {
    setTimeout(() => {
      // console.log("워드클라우드");
      var tags = this.tags.split("|");
      // console.log(tags);
      var word_array = [];
      for (var i = 0; i < tags.length; i++) {
        let tmp = { text: tags[i], weight: 15 - i * 1.5 };
        word_array.push(tmp);
      }
      // console.log(word_array);
      $(function() {
        $("#WC").jQCloud(word_array);
      });
    }, 1000);
  }
};
</script>

<style scoped>
#WC {
  width: 100%;
  height: 350px;
  border-radius: 5%;
  background: whitesmoke;
  justify-content: center;
}
h1 {
  color: black;
  font-size: 30px;
  text-align: center;
  font-family: "Do Hyeon", sans-serif;
  font-style: italic;
  font-weight: 1;
}
.line {
  color: silver;
  margin-top: 10px;
}
@media screen and (max-width: 600px) {
  h1 {
    font-size: 10vw;
  }
}
</style>