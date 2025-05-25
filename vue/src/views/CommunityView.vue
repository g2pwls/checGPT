<template>
  <div class="community-container">
    <h1 class="community-title">커뮤니티</h1>
    <div class="threads-container">
      <div v-for="thread in threads" :key="thread.id" class="thread-card" @click="goToThread(thread.id)">
        <div class="thread-header">
          <div class="book-info">
            <img :src="thread.book.cover" alt="책 표지" class="book-cover">
            <span class="book-title">{{ thread.book.title }}</span>
          </div>
          <div class="thread-meta">
            <span class="author">by {{ thread.writer.username }}</span>
            <span class="date">{{ formatDate(thread.read_date) }}</span>
          </div>
        </div>
        <h2 class="thread-title">{{ thread.title }}</h2>
        <p class="thread-content">{{ truncateContent(thread.content) }}</p>
        <div class="thread-footer">
          <div class="interactions">
            <span>❤️ {{ thread.likes_count }}</span>
            <span>💬 {{ thread.comments_count }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      threads: [],
    }
  },
  async created() {
    await this.loadThreads();
  },
  methods: {
    async loadThreads() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/threads/', {
          headers: {
            Authorization: `Token ${token}`
          }
        });
        this.threads = response.data;
      } catch (error) {
        console.error('스레드 목록 로딩 실패:', error);
      }
    },
    goToThread(threadId) {
      this.$router.push(`/threads/${threadId}`);
    },
    truncateContent(content) {
      return content.length > 100 ? content.slice(0, 100) + '...' : content;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}/${month}/${day}`;
    }
  }
}
</script>

<style scoped>
.community-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 0 20px;
}

.community-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 30px;
  color: #333;
}

.threads-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.thread-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.thread-card:hover {
  transform: translateY(-2px);
}

.thread-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.book-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.book-cover {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.book-title {
  font-size: 0.9rem;
  color: #666;
}

.thread-meta {
  display: flex;
  gap: 15px;
  color: #888;
  font-size: 0.9rem;
}

.thread-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #333;
}

.thread-content {
  color: #666;
  line-height: 1.5;
  margin-bottom: 15px;
}

.thread-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.interactions {
  display: flex;
  gap: 15px;
  color: #888;
}
</style> 