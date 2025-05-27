<template>
  <div class="main-container">
    <div class="search-container" :class="{ 'loaded': isLoaded, 'results-loaded': recommendedBooks.length > 0 }">
      <h1 class="title">도서 AI 에이전트</h1>
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="어떤 책을 찾으시나요?"
          @keyup.enter="handleSearch"
          class="search-input"
        >
        <button @click="handleSearch" class="search-button">
          <i class="fas fa-search"></i>
        </button>
      </div>
      
      <!-- 로딩 인디케이터 -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <transition name="fade-text" mode="out-in">
          <p class="loading-message" :key="loadingMessage">{{ loadingMessage }}...</p>
        </transition>
      </div>

      <div v-if="recommendedBooks.length > 0" class="recommendations">
        <h2 class="h2-title">검색 결과</h2>
        <transition-group name="stagger-cards" tag="div" class="books-grid">
          <!-- 2순위 책 (왼쪽) -->
          <div v-if="recommendedBooks[1]" 
               class="book-card second"
               :key="recommendedBooks[1].id"
               @click="goToBookDetail(recommendedBooks[1].id)">
            <div class="rank">2순위</div>
            <div class="match-percent">일치도: {{ recommendedBooks[1].matchPercent }}%</div>
            <img :src="recommendedBooks[1].cover" :alt="recommendedBooks[1].title" class="book-cover">
            <h3 class="book-title">{{ recommendedBooks[1].title }}</h3>
          </div>
          
          <!-- 1순위 책 (중앙) -->
          <div v-if="recommendedBooks[0]" 
               class="book-card first"
               :key="recommendedBooks[0].id"
               @click="goToBookDetail(recommendedBooks[0].id)">
            <div class="rank">1순위</div>
            <div class="match-percent">일치도: {{ recommendedBooks[0].matchPercent }}%</div>
            <img :src="recommendedBooks[0].cover" :alt="recommendedBooks[0].title" class="book-cover">
            <h3 class="book-title">{{ recommendedBooks[0].title }}</h3>
          </div>
          
          <!-- 3순위 책 (오른쪽) -->
          <div v-if="recommendedBooks[2]" 
               class="book-card third"
               :key="recommendedBooks[2].id"
               @click="goToBookDetail(recommendedBooks[2].id)">
            <div class="rank">3순위</div>
            <div class="match-percent">일치도: {{ recommendedBooks[2].matchPercent }}%</div>
            <img :src="recommendedBooks[2].cover" :alt="recommendedBooks[2].title" class="book-cover">
            <h3 class="book-title">{{ recommendedBooks[2].title }}</h3>
          </div>
        </transition-group>
      </div>
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'MainView',
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      searchQuery: '',
      recommendedBooks: [],
      loading: false,
      error: '',
      apiKey: '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',
      isLoaded: false,
      loadingMessage: '잠시만 기다려 주세요',
      loadingMessages: [
        '잠시만 기다려 주세요',
        '도서를 분석하고 있습니다',
        '최적의 추천을 찾고 있습니다',
        '거의 다 됐습니다'
      ],
      messageInterval: null
    }
  },
  created() {
    // 페이지 로드 시 검색 결과 초기화
    this.searchQuery = '';
    this.recommendedBooks = [];
    this.error = '';
  },
  mounted() {
    // 초기 로드 애니메이션 트리거
    setTimeout(() => {
      this.isLoaded = true;
    }, 100);
  },
  beforeUnmount() {
    this.stopLoadingMessages();
  },
  methods: {
    startLoadingMessages() {
      let messageIndex = 0;
      this.loadingMessage = this.loadingMessages[messageIndex];
      this.messageInterval = setInterval(() => {
        messageIndex = (messageIndex + 1) % this.loadingMessages.length;
        this.loadingMessage = this.loadingMessages[messageIndex];
      }, 3000); // 느리게
    },
    stopLoadingMessages() {
      clearInterval(this.messageInterval);
      this.messageInterval = null;
    },
    async handleSearch() {
      if (!this.searchQuery.trim()) return;
      
      this.loading = true;
      this.recommendedBooks = [];
      this.error = '';
      this.startLoadingMessages();
      
      try {
        // GPT API를 통해 검색어 분석
        const gptResponse = await axios.post(
          'https://api.openai.com/v1/chat/completions',
          {
            model: 'gpt-4',
            messages: [
              {
                role: 'system',
                content: '당신은 도서 추천 전문가입니다. 사용자의 요청을 분석하여 검색에 사용할 키워드들을 추출하고, 각 키워드의 중요도를 백분율로 평가해주세요. 반드시 다음과 같은 JSON 형식으로만 응답해주세요: {"keywords": [{"word": "키워드1", "importance": 70}, {"word": "키워드2", "importance": 30}]}'
              },
              {
                role: 'user',
                content: this.searchQuery
              }
            ],
            temperature: 0.3,
            max_tokens: 500
          },
          {
            headers: {
              'Authorization': `Bearer ${this.apiKey}`,
              'Content-Type': 'application/json'
            }
          }
        );

        let keywordsData;
        try {
          keywordsData = JSON.parse(gptResponse.data.choices[0].message.content);
          if (!keywordsData.keywords || !Array.isArray(keywordsData.keywords)) {
            throw new Error('잘못된 GPT 응답 형식');
          }
        } catch (parseError) {
          console.error('GPT 응답 파싱 오류:', parseError);
          throw new Error('검색어 분석 중 오류가 발생했습니다.');
        }
        
        // 모든 도서 데이터 가져오기
        const booksResponse = await axios.get('http://127.0.0.1:8000/api/books/');
        const allBooks = booksResponse.data;
        
        if (!Array.isArray(allBooks)) {
          throw new Error('서버로부터 올바른 도서 데이터를 받지 못했습니다.');
        }

        // 도서 점수 계산 및 정렬
        const scoredBooks = allBooks.map(book => {
          let totalScore = 0;
          let maxPossibleScore = 0;
          
          keywordsData.keywords.forEach(keyword => {
            const keywordImportance = keyword.importance;
            maxPossibleScore += keywordImportance;
            
            let matchScore = 0;
            const searchWord = keyword.word.toLowerCase();
            
            // 설명 검색 (가중치: 1.0)
            if (book.description && book.description.toLowerCase().includes(searchWord)) {
              matchScore = keywordImportance * 1.0;
            }
            // 카테고리 검색 (가중치: 0.8)
            else if (book.categories && book.categories.some(cat => 
              cat.name.toLowerCase().includes(searchWord)
            )) {
              matchScore = keywordImportance * 0.8;
            }
            // 제목 검색 (가중치: 0.6)
            else if (book.title.toLowerCase().includes(searchWord)) {
              matchScore = keywordImportance * 0.6;
            }
            
            totalScore += matchScore;
          });
          
          const matchPercent = Math.min(100, Math.round((totalScore / maxPossibleScore) * 100));
          
          return {
            ...book,
            matchPercent: matchPercent,
            originalMatchPercent: matchPercent
          };
        });
        
        // 점수가 0보다 큰 책들만 필터링하고 상위 5권 선택
        let topBooks = scoredBooks
          .filter(book => book.matchPercent > 0)
          .sort((a, b) => {
              if (b.matchPercent === a.matchPercent) {
                  return (b.clicks || 0) - (a.clicks || 0); // 인기순 정렬
              }
              return b.matchPercent - a.matchPercent; // 일치도순 정렬
          })
          .slice(0, 5);

        // GPT를 통한 도서 분석 및 최종 점수 조정
        if (topBooks.length > 0) {
          const analysisPromises = topBooks.map(async (book) => {
            try {
              const analysisResponse = await axios.post(
                'https://api.openai.com/v1/chat/completions',
                {
                  model: 'gpt-4',
                  messages: [
                    {
                      role: 'system',
                      content: `당신은 도서 추천 전문가입니다. 주어진 도서가 사용자의 요청("${this.searchQuery}")과 얼마나 일치하는지 분석해주세요. 반드시 다음과 같은 JSON 형식으로만 응답해주세요:\n                      {
                        "score": 85,
                        "analysis": "이 책이 사용자의 요청과 일치하는 이유...",
                        "additional_info": "책에 대한 추가 발견 정보..."
                      }`
                    },
                    {
                      role: 'user',
                      content: `도서 제목: ${book.title}\n작가: ${book.author}\n줄거리: ${book.description}`
                    }
                  ],
                  temperature: 0.3,
                  max_tokens: 1000
                },
                {
                  headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                  }
                }
              );

              let gptAnalysis;
              try {
                gptAnalysis = JSON.parse(analysisResponse.data.choices[0].message.content);
                if (!gptAnalysis.score || !gptAnalysis.analysis || !gptAnalysis.additional_info) {
                  throw new Error('잘못된 GPT 분석 응답 형식');
                }
              } catch (parseError) {
                console.error('GPT 분석 응답 파싱 오류:', parseError);
                throw new Error('도서 분석 중 오류가 발생했습니다.');
              }

              const finalScore = Math.round((book.originalMatchPercent * 0.3) + (gptAnalysis.score * 0.7));
              
              return {
                ...book,
                matchPercent: finalScore,
                gptAnalysis: gptAnalysis.analysis,
                additionalInfo: gptAnalysis.additional_info
              };
            } catch (error) {
              console.error('도서 분석 오류:', error);
              return {
                ...book,
                matchPercent: book.originalMatchPercent,
                gptAnalysis: '분석을 불러올 수 없습니다.',
                additionalInfo: '추가 정보를 불러올 수 없습니다.'
              };
            }
          });

          try {
            topBooks = await Promise.all(analysisPromises);
            // 최종 점수로 다시 정렬하고 상위 3권만 선택
            topBooks = topBooks
              .sort((a, b) => b.matchPercent - a.matchPercent)
              .slice(0, 3);
          } catch (error) {
            console.error('도서 분석 결과 처리 오류:', error);
            throw new Error('도서 분석 결과를 처리하는 중 오류가 발생했습니다.');
          }
        }

        // 순위 지정 (일치도가 높은 순서대로)
        this.recommendedBooks = topBooks.map((book, index) => {
          return {
            ...book,
            rank: index + 1,
            matchPercent: book.matchPercent
          };
        });

        // 검색 결과를 localStorage에 저장
        localStorage.setItem('lastSearch', JSON.stringify({
          query: this.searchQuery,
          books: this.recommendedBooks
        }));

        if (this.recommendedBooks.length === 0) {
          this.error = '죄송합니다. 해당하는 도서를 찾을 수 없습니다.';
        }
      } catch (error) {
        console.error('검색 오류:', error);
        this.error = error.message || '검색 중 오류가 발생했습니다. 다시 시도해 주세요.';
      } finally {
        this.loading = false;
        this.stopLoadingMessages();
      }
    },
    
    goToBookDetail(bookId) {
      this.router.push(`/books/${bookId}`);
    },

    // 검색 결과 초기화
    clearSearch() {
      this.searchQuery = '';
      this.recommendedBooks = [];
      this.error = '';
      localStorage.removeItem('lastSearch');
    }
  }
}
</script>

