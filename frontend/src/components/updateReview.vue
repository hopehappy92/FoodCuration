<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on }">
        <i class="fas fa-edit" v-on="on" />
      </template>

      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>리뷰 수정</v-card-title>
        <textarea v-model="eContent" type="text" value="hhh">content</textarea>
        <v-divider />
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" text @click="editDone">수정</v-btn>
          <v-btn color="red" text @click="dialog = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  props: {
    reviewId: Number,
    content: String
  },
  data() {
    return {
      dialog: false,
      eContent: this.content,
      score: 3
    };
  },
  methods: {
    ...mapActions("data", ["editReview"]),
    editDone: async function() {
      const params = {
        id: this.reviewId,
        score: this.score,
        content: this.eContent
      };
      await this.editReview(params)
        .then(this.$emit("editReview"))
        .then((this.dialog = false));
    }
  }
};
</script>

<style scoped>
i {
  font-size: 20px;
}
i:hover {
  font-size: 25px;
  cursor: pointer;
}
textarea {
  width: 100%;
  height: 200px;
  padding-left: 20px;
  padding-right: 20px;
}
</style>