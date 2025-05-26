<template>
  <div class="main-view">
    <div class="main-container">
      <!-- 베스트셀러 섹션 -->
      <section class="bestseller-section">
        <h2 class="section-title">지금 인기있어요!</h2>
        <div class="book-slider">
          <div v-for="book in bestSellers" :key="book.isbn" class="book-card" @click="goToBookDetail(book)">
            <img :src="book.cover" alt="book cover" class="book-cover" />
            <div class="book-info">
              <h3 class="book-title">{{ book.title }}</h3>
              <p class="book-author">{{ book.author }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 카테고리 섹션 -->
      <section class="category-section">
        <h2 class="section-title">갈래별 보기</h2>
        <div class="category-grid">
          <div 
            v-for="category in categories" 
            :key="category.id" 
            class="category-card"
            @click="goToCategory(category.id)"
          >
            <h3>{{ category.name }}</h3>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      bestSellers: [],
      categories: [],
      dbBooks: [], // 데이터베이스의 책 정보 저장
    }
  },
  async created() {
    await this.loadDbBooks(); // 데이터베이스 책 정보 먼저 로드
    await this.loadBestSellers();
    await this.loadCategories();
  },
  methods: {
    async loadDbBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/books/');
        this.dbBooks = response.data;
      } catch (error) {
        console.error('데이터베이스 책 로딩 실패:', error);
      }
    },
    async loadBestSellers() {
      try {
        const ttbKey = 'ttbyhjyhw10041939002';
        const script = document.createElement('script');
        const callbackName = 'aladin' + Date.now();
        
        window[callbackName] = (data) => {
          if (data && data.item) {
            this.bestSellers = data.item.map(book => {
              // 데이터베이스에서 매칭되는 책 찾기
              const matchedBook = this.dbBooks.find(dbBook => 
                dbBook.title.replace(/\s+/g, '') === book.title.replace(/\s+/g, '') ||
                dbBook.isbn === book.isbn13 ||
                dbBook.isbn === book.isbn
              );

              return {
                isbn: book.isbn13 || book.isbn,
                title: book.title,
                author: book.author,
                cover: book.cover,
                dbId: matchedBook ? matchedBook.id : null // 매칭된 책의 ID 저장
              };
            });
          }
          delete window[callbackName];
          document.body.removeChild(script);
        };

        const url = `http://www.aladin.co.kr/ttb/api/ItemList.aspx?TTBKey=${ttbKey}&QueryType=Bestseller&MaxResults=10&start=1&SearchTarget=Book&output=js&Version=20131101&callback=${callbackName}`;
        
        script.src = url;
        document.body.appendChild(script);
      } catch (error) {
        console.error('베스트셀러 로딩 실패:', error);
      }
    },
    async loadCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('카테고리 로딩 실패:', error);
      }
    },
    formatPrice(price) {
      return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    goToBookDetail(book) {
      if (book.dbId) {
        this.$router.push(`/books/${book.dbId}`);
      } else {
        alert('죄송합니다. 현재 이 책의 상세 정보는 제공되지 않습니다.');
      }
    },
    goToCategory(categoryId) {
      this.$router.push({
        path: '/booklist',
        query: { category: categoryId }
      });
    }
  }
}
</script>

<style scoped>
.main-view {
  background-color: #f9f6f2;
  min-height: 100vh;
  width: 100%;
  padding-top: 1px; /* margin collapse 방지 */
}

.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 30px;
  color: #2c3e50;
}

/* 베스트셀러 섹션 */
.bestseller-section {
  margin-bottom: 60px;
}

.book-slider {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  margin-bottom: 40px;
}

.book-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 200px;
  margin: 0 auto;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.12);
}

.book-cover {
  width: 100%;
  height: 200px;
  object-fit: contain;
  background: #ffffff;
  padding: 10px;
  border-bottom: 1px solid #f0e9e3;
}

.book-info {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.book-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 6px;
  color: #2c3e50;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 2.4em;
}

.book-author {
  font-size: 0.8rem;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-price {
  font-size: 1.1rem;
  color: #e74c3c;
  font-weight: bold;
  margin-top: auto;
}

/* 카테고리 섹션 */
.category-section {
  margin-bottom: 60px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.category-card {
  background: white;
  color: #2c3e50;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 15px rgba(0,0,0,0.08);
  border: 1px solid #f0e9e3;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.12);
  background: #fff;
}

.category-card h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0;
  color: #2c3e50;
}
</style> 