<template>
  <div class="report-view">
    <div class="report-container">
      <h1 class="report-title">Thread</h1>
      
      <!-- 정렬 탭 추가 -->
      <div class="sort-tabs">
        <button 
          @click="sortType = 'latest'" 
          :class="{ active: sortType === 'latest' }"
          class="sort-tab"
        >
          최신순
        </button>
        <button 
          @click="sortType = 'likes'" 
          :class="{ active: sortType === 'likes' }"
          class="sort-tab"
        >
          좋아요순
        </button>
        <button 
          @click="sortType = 'comments'" 
          :class="{ active: sortType === 'comments' }"
          class="sort-tab"
        >
          댓글순
        </button>
      </div>

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
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      threads: [],
      sortType: 'latest', // 기본값은 최신순
    }
  },
  async created() {
    await this.loadThreads();
  },
  watch: {
    sortType() {
      this.loadThreads();
    }
  },
  methods: {
    async loadThreads() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/threads/', {
          headers: {
            Authorization: `Token ${token}`
          },
          params: {
            sort_by: this.sortType
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
      if (!dateString) return '';
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
.report-view {
  background: #fff;
  min-height: 100vh;
  width: 100%;
  padding-top: 1px; /* margin collapse 방지 */
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
}

.report-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #ffffff; /* 흰색 배경 */
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid #ddd;
}

.report-title {
  font-size: 1.8rem; /* 폰트 크기 조정 */
  font-weight: bold;
  margin-bottom: 20px; /* 마진 조정 */
  color: #333;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

/* 정렬 탭 스타일 */
.sort-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.sort-tab {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: #eee; /* 배경색 */
  color: #666; /* 글자색 */
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem; /* 폰트 크기 조정 */
}

.sort-tab:hover {
  background-color: #ddd; /* 호버 시 배경색 */
  color: #333; /* 호버 시 글자색 */
}

.sort-tab.active {
  background-color: #333; /* 활성화 시 배경색 */
  color: white; /* 활성화 시 글자색 */
}

.threads-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); /* 반응형 그리드 */
  gap: 20px;
  margin-top: 20px;
}

.thread-card {
  background-color: #f9f9f9; /* 밝은 배경 */
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  min-height: 250px; /* 최소 높이 유지 */
}

.thread-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.06);
}

.thread-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 15px;
}

.book-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.book-cover {
  width: 40px; /* 책 표지 크기 조정 */
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.book-title {
  font-size: 0.9rem; /* 폰트 크기 조정 */
  color: #555; /* 글자색 조정 */
  flex: 1;
  word-break: break-word;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.thread-meta {
  display: flex;
  justify-content: space-between;
  color: #777; /* 글자색 조정 */
  font-size: 0.8rem;
}

.thread-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
  word-break: break-word;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.thread-content {
  font-size: 0.9rem;
  color: #555; /* 글자색 조정 */
  line-height: 1.4;
  margin-bottom: 12px;
  flex-grow: 1;
  word-break: break-word;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.thread-footer {
  margin-top: auto;
  border-top: 1px solid #eee;
  padding-top: 10px;
}

.interactions {
  display: flex;
  gap: 15px;
  color: #777; /* 글자색 조정 */
  font-size: 0.9rem;
}

.author {
  font-weight: bold;
  color: #333;
}

.date {
  color: #999;
}

@media (max-width: 768px) {
  .report-container {
    padding: 20px 10px;
  }

  .report-title {
    font-size: 1.5rem;
  }

  .sort-tabs {
    flex-wrap: wrap;
    justify-content: center;
  }

  .threads-container {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }

  .thread-card {
    min-height: 200px; /* 모바일 최소 높이 */
  }

  .book-cover {
    width: 30px;
    height: 45px;
  }

  .book-title {
    font-size: 0.8rem;
  }

  .thread-meta {
    font-size: 0.7rem;
  }

  .thread-title {
    font-size: 1rem;
  }

  .thread-content {
    font-size: 0.85rem;
  }

  .interactions {
    font-size: 0.8rem;
  }
}
</style> 