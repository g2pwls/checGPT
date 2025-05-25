<template>
  <section class="thread-detail">
    <div class="main-container" v-if="thread">
      <!-- 책 정보 -->
      <div class="left-box" v-if="thread.book">
        <img :src="thread.book.cover" alt="책 이미지" class="book-image" />
        <div class="book-info">
          <div class="book-title">{{ thread.book.title }}</div>
          <div class="book-subtitle">{{ thread.book.subTitle }}</div>
          <div class="book-pub_date">{{ thread.book.pub_date }}</div>
        </div>
      </div>

      <!-- 스레드 본문 및 조작 -->
      <div class="right-box">
        <h1 class="thread-title">{{ thread.title }}</h1>
        <p class="thread-content">{{ thread.content }}</p>
        <div class="actions">
          <button @click="toggleLike">❤️ {{ thread.likes_count }}</button>
          <button @click="editThread">수정</button>
          <button @click="deleteThread">삭제</button>
        </div>

        <!-- 댓글 -->
        <div class="comments" v-if="thread.comments">
          <h3>댓글 ({{ thread.comments_count }})</h3>
          <input v-model="newComment" placeholder="댓글을 입력하세요..." />
          <div class="actions-comment">
          <button @click="postComment">댓글 작성</button>
          </div>

          <div v-for="comment in thread.comments" :key="comment.id" class="comment">
            <p>{{ comment.content }}</p>
            <small>작성자: {{ comment.author.username }} | {{ comment.created_at }}</small>
          </div>
        </div>
      </div>
    </div>

    <!-- 프로필 정보 -->
    <div class="profile-box" v-if="thread && thread.writer">
      <img 
        :src="thread.writer.profile_image ? `http://127.0.0.1:8000${thread.writer.profile_image}` : '/default-profile.png'" 
        class="avatar" 
        alt="프로필 이미지"
      />
      <span class="username">{{ thread.writer.username }}</span>
      <button @click="followUser">+ 팔로우</button>
      <button @click="goToProfile">프로필가기</button>
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
    };
  },
  async mounted() {
    try {
      const id = this.$route.params.threadId;
      const token = localStorage.getItem('token');

      // Load thread data
      const res = await axios.get(`http://127.0.0.1:8000/api/threads/${id}/`, {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      this.thread = res.data;
    } catch (err) {
      console.error('데이터 로딩 실패:', err);
    }
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
  try {
    const token = localStorage.getItem('token'); // 로그인 시 저장한 토큰 불러오기
    await axios.delete(`http://127.0.0.1:8000/api/threads/${this.thread.id}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    });
    this.$router.push(`/books/${this.thread.book.id}`);
  } catch (error) {
    console.error('삭제 실패:', error);
  }
}
,


    async followUser() {
      await axios.post(`/api/follow/${this.thread.writer.id}/`);
    },
    goToProfile() {
      this.$router.push(`/users/${this.thread.writer.id}/profile`);
    },
    async postComment() {
  try {
    const token = localStorage.getItem('token'); // 로그인된 사용자 토큰
    const res = await axios.post('/api/comments/', {
      thread: this.thread.id,          // 스레드 ID
      content: this.newComment         // 작성한 댓글 내용
    }, {
      headers: {
        Authorization: `Token ${token}`  // 인증 헤더 추가
      }
    });

    // 댓글 목록에 새 댓글 추가
    this.thread.comments.push(res.data);

    // 댓글 수 수동 증가
    this.thread.comments_count += 1;

    // 댓글 입력창 초기화
    this.newComment = '';
  } catch (err) {
    console.error('댓글 작성 실패:', err);
  }
}

  }
}
</script>

<style scoped>
.thread-detail {
  background: #f1f1f1;
  color: black;
  padding-bottom: 40px;
  height: 95vh;
}

/* 가운데 정렬 */
.main-container {
  display: flex;
  padding: 20px;
  gap: 40px;
  max-width: 1000px;
  margin: 0 auto;
}

.left-box {
  background: #222;
  padding: 20px;
  border-radius: 10px;
  width: 260px;
}
.book-image {
  width: 100%;
  border-radius: 6px;
  margin-bottom: 10px;
}
.book-title {
  font-size: 20px;
  font-weight: bold;
  color: #f1f1f1;
}
.book-subtitle {
  font-size: 14px;
  color: #aaa;
}
.book-pub_date {
  font-size: 14px;
  color: #aaa;
}

.right-box {
  flex: 1;
}
.thread-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 10px;
}
.thread-content {
  font-size: 16px;
  margin-bottom: 20px;
}
.actions button {
  margin-right: 10px;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
}
.actions-comment button {
  display: flex;
  margin-right: 10px;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
}
.comments {
  margin-top: 40px;
}
.comments input {
  width: 80%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
  border: none;
  border: 1px solid #cecece;
}
.comment {
  background: #222;
  padding: 10px;
  margin-top: 10px;
  border-radius: 6px;
}

.profile-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px;
  margin: 20px auto;
  background: #1c1c1c;
  border-top: 1px solid #333;
  max-width: 1000px;
}
.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.username {
  font-weight: bold;
}
</style>
