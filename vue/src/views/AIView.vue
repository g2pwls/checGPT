<template>
  <div class="ai-container">
    <h1 class="title">AI 도서 분석</h1>
    
    <!-- AI 기반 책 추천 섹션 -->
    <section class="ai-section">
      <h2>AI 기반 책 추천</h2>
      <div class="recommendations" v-if="recommendedBooks.length > 0">
        <div class="book-card" v-for="book in recommendedBooks" :key="book.id" @click="goToBookDetail(book.id)">
          <img :src="book.cover" :alt="book.title" class="book-cover">
          <div class="book-info">
            <h3>{{ book.title }}</h3>
            <p>{{ book.author }}</p>
            <div class="match-score">
              일치도: {{ book.matchPercent }}%
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 추천 장소 섹션 -->
    <section class="ai-section">
      <h2>이 책을 읽기 좋은 장소</h2>
      <div class="places" v-if="recommendedPlaces.length > 0">
        <div class="place-card" v-for="(place, index) in recommendedPlaces" :key="index">
          <div class="place-icon">
            <i :class="place.icon"></i>
          </div>
          <div class="place-info">
            <h3>{{ place.name }}</h3>
            <p>{{ place.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'AIView',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const recommendedBooks = ref([]);
    const recommendedPlaces = ref([]);
    const bookId = ref(null);

    const goToBookDetail = (id) => {
      router.push({ name: 'book-detail', params: { id } });
    };

    const fetchRecommendedBooks = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/books/${bookId.value}/recommendations/`);
        recommendedBooks.value = response.data;
      } catch (error) {
        console.error('추천 도서를 불러오는데 실패했습니다:', error);
      }
    };

    const analyzeReadingPlaces = async () => {
      try {
        // 여기에서 책의 장르, 분위기 등을 기반으로 장소를 추천
        recommendedPlaces.value = [
          {
            name: '조용한 카페',
            description: '차분한 분위기에서 집중해서 읽기 좋은 장소입니다.',
            icon: 'fas fa-coffee'
          },
          {
            name: '공원 벤치',
            description: '자연 속에서 여유롭게 읽기 좋은 장소입니다.',
            icon: 'fas fa-tree'
          },
          {
            name: '도서관',
            description: '깊이 있는 독서를 위한 최적의 장소입니다.',
            icon: 'fas fa-book-reader'
          }
        ];
      } catch (error) {
        console.error('장소 분석에 실패했습니다:', error);
      }
    };

    onMounted(() => {
      bookId.value = route.params.id;
      if (bookId.value) {
        fetchRecommendedBooks();
        analyzeReadingPlaces();
      }
    });

    return {
      recommendedBooks,
      recommendedPlaces,
      goToBookDetail
    };
  }
};
</script>

<style scoped>
.ai-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.ai-section {
  margin-bottom: 3rem;
  background: white;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ai-section h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.recommendations {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.book-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-5px);
}

.book-cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.book-info {
  padding: 1rem;
}

.book-info h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.match-score {
  margin-top: 0.5rem;
  color: #4CAF50;
  font-weight: bold;
}

.places {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.place-card {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.place-card:hover {
  transform: translateY(-3px);
}

.place-icon {
  font-size: 2rem;
  margin-right: 1.5rem;
  color: #4CAF50;
}

.place-info h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.place-info p {
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .ai-container {
    padding: 1rem;
  }

  .recommendations,
  .places {
    grid-template-columns: 1fr;
  }
}
</style> 