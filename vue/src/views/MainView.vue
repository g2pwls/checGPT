<template>
  <div class="main-container">
    <div class="search-container">
      <h1 class="title">AI 도서 검색</h1>
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
      <div v-if="loading" class="loading">
        검색 중...
      </div>
      <div v-if="recommendedBooks.length > 0" class="recommendations">
        <h2>추천 도서</h2>
        <div class="books-grid">
          <!-- 2순위 책 (왼쪽) -->
          <div v-if="recommendedBooks[1]" 
               class="book-card second"
               @click="goToBookDetail(recommendedBooks[1].id)">
            <div class="rank">2순위</div>
            <div class="match-percent">일치도: {{ recommendedBooks[1].matchPercent }}%</div>
            <img :src="recommendedBooks[1].cover" :alt="recommendedBooks[1].title" class="book-cover">
            <h3 class="book-title">{{ recommendedBooks[1].title }}</h3>
          </div>
          
          <!-- 1순위 책 (중앙) -->
          <div v-if="recommendedBooks[0]" 
               class="book-card first"
               @click="goToBookDetail(recommendedBooks[0].id)">
            <div class="rank">1순위</div>
            <div class="match-percent">일치도: {{ recommendedBooks[0].matchPercent }}%</div>
            <img :src="recommendedBooks[0].cover" :alt="recommendedBooks[0].title" class="book-cover">
            <h3 class="book-title">{{ recommendedBooks[0].title }}</h3>
          </div>
          
          <!-- 3순위 책 (오른쪽) -->
          <div v-if="recommendedBooks[2]" 
               class="book-card third"
               @click="goToBookDetail(recommendedBooks[2].id)">
            <div class="rank">3순위</div>
            <div class="match-percent">일치도: {{ recommendedBooks[2].matchPercent }}%</div>
            <img :src="recommendedBooks[2].cover" :alt="recommendedBooks[2].title" class="book-cover">
            <h3 class="book-title">{{ recommendedBooks[2].title }}</h3>
          </div>
        </div>
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
      apiKey: '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'
    }
  },
  created() {
    // 페이지 로드 시 검색 결과 초기화
    this.searchQuery = '';
    this.recommendedBooks = [];
    this.error = '';
  },
  methods: {
    async handleSearch() {
      if (!this.searchQuery.trim()) return;
      
      this.loading = true;
      this.recommendedBooks = [];
      this.error = '';
      
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
          .sort((a, b) => b.matchPercent - a.matchPercent)
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
                      content: `당신은 도서 추천 전문가입니다. 주어진 도서가 사용자의 요청("${this.searchQuery}")과 얼마나 일치하는지 분석해주세요. 반드시 다음과 같은 JSON 형식으로만 응답해주세요:
                      {
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
  min-height: 93.9vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

.search-container {
  width: 100%;
  max-width: 1200px;
  padding: 2rem;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 2rem;
  font-weight: bold;
  margin-top: 10px;
}

.search-box {
  display: flex;
  margin: 0 auto;
  max-width: 600px;
  background: white;
  border-radius: 50px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-input {
  flex: 1;
  padding: 1.5rem 2rem;
  border: none;
  border-radius: 50px 0 0 50px;
  font-size: 1.1rem;
  outline: none;
}

.search-button {
  padding: 1.5rem 2rem;
  border: none;
  background: #4CAF50;
  color: white;
  border-radius: 0 50px 50px 0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background: #45a049;
}

.loading {
  margin-top: 2rem;
  font-size: 1.1rem;
  color: #666;
}

.recommendations {
  margin-top: 3rem;
}

.recommendations h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 2rem;
}

.books-grid {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  padding: 1rem;
  position: relative;
  height: 500px;
}

.book-card {
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.book-card.first {
  order: 2;
  z-index: 3;
  transform: scale(1);
}

.book-card.second {
  order: 1;
  z-index: 2;
  transform: scale(0.85);
}

.book-card.third {
  order: 3;
  z-index: 1;
  transform: scale(0.7);
}

.rank {
  position: absolute;
  top: -10px;
  left: -10px;
  background: #4CAF50;
  color: white;
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
  background: #2196F3;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
  z-index: 1;
}

.book-cover {
  width: 100%;
  max-width: 200px;
  height: auto;
  margin-bottom: 1rem;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  margin: 0.5rem 0;
  text-align: center;
  max-width: 200px;
}

.error {
  margin-top: 2rem;
  padding: 1rem;
  background: #ffebee;
  color: #c62828;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .search-container {
    padding: 1rem;
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
    transform: none !important;
  }
  
  .book-cover {
    max-width: 150px;
  }
}
</style> 