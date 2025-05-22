<template>
    <div class="book-detail-wrapper">
      <!-- 제목과 쓰레드 작성 버튼 -->
      <header class="header">
        <h1 class="book-title">{{ book.title }}</h1>
        <button class="thread-btn" @click="goToThreadWrite">+</button>
      </header>
      
      <div class="backback">
      <!-- 책 정보 섹션 -->
      <section class="book-info-section">
        <img :src="book.cover" alt="book cover" class="book-cover" />
        <div class="book-details">
          <p class="subtitle">{{ book.subTitle }}</p>
          <p class="description">{{ book.description }}</p>
          <p><strong>출판사:</strong> {{ book.publisher }}</p>
          <p><strong>출간일:</strong> {{ book.pub_date }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn }}</p>
          <p><strong>고객 리뷰 평점:</strong> {{ book.customer_review_rank }}</p>
        </div>
      </section>
  
      <!-- 작가 정보 섹션 -->
      <section class="author-info-section">
        <h2>작가 정보</h2>
        <div class="author-profile">
          <img v-if="book.author_photo" :src="book.author_photo" alt="author" class="author-photo" />
          <div>
            <p class="author-name"><strong>{{ book.author }}</strong></p>
            <p class="author-desc">{{ book.author_info }}</p>
          </div>
        </div>
      </section>
      </div>
    </div>
  </template>
  
  <script>
    import axios from 'axios'

    export default {
    name: 'BookDetail',
    data() {
        return {
        book: null,
        }
    },
    async created() {
        const bookId = Number(this.$route.params.bookId)
        try {
        const response = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/`)
        this.book = response.data
        } catch (error) {
        console.error('책 정보를 불러오는 데 실패했습니다:', error)
        }
    },
    methods: {
        goToThreadWrite() {
        this.$router.push(`/threads/${this.book.id}/write`)
        }
    }
    }
</script>

  
  <style scoped>
  .backback {
    padding: 30px;
    background-color:rgb(241, 241, 241);
  }
  
  .book-detail-wrapper {
    max-width: 900px;
    margin: 40px auto;
    font-family: "Noto Sans KR", sans-serif;
    color: #111;

  }
  
  /* 제목과 버튼 영역 */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    height: 50px;
  }
  
  .book-title {
    font-size: 2rem;
    font-weight: bold;
  }
  
  .thread-btn {
    background-color: #f44;
    border: none;
    color: white;
    font-size: 1.8rem;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    line-height: 1;
    transition: background-color 0.3s ease;
  }
  
  .thread-btn:hover {
    background-color: #d33;
  }
  
  /* 책 정보 섹션 */
  .book-info-section {
    display: flex;
    gap: 20px;
    margin-bottom: 40px;
  }
  
  .book-cover {
    width: 160px;
    height: 240px;
    object-fit: cover;
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
  }
  
  .book-details {
    flex: 1;
  }
  
  .subtitle {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 12px;
  }
  
  .description {
    margin-bottom: 15px;
    white-space: pre-wrap;
    line-height: 1.5;
  }
  
  /* 작가 정보 섹션 */
  .author-info-section {
    border-top: 1px solid #ddd;
    padding-top: 30px;
  }
  
  .author-info-section h2 {
    margin-bottom: 20px;
    font-weight: 700;
    font-size: 1.4rem;
  }
  
  .author-profile {
    display: flex;
    gap: 20px;
    align-items: flex-start;
  }
  
  .author-photo {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 0 5px rgba(0,0,0,0.1);
  }
  
  .author-name {
    font-size: 1.2rem;
    margin-bottom: 10px;
  }
  
  .author-desc {
    font-size: 0.9rem;
    line-height: 1.4;
    white-space: pre-wrap;
  }
  </style>
  