<style scoped>
.main-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background-color: #ffffff; /* Keep monochromatic */
  padding: 20px;
}

.search-container {
  width: 100%;
  max-width: 1200px;
  padding: 2rem;
  text-align: center;
  padding-top: 250px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s, transform 0.6s, padding-top 0.7s cubic-bezier(.4,1.4,.6,1), margin-top 0.7s cubic-bezier(.4,1.4,.6,1);
}

.search-container.loaded {
  opacity: 1;
  transform: translateY(0);
}

.search-container.results-loaded {
  padding-top: 80px;
}

.title {
  font-size: 2.5rem;
  color: #000000; /* Keep monochromatic */
  margin-bottom: 2rem;
  font-weight: 300;
  margin-top: 10px;
  transition: margin-bottom 0.5s ease-out;
}

.search-container.results-loaded .title {
  margin-bottom: 1rem;
}

.search-box {
  display: flex;
  margin: 0 auto;
  max-width: 600px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #dadada;
  transition: margin-bottom 0.5s ease-out;
}

.search-container.results-loaded .search-box {
  margin-bottom: 1rem;
}

.search-input {
  flex: 1;
  padding: 1.5rem 2rem;
  border: none;
  border-radius: 15px 0 0 15px;
  font-size: 1.1rem;
  outline: none;
}

