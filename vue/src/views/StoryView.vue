<template>
  <div class="story-view">
    <div class="story-header">
      <h2 class="page-title">📚 이야기마당</h2>
      <p class="description">독자들과 함께 나누는 책 이야기 공간입니다.</p>
    </div>

    <!-- 최근 오픈된 이야기마당 공지 섹션 -->
    <div class="notice-section">
      <h3>🎉 새로 열린 이야기마당</h3>
      <div class="notice-items">
        <div v-for="book in recentStoryBooks" :key="'story-'+book.id" 
             class="notice-item" @click="goToCommunity(book.id)">
          <div class="notice-book-info">
            <img :src="book.cover" :alt="book.title" class="notice-book-cover">
            <div class="notice-text">
              <span class="book-title">{{ book.title }}</span>
              <span class="open-label">이야기마당이 열렸습니다!</span>
            </div>
          </div>
          <span class="notice-date">{{ formatDate(book.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- 전체 이야기마당 목록 -->
    <div class="books-section">
      <h3>📖 전체 이야기마당</h3>
      <div class="books-grid">
        <div v-for="book in booksWithStory" :key="book.id" 
             class="book-card" @click="goToCommunity(book.id)">
          <img :src="book.cover" :alt="book.title" class="book-cover">
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
            <div class="story-stats">
              <span class="stat-item">
                <i class="fas fa-comments"></i> {{ book.comment_count || 0 }}
              </span>
              <span class="stat-item">
                <i class="fas fa-heart"></i> {{ book.like_count || 0 }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StoryView',
  data() {
    return {
      booksWithStory: [],
      recentStoryBooks: []
    }
  },
  async created() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/books/');
      // 커뮤니티(이야기마당)가 있는 책들만 필터링
      const booksWithCommunity = response.data.filter(book => 
        book.has_community || book.community_posts?.length > 0
      );
      
      // 전체 이야기마당 목록
      this.booksWithStory = booksWithCommunity;
      
      // 최근 오픈된 3개의 이야기마당
      this.recentStoryBooks = [...booksWithCommunity]
        .sort((a, b) => {
          const dateA = a.community_created_at ? new Date(a.community_created_at) : new Date(0);
          const dateB = b.community_created_at ? new Date(b.community_created_at) : new Date(0);
          return dateB - dateA;
        })
        .slice(0, 3);

      console.log('이야기마당이 있는 책들:', this.booksWithStory);
      console.log('최근 오픈된 이야기마당:', this.recentStoryBooks);
    } catch (error) {
      console.error('책 정보 로딩 실패:', error);
      if (error.response) {
        console.error('에러 응답:', error.response.data);
      }
    }
  },
  methods: {
    goToCommunity(bookId) {
      this.$router.push({ 
        name: 'community',
        params: { bookId: bookId }
      });
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    }
  }
}
</script>

<style scoped>
.story-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.story-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2em;
}

.description {
  color: #666;
}

/* 공지 섹션 스타일 */
.notice-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.notice-section h3 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.notice-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.notice-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notice-item:hover {
  background-color: #e3f2fd;
  transform: translateY(-2px);
}

.notice-book-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.notice-book-cover {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.notice-text {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.notice-text .book-title {
  font-weight: 600;
  color: #1976d2;
}

.open-label {
  font-size: 0.9em;
  color: #4caf50;
}

.notice-date {
  color: #666;
  font-size: 0.9em;
}

/* 책 목록 섹션 스타일 */
.books-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.books-section h3 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.book-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.book-cover {
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.book-info {
  padding: 15px;
}

.book-title {
  margin: 0;
  font-size: 1.1em;
  color: #2c3e50;
  margin-bottom: 5px;
}

.book-author {
  margin: 0;
  color: #666;
  font-size: 0.9em;
  margin-bottom: 10px;
}

.story-stats {
  display: flex;
  gap: 15px;
}

.stat-item {
  color: #666;
  font-size: 0.9em;
}

.stat-item i {
  margin-right: 5px;
}

@media (max-width: 768px) {
  .story-view {
    padding: 15px;
  }

  .notice-section, .books-section {
    padding: 15px;
  }

  .notice-book-cover {
    width: 50px;
    height: 70px;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }

  .book-cover {
    height: 200px;
  }

  .book-info {
    padding: 10px;
  }
}
</style> 