<template>
  <div id="WC" style="width:100%;">
    <h1>"{{storeName}} 관련 태그"</h1>
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
      console.log("워드클라우드");
      var tags = this.tags.split("|");
      console.log(tags);
      var word_array = [];
      for (var i = 0; i < tags.length; i++) {
        let tmp = { text: tags[i], weight: 15 - i * 1.5 };
        word_array.push(tmp);
      }
      console.log(word_array);

      // var word_array = [
      //   { text: "Lorem", weight: 15 },
      //   { text: "Ipsum", weight: 9, link: "http://jquery.com/" },
      //   {
      //     text: "Dolor",
      //     weight: 6,
      //     html: { title: "I can haz any html attribute" }
      //   },
      //   { text: "Sit", weight: 7 },
      //   { text: "Amet", weight: 5 }
      //   // ...as many words as you want
      // ];
      $(function() {
        // When DOM is ready, select the container element and call the jQCloud method, passing the array of words as the first argument.
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