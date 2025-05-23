<template>
  <section class="thread-detail">
    <div class="cover-img"></div>

    <div class="content">
      <div class="book-box">
        <img :src="thread.book.cover_image" />
        <div>
          <p class="book-title">{{ thread.book.title }}</p>
          <p>{{ thread.book.published_date }}</p>
        </div>
      </div>

      <div class="thread-content">
        <p class="thread-title">{{ thread.title }}</p>
        <p class="thread-body">{{ thread.content }}</p>
        <div class="actions">
          <button @click="toggleLike">❤️ {{ thread.likes_count }}</button>
          <button @click="editThread">수정</button>
          <button @click="deleteThread">삭제</button>
        </div>
      </div>

      <div class="author-box">
        <img :src="authorProfile.image" class="avatar" />
        <span>{{ thread.author.username }}</span>
        <button @click="followUser">+ 팔로우</button>
        <button @click="goToProfile">프로필가기</button>
      </div>

      <div class="comments">
        <h3>댓글 ({{ thread.comments.length }})</h3>
        <input v-model="newComment" placeholder="댓글을 입력하세요..." />
        <button @click="postComment">댓글 작성</button>

        <div v-for="comment in thread.comments" :key="comment.id" class="comment">
          <p>{{ comment.content }}</p>
          <small>작성자: {{ comment.author.username }} | {{ comment.created_at }}</small>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      thread: null,
      newComment: '',
      authorProfile: {},
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    const res = await axios.get(`/api/threads/${id}/`);
    this.thread = res.data;

    const profileRes = await axios.get(`/api/users/${this.thread.author.id}/profile/`);
    this.authorProfile = profileRes.data;
  },
  methods: {
    async toggleLike() {
      await axios.post(`/api/threads/${this.thread.id}/like/`);
      this.thread.likes_count += 1;
    },
    async postComment() {
      const res = await axios.post(`/api/comments/`, {
        thread: this.thread.id,
        content: this.newComment,
      });
      this.thread.comments.push(res.data);
      this.newComment = '';
    },
    async editThread() {
      this.$router.push(`/threads/${this.thread.id}/edit`);
    },
    async deleteThread() {
      await axios.delete(`/api/threads/${this.thread.id}/`);
      this.$router.push('/');
    },
    followUser() {
      axios.post(`/api/follow/${this.thread.author.id}/`);
    },
    goToProfile() {
      this.$router.push(`/users/${this.thread.author.id}/profile`);
    }
  }
}
</script>

<style scoped>
.thread-detail {
  background: #111;
  color: white;
  padding: 20px;
}
.cover-img {
  height: 250px;
  background-image: url('/cover.jpg');
  background-size: cover;
  background-position: center;
  margin-bottom: 20px;
}
.book-box {
  display: flex;
  align-items: center;
  background: #222;
  padding: 10px;
  border-radius: 8px;
}
.book-title {
  font-weight: bold;
  font-size: 18px;
}
.thread-content, .author-box, .comments {
  margin-top: 20px;
}
.comment {
  background: #222;
  padding: 10px;
  margin-top: 10px;
  border-radius: 6px;
}
.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.actions button {
  margin-right: 10px;
}
</style>
