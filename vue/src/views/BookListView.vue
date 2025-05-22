<template>
    <div class="container">
      <!-- 사이드바 -->
      <main class="sidebar">
        <ul>
          <input
            v-model="searchQuery"
            placeholder="검색어를 입력하세요..."
            class="search-input"
          />
          <li
          :class="{ active: selectedCategory === 0 }"
          @click="selectedCategory = 0"
            >
            전체
            </li>
          <li
            v-for="category in categories"
            :key="category.id"
            :class="{ active: selectedCategory === category.id }"
            @click="selectedCategory = category.id"
          >
            {{ category.name }}
          </li>
        </ul>
      </main>
  
      <!-- 본문 -->
      <main class="main-content">
        <div class="book-grid">
          <div
            v-for="book in books"
            :key="book.pk"
            class="book-card"
            @click="goToDetail(book.pk)"
            style="cursor: pointer;"
          >
            <img :src="book.cover" alt="book cover" class="book-cover" />
            <div class="book-info">
              <h3 class="book-title">{{ book.title }}</h3>
              <p class="book-meta">
                {{ book.author }} | {{ book.publisher }} | {{ book.pub_date }}
              </p>
              <p class="book-subtitle">{{ book.subTitle }}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
</template>
  
<script setup>
  import { ref, watch, onMounted } from "vue";
  import axios from "axios";
  import { useRouter } from "vue-router";
  
  const books = ref([]);
  const categories = ref([]);
  const searchQuery = ref("");
  const selectedCategory = ref(0);
  const router = useRouter();
  
  const fetchBooks = async () => {
    const params = {};
    if (selectedCategory.value) {
      params.category = selectedCategory.value;
    }
    if (searchQuery.value) {
      params.search = searchQuery.value;
    }
    const response = await axios.get("http://127.0.0.1:8000/api/books/", { params });
    books.value = response.data;
  };
  
  const fetchCategories = async () => {
    const response = await axios.get("http://127.0.0.1:8000/api/categories/");
    categories.value = response.data;
  };
  
  onMounted(async () => {
    await fetchCategories();
    await fetchBooks();
  });
  
  watch([selectedCategory, searchQuery], fetchBooks);
  
  const goToDetail = (bookId) => {
    router.push(`/books/${bookId}`);
  };
</script>
  
<style scoped>
    /* 전체 컨테이너 */
    .container {
        display: flex;
        height: 100vh;
        background-color: #111;
        color: white;
        font-family: sans-serif;
        gap: 0;
    }
    
    /* 사이드바 */
    .sidebar {
        width: 20%;
        padding: 20px 10px 20px 20px;
        background-color: #000;

        display: flex;            /* flex 컨테이너 */
        flex-direction: column;   /* 세로 정렬 */
        align-items: center;      /* 가로 중앙 정렬 */
    
    }
    
    .sidebar h2 {
        color: #f44;
        font-size: 1.2rem;
        margin-bottom: 16px;
        margin-left: 16px;
        
    }
    
    .sidebar ul {
        list-style: none;
        padding: 0;
        margin-top: 100px;
    }
    
    .sidebar li {
        font-size: 15px;
        margin-bottom: 15px;
        cursor: pointer;
        color: #ccc;
    }
    
    .sidebar li:hover {
        color: #f88;
    }
    
    .sidebar li.active {
        color: #f44;
        font-weight: bold;
    }
    
    /* 본문 */
    .main-content {
        flex: 1;
        padding: 24px 24px 24px 10px;
        overflow-y: auto;
        background-color: #000;
        margin-top: 100px;
        display: flex;
        /* justify-content: center */
        /* overflow: hidden; */

    }
    
    /* 검색창 */
    .search-input {
        padding: 10px;
        /* width: 100%; */
        margin-bottom: 24px;
        border: 1px solid #666;
        background-color: #222;
        color: white;
        height: 20px;
        width: 200px;
        border-radius: 3px;
        font-size: 16px;
    }
    
    /* 책 카드 그리드 */
    .book-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* 두 개씩 고정 */
        gap: 24px;
        max-width: 1200px; /* 전체 그리드 너비 제한 */
        width: 100%;
        height: 200px;

    }
    
    /* 개별 책 카드 */
    .book-card {
    display: flex;
    background-color: #222;
    padding: 16px;
    border-radius: 8px;
    gap: 16px; /* 이미지와 텍스트 사이 간격 */
    align-items: flex-start; /* 이미지와 텍스트 상단 정렬 */
    height: 200px;
    overflow: hidden;
    }

    .book-cover {
    width: 120px; /* 이미지 너비 */
    height: 180px; /* 이미지 높이 */
    object-fit: cover;
    flex-shrink: 0; /* 이미지 크기 고정 */
    }

    .book-info {
    flex: 1; /* 텍스트 영역이 남는 공간 차지 */
    display: flex;
    flex-direction: column;
    justify-content: center; /* 필요 시 세로 중앙 정렬 */
    overflow: hidden;
    }

    .book-title {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 4px;
    }

    .book-meta {
    font-size: 0.85rem;
    color: #aaa;
    margin-bottom: 4px;
    }

    .book-subtitle {
    font-size: 0.75rem;
    color: #666;
    }

</style>
  