.search-button {
  padding: 1.5rem 2rem;
  border: none;
  background: #ffffff;
  color: #000;
  border-radius: 0 15px 15px 0;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button:hover {
  background: #777777;
}

.search-button i {
  color: #000;
  font-size: 1.2rem;
}

/* 로딩 인디케이터 스타일 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #333; /* Monochromatic */
  border-radius: 50%;
  animation: spin 2s linear infinite; /* Slowed down */
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-message {
  color: #666; /* Keep monochromatic */
  font-size: 1.1rem; /* Slightly larger */
  margin: 0;
  min-height: 1.1em; /* Prevent layout shift */
  transition: color 0.8s, opacity 0.8s;
  animation: fadeText 2.4s infinite alternate;
}

@keyframes fadeText {
  0% { color: #666; opacity: 1; }
  50% { color: #333; opacity: 0.5; }
  100% { color: #666; opacity: 1; }
}

.fade-text-enter-active, .fade-text-leave-active {
  transition: opacity 0.8s;
}
.fade-text-enter, .fade-text-leave-to {
  opacity: 0;
}

.recommendations {
  margin-top: 0.6rem;
}

.recommendations h2 {
  font-size: 1.8rem;
  color: #333; /* Keep monochromatic */
  margin-bottom: 1rem;
  text-align: center;
}

.books-grid {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 2rem;
  padding: 1rem;
  position: relative;
  height: 500px; /* Adjust as needed */
}

.book-card {
  background-color: #f9f9f9; /* Monochromatic */
  border: 1px solid #ddd; /* Monochromatic */
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Keep shadow */
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  position: relative;
  transition: transform 0.3s, box-shadow 0.3s, z-index 0.3s;
}

.book-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.18);
  transform: scale(1.03) translateY(-10px);
}

.book-card.first {
  z-index: 3;
  transform: scale(1.5);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  transition: transform 0.3s, box-shadow 0.3s, z-index 0.3s;
}

.book-card.first:hover {
  transform: scale(1.55);
  box-shadow: 0 12px 32px rgba(0,0,0,0.18);
}

.book-card.second {
  z-index: 2;
  transform: scale(1.1);
}

.book-card.third {
  z-index: 1;
  transform: scale(1.0);
}

.rank {
  position: absolute;
  top: -10px;
  left: -10px;
  background: #333; /* Monochromatic */
  color: white; /* Keep monochromatic */
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
  z-index: 1;
}

.match-percent {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #f3f3f3; /* Monochromatic */
  color: #333; /* Monochromatic */
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
  z-index: 1;
  border: 1px solid #ddd; /* Monochromatic */
}

.book-cover {
  width: 100%;
  max-width: 200px;
  height: auto;
  margin-bottom: 1rem;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Keep shadow */
  border: 1px solid #ddd; /* Monochromatic */
}

.book-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333; /* Monochromatic */
  margin: 0.5rem 0;
  text-align: center;
  max-width: 200px;
  line-height: 1.4;
}

.error {
  margin-top: 2rem;
  padding: 1rem;
  background: #f9f9f9; /* Monochromatic */
  color: #666; /* Monochromatic */
  border-radius: 5px;
  border: 1px solid #ddd; /* Monochromatic */
  text-align: center;
}

@media (max-width: 768px) {
  .search-container {
    padding: 1rem;
    margin: 20px auto;
  }

  .title {
    font-size: 2rem;
  }

  .search-input {
    padding: 1rem 1.5rem;
  }

  .search-button {
    padding: 1rem 1.5rem;
  }

  .books-grid {
    flex-direction: column;
    height: auto;
    gap: 1rem;
  }

  .book-card {
    position: static; /* Revert positioning for mobile */
    transform: none !important; /* Disable scale transforms for mobile */
    width: 80%;
    max-width: 300px;
    margin: 0 auto;
  }

  .book-cover {
    max-width: 150px;
  }
}

.stagger-cards-enter-active {
  transition: all 0.7s cubic-bezier(.4,1.4,.6,1);
}
.stagger-cards-leave-active {
  transition: all 0.3s cubic-bezier(.4,1.4,.6,1);
  opacity: 0;
}
.stagger-cards-enter-from {
  opacity: 0;
  transform: translateY(40px) scale(0.8);
}
.stagger-cards-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.h2-title{
  font-weight: 300;
  margin-bottom: 1rem;
}

</style> 
