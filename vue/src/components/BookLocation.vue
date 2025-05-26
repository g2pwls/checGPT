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
        const prompt = `다음 책과 비슷한 분위기나 주제를 가진 책을 추천해주세요:

제목: ${this.book.title}
작가: ${this.book.author}
줄거리: ${this.book.description}

이 책의 독자가 좋아할 만한 다른 책 3권을 추천해주세요.
반드시 3권의 책을 추천해주세요. 각 책에 대해 추천 이유도 자세히 설명해주세요.
책은 실제로 존재하는 책이어야 합니다.

응답 형식:
추천도서1: [책 제목] - [작가]
추천이유1: [추천 이유]
추천도서2: [책 제목] - [작가]
추천이유2: [추천 이유]
추천도서3: [책 제목] - [작가]
추천이유3: [추천 이유]`;

        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
          model: "gpt-3.5-turbo",
          messages: [{
            role: "user",
            content: prompt
          }],
          temperature: 0.7,
          max_tokens: 1000
        }, {
          headers: {
            'Authorization': `Bearer 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`,
            'Content-Type': 'application/json'
          }
        });

        const content = response.data.choices[0].message.content;
        await this.fetchRecommendedBooks(content);
      } catch (error) {
        console.error('책 추천 실패:', error);
      }
    },

    async fetchRecommendedBooks(gptResponse) {
      try {
        const recommendations = [];
        const lines = gptResponse.split('\n');
        
        for (let i = 0; i < lines.length; i++) {
          if (lines[i].startsWith('추천도서')) {
            const bookInfo = lines[i].split(/:\s*|\s*-\s*/g).slice(1);
            const reasonLine = lines[i + 1];
            if (reasonLine && reasonLine.startsWith('추천이유')) {
              const reason = reasonLine.split(/:\s*/)[1];
              recommendations.push({
                title: bookInfo[0].trim(),
                author: bookInfo[1].trim(),
                reason: reason.trim()
              });
            }
          }
        }

        const bookPromises = recommendations.map(async (rec) => {
          try {
            const response = await axios.get('http://127.0.0.1:8000/api/books/');
            const allBooks = response.data;
            
            // 1. 정확한 제목 매칭 시도
            let matchedBook = allBooks.find(book => 
              this.normalizeText(book.title) === this.normalizeText(rec.title)
            );

            // 2. 정확한 제목 매칭이 실패하면, 제목이 포함된 경우 검색
            if (!matchedBook) {
              const possibleMatches = allBooks.filter(book => 
                this.normalizeText(book.title).includes(this.normalizeText(rec.title)) ||
                this.normalizeText(rec.title).includes(this.normalizeText(book.title))
              );

              // 작가 이름으로 필터링
              if (possibleMatches.length > 0) {
                matchedBook = possibleMatches.find(book =>
                  this.normalizeText(book.author).includes(this.normalizeText(rec.author)) ||
                  this.normalizeText(rec.author).includes(this.normalizeText(book.author))
                );
              }

              // 여전히 매칭이 없으면 첫 번째 가능한 매치 사용
              if (!matchedBook && possibleMatches.length > 0) {
                matchedBook = possibleMatches[0];
              }
            }

            if (matchedBook) {
              return {
                ...matchedBook,
                recommendation_reason: rec.reason,
                original_recommendation: {
                  title: rec.title,
                  author: rec.author
                }
              };
            }
            return null;
          } catch (error) {
            console.error(`책 검색 실패 (${rec.title}):`, error);
            return null;
          }
        });

        const books = await Promise.all(bookPromises);
        this.recommendedBooks = books.filter(book => book);
      } catch (error) {
        console.error('추천 도서 검색 실패:', error);
      }
    },

    // 텍스트 정규화 함수
    normalizeText(text) {
      return text
        .toLowerCase()
        .replace(/\s+/g, '') // 모든 공백 제거
        .replace(/[^\w\s가-힣]/g, ''); // 특수문자 제거, 한글 유지
    },

    processGPTResponse(content) {
      const placeMatch = content.match(/장소:\s*(.+?)(?=\n|$)/);
      const analysisMatch = content.match(/분석:\s*(.+?)(?=\n|$)/);

      if (placeMatch && placeMatch[1]) {
        this.recommendedPlace = placeMatch[1].trim();
        this.updateMapUrl(this.recommendedPlace);
      }

      if (analysisMatch && analysisMatch[1]) {
        this.analysis = analysisMatch[1].trim();
      }

      if (!placeMatch || !analysisMatch) {
        this.error = 'AI의 응답을 처리하는 중에 문제가 발생했습니다.';
      }
    },

    updateMapUrl(place) {
      this.mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(place)}&output=embed`;
    },

    retryAnalysis() {
      this.analyzeBookLocation();
    },

    goToBook(bookId) {
      this.$router.push(`/books/${bookId}`);
    }
  },
  watch: {
    book: {
      handler(newBook) {
        if (newBook) {
          this.analyzeBookLocation();
        }
      },
      immediate: true
    }
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
  margin-top: 30px;
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.recommendation-section h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.5em;
  text-align: center;
}

.recommended-books {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.book-card {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.book-card .book-cover {
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.book-info {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.book-title {
  margin: 0;
  font-size: 1.2em;
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 8px;
}

.book-author {
  margin: 0;
  color: #666;
  font-size: 1em;
}

.divider {
  height: 1px;
  background-color: #eee;
  margin: 15px 0;
}

.recommendation-reason {
  margin: 0;
  font-size: 0.95em;
  color: #666;
  line-height: 1.5;
}

.reason-label {
  display: block;
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 5px;
  font-size: 0.9em;
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

@media (max-width: 1200px) {
  .recommended-books {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .recommended-books {
    grid-template-columns: 1fr;
  }

  .book-card .book-cover {
    height: 200px;
  }

  .book-info {
    padding: 15px;
  }
}
</style> 