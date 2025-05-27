<template>
  <div class="book-location">
    <div class="analysis-section">
      <h3>📚 이 책과 관련된 AI분석</h3>
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>AI가 책의 내용을 분석하고 있습니다...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="retryAnalysis" class="retry-button">다시 시도하기</button>
      </div>
      <div v-else-if="analysis" class="analysis-content">
        <div class="analysis-text">
          <h4>📍 추천 장소</h4>
          <p class="place">{{ recommendedPlace }}</p>
          <div class="divider"></div>
          <h4>📖 장소 선정 이유</h4>
          <p class="reason">{{ analysis }}</p>
        </div>
      </div>
    </div>

    <div v-if="mapUrl" class="map-section">
      <iframe 
        :src="mapUrl" 
        width="100%" 
        height="400" 
        style="border:0;" 
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        allowfullscreen>
      </iframe>
    </div>

    <div class="recommendation-section" v-if="recommendedBooks.length > 0">
      <h3>📚 이런 책은 어떠세요?</h3>
      <div class="recommended-books">
        <div v-for="book in recommendedBooks" :key="book.id" class="book-card" @click="goToBook(book.id)">
          <img :src="book.cover" :alt="book.title" class="book-cover">
          <div class="book-info">
            <div class="original-recommendation" v-if="book.original_recommendation.title !== book.title">
              <span class="ai-recommendation-label">AI 추천 도서</span>
              <p class="original-title">{{ book.original_recommendation.title }}</p>
              <p class="original-author">{{ book.original_recommendation.author }}</p>
            </div>
            <div class="matched-book">
              <span class="matched-label">매칭된 도서</span>
              <h4 class="book-title">{{ book.title }}</h4>
              <p class="book-author">{{ book.author }}</p>
            </div>
            <div class="divider"></div>
            <p class="recommendation-reason">
              <span class="reason-label">AI의 추천 이유</span>
              {{ book.recommendation_reason }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BookLocation',
  props: {
    book: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      error: null,
      analysis: null,
      recommendedPlace: null,
      mapUrl: null,
      recommendedBooks: []
    }
  },
  methods: {
    async analyzeBookLocation() {
      this.loading = true;
      this.error = null;
      this.analysis = null;
      this.recommendedPlace = null;
      this.mapUrl = null;
      
      try {
        const prompt = `다음 책을 분석하여 책과 가장 관련이 깊은 실제 장소를 찾아주세요:

제목: ${this.book.title}
작가: ${this.book.author}
줄거리: ${this.book.description}

다음 형식으로 답변해주세요:
1. 먼저 책의 내용을 깊이 있게 분석해주세요
2. 분석을 바탕으로 이 책과 가장 관련이 깊은 실제 장소 하나를 선정해주세요
3. 그 장소를 선정한 이유를 설명해주세요

응답 형식:
장소: [구체적인 장소 이름]
분석: [장소 선정 이유와 책과의 연관성]`;

        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
          model: "gpt-3.5-turbo",
          messages: [{
            role: "user",
            content: prompt
          }],
          temperature: 0.7,
          max_tokens: 500
        }, {
          headers: {
            'Authorization': `Bearer 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`,
            'Content-Type': 'application/json'
          }
        });

        const content = response.data.choices[0].message.content;
        this.processGPTResponse(content);
        await this.getBookRecommendations();
      } catch (error) {
        console.error('장소 분석 실패:', error);
        this.error = '장소를 분석하는 중에 문제가 발생했습니다. 잠시 후 다시 시도해주세요.';
      } finally {
        this.loading = false;
      }
    },

    async getBookRecommendations() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/books/${this.book.id}/recommend_similar/`,
          {
            headers: {
              Authorization: `Token ${localStorage.getItem('token')}`
            }
          }
        );
        
        this.recommendedBooks = response.data.map(rec => ({
          id: rec.book.id,
          cover: rec.book.cover,
          title: rec.book.title,
          author: rec.book.author,
          recommendation_reason: rec.reason
        }));
      } catch (error) {
        console.error('책 추천 실패:', error);
      }
    },

    goToBook(bookId) {
      if (bookId === this.book.id) return;
      this.$router.push(`/books/${bookId}`);
    },

    processGPTResponse(content) {
      const placeMatch = content.match(/장소:\s*([^\n]+)/);
      const analysisMatch = content.match(/분석:\s*([^\n]+)/);

      if (placeMatch) {
        this.recommendedPlace = placeMatch[1].trim();
        this.updateMapUrl(this.recommendedPlace);
      }
      if (analysisMatch) {
        this.analysis = analysisMatch[1].trim();
      }
    },

    updateMapUrl(place) {
      this.mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(place)}&output=embed`;
    },

    retryAnalysis() {
      this.analyzeBookLocation();
    }
  },
  async created() {
    await this.analyzeBookLocation();
  }
}
</script>

<style scoped>
.book-location {
  margin: 20px 0;
  font-family: 'Noto Sans KR', sans-serif;
}

.analysis-section {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.analysis-section h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.5em;
  text-align: center;
}

.analysis-section h4 {
  color: #34495e;
  margin: 15px 0 10px 0;
  font-size: 1.2em;
}

.analysis-content {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.analysis-text p {
  line-height: 1.6;
  color: #4a4a4a;
  margin: 10px 0;
}

.place {
  font-size: 1.2em;
  color: #2c3e50;
  font-weight: 500;
}

.reason {
  color: #666;
  line-height: 1.8;
}

.divider {
  height: 1px;
  background-color: #e0e0e0;
  margin: 20px 0;
}

.loading {
  text-align: center;
  padding: 40px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 20px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  color: #666;
  font-size: 1.1em;
}

.error {
  text-align: center;
  padding: 20px;
  background-color: #fff3f3;
  border-radius: 8px;
  margin-top: 10px;
}

.error p {
  color: #e74c3c;
  margin-bottom: 15px;
}

.retry-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #2980b9;
}

.map-section {
  margin-top: 20px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background-color: white;
  padding: 20px;
}

iframe {
  display: block;
  width: 100%;
  border-radius: 8px;
}

.recommendation-section {
  margin-top: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.recommendation-section h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.recommended-books {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.book-card {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
  display: flex;
  gap: 1rem;
}

.book-card:hover {
  transform: translateY(-2px);
}

.book-card .book-cover {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 0.25rem;
}

.book-info {
  flex: 1;
}

.book-info h4 {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.book-info .book-author {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.recommendation-reason {
  color: #555;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-top: 0.5rem;
}

.reason-label {
  display: block;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.3rem;
}

.original-recommendation {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.ai-recommendation-label, .matched-label {
  display: inline-block;
  font-size: 0.8em;
  padding: 3px 8px;
  border-radius: 4px;
  margin-bottom: 5px;
}

.ai-recommendation-label {
  background-color: #e3f2fd;
  color: #1976d2;
}

.matched-label {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.original-title {
  font-size: 1em;
  color: #1976d2;
  margin: 5px 0 2px 0;
  font-weight: 500;
}

.original-author {
  font-size: 0.9em;
  color: #666;
  margin: 0;
}

.matched-book {
  margin-top: 10px;
}

@media (max-width: 1024px) {
  .recommended-books {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .recommended-books {
    grid-template-columns: 1fr;
  }
}
</style> 