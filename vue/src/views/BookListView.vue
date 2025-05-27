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
            :class="{ active: selectedCategory === null }"
            @click="selectedCategory = null"
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
            :key="book.id"
            class="book-card"
            @click="goToDetail(book.id)"
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
  import { useRouter, useRoute } from "vue-router";
  
  const books = ref([]);
  const categories = ref([]);
  const searchQuery = ref("");
  const selectedCategory = ref(null);  // null로 초기화
  const router = useRouter();
  const route = useRoute();
  
  // URL에서 카테고리 파라미터 가져오기
  const categoryParam = route.query.category;
  if (categoryParam) {
    selectedCategory.value = Number(categoryParam);
  }

  const fetchBooks = async () => {
    const params = {};
    if (selectedCategory.value !== null) {  // null이 아닐 때만 category 파라미터 추가
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
  
  // 카테고리 변경 감시
  watch(selectedCategory, (newCategory) => {
    fetchBooks();
    // URL 쿼리 파라미터 업데이트
    router.push({
      query: { 
        ...route.query,
        category: newCategory || undefined
      }
    });
  });
  
  // 검색어 변경 감시
  watch(searchQuery, fetchBooks);
  
  // URL 쿼리 파라미터 변경 감시
  watch(() => route.query.category, (newCategory) => {
    if (newCategory !== selectedCategory.value?.toString()) {
      selectedCategory.value = newCategory ? Number(newCategory) : null;
    }
  });
  
  onMounted(async () => {
    await Promise.all([fetchCategories(), fetchBooks()]);
  });
  
  const goToDetail = (bookId) => {
    router.push(`/books/${bookId}`);
  };
</script>
  
<style scoped>
    /* 전체 컨테이너 */
    .container {
        display: flex;
        height: 93.5vh;
        background-color: #ffffff; /* 흰색 배경 */
        color: #333; /* 어두운 글자색 */
        font-family: 'Noto Sans KR', sans-serif;
        gap: 0;
    }
    
    /* 사이드바 */
    .sidebar {
        width: 200px; /* 너비 조정 */
        padding: 20px; /* 패딩 조정 */
        background-color: #ffffff; /* 흰색 배경 */

        display: flex;            /* flex 컨테이너 */
        flex-direction: column;   /* 세로 정렬 */
        align-items: flex-start;      /* 왼쪽 정렬 */
        border-right: 1px solid #ddd; /* 구분선 */
        box-sizing: border-box;
        overflow-y: auto; /* 스크롤 가능 */
    }
    
    .sidebar h2 {
        color: #555; /* 무채색 계열 색상 */
        font-size: 1.2rem;
        margin-bottom: 20px; /* 마진 조정 */
        align-self: center; /* 제목 중앙 정렬 */
    }
    
    .sidebar ul {
        list-style: none;
        padding: 0;
        margin-top: 0; /* 마진 제거 */
        width: 100%; /* 전체 너비 사용 */
        text-align: left; /* 텍스트 왼쪽 정렬 */
    }
    
    .sidebar li {
        font-size: 1rem; /* 폰트 크기 조정 */
        margin-bottom: 12px; /* 마진 조정 */
        cursor: pointer;
        color: #555; /* 무채색 계열 색상 */
        font-weight: normal; /* 기본 폰트 굵기 */
        padding: 8px 10px; /* 패딩 추가 */
        border-radius: 4px; /* 둥근 모서리 */
        transition: all 0.2s ease;
    }
    
    .sidebar li:hover {
        color: #333; /* 호버 시 글자색 진하게 */
        background-color: #f8f8f8; /* 호버 시 배경색 살짝 추가 */
    }
    
    .sidebar li.active {
        color: #333; /* 활성화된 항목 글자색 진하게 */
        font-weight: bold; /* 활성화된 항목 폰트 굵기 */
        background-color: #eee; /* 활성화된 항목 배경색 */
    }
    
    /* 본문 */
    .main-content {
        flex: 1;
        padding: 40px 24px; /* 패딩 조정 */
        overflow-y: auto;
        background-color: #ffffff; /* 흰색 배경 */
        display: flex;
        justify-content: center;
    }
    
    /* 검색창 */
    .search-input {
        padding: 10px;
        width: 158px; /* 패딩 고려한 너비 */
        margin-bottom: 24px;
        border: 1px solid #ccc;
        background-color: #fff;
        color: #333;
        height: 40px;
        border-radius: 4px;
        font-size: 16px;
        box-sizing: border-box;
    }
    .search-input::placeholder {
      color: #999;
    }

    
    /* 책 카드 그리드 */
    .book-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 24px;
        max-width: 1200px;
        width: 100%;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* 개별 책 카드 */
    .book-card {
    display: flex;
    background-color: #ffffff;
    padding: 16px;
    border-radius: 8px;
    gap: 16px;
    align-items: flex-start;
    min-height: 200px;
    overflow: hidden;
    color: #333;
    border: 1px solid #ddd;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
    }

    .book-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    .book-cover {
    width: 120px;
    height: 180px;
    object-fit: cover;
    flex-shrink: 0;
    border-radius: 4px;
    border: 1px solid #ddd;
    }

    .book-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    overflow: hidden;
    }

    .book-title {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 8px;
    color: #333;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    word-break: break-word;
    }

    .book-meta {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 8px;
    }

    .book-subtitle {
    font-size: 0.85rem;
    color: #555;
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    word-break: break-word;
    }

/* 반응형 디자인 */
@media (max-width: 768px) {
  .container {
    flex-direction: column; /* 세로 정렬 */
    height: auto; /* 높이 자동 */
  }

  .sidebar {
    width: 100%; /* 전체 너비 */
    padding: 10px;
    border-right: none;
    border-bottom: 1px solid #ddd; /* 하단 구분선 */
    align-items: center; /* 중앙 정렬 */
  }

  .sidebar ul {
    margin-top: 0; /* 상단 마진 제거 */
    display: flex; /* 가로 정렬 */
    flex-wrap: wrap; /* 넘칠 경우 줄 바꿈 */
    justify-content: center; /* 중앙 정렬 */
    gap: 10px; /* 간격 */
  }

  .sidebar li {
    margin-bottom: 0; /* 하단 마진 제거 */
    padding: 5px 10px; /* 패딩 조정 */
  }

  .main-content {
    padding: 20px 10px; /* 패딩 조정 */
  }

  .book-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
    padding: 0;
  }

  .book-card {
    flex-direction: column; /* 세로 카드 */
    align-items: center; /* 중앙 정렬 */
    gap: 10px;
    min-height: auto; /* 최소 높이 자동 */
    padding: 10px;
  }

  .book-cover {
    width: 100px;
    height: 150px;
  }

  .book-info {
    text-align: center; /* 텍스트 중앙 정렬 */
  }

  .book-title, .book-meta, .book-subtitle {
    text-align: center; /* 텍스트 중앙 정렬 */
  }
}

</style>