<template>
  <div class="movie-recommendation-wrapper">
    <h1 class="title">{{ book.title }} 관련 영화 추천</h1>
    
    <!-- 영화 추천 섹션 -->
    <section class="movie-section">
      <div v-if="isLoading" class="section-loading">
        <div class="loading-spinner"></div>
        <p>영화 추천을 생성하는 중입니다...</p>
      </div>
      
      <div v-else-if="recommendedMovies.length > 0" class="movie-grid">
        <div v-for="movie in recommendedMovies" :key="movie.title" 
             class="movie-card" 
             :class="{ 'expanded': expandedMovie === movie }"
             @click="toggleMovieExpansion(movie)">
          <div class="movie-info">
            <h3 class="movie-title">{{ movie.title }}</h3>
            <p class="movie-year">{{ movie.year }}</p>
            <div class="movie-trailer" v-if="movie.trailerId">
              <iframe
                :src="`https://www.youtube.com/embed/${movie.trailerId}?rel=0`"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                loading="lazy"
              ></iframe>
            </div>
            <p class="movie-description">{{ movie.description }}</p>
          </div>
        </div>
      </div>
      <div v-else class="no-movies">
        <p>관련 영화를 찾을 수 없습니다.</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AIMovie',
  data() {
    return {
      book: {},
      recommendedMovies: [],
      isLoading: true,
      expandedMovie: null
    }
  },
  async created() {
    await this.loadBookData()
    await this.getMovieRecommendations()
    this.isLoading = false
  },
  methods: {
    async loadBookData() {
      try {
        const bookId = this.$route.params.bookId
        const response = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/`)
        this.book = response.data
      } catch (error) {
        console.error('책 정보를 불러오는 데 실패했습니다:', error)
      }
    },
    async getMovieRecommendations() {
      try {
        const prompt = `다음 책의 내용을 바탕으로 관련된 영화를 3가지 추천해주세요:
제목: ${this.book.title}
작가: ${this.book.author}
줄거리: ${this.book.description}

무엇보다 중요한 부분입니다.
위의 줄거리는 단순히 참고만 하고,
직접 해당 도서의 줄거리를 찾아서 이 책의 내용을 파악한 뒤 이 책의 내용과 밀접하게 관련된 영화 3가지를 추천해 주세요.
만약 해당 도서가 실제 사건을 바탕으로 한 책이라면,
해당 도서의 역사적 배경과 일치하는 배경을 가진 영화를 찾고, 그 중 관객 수가 가장 많은 순으로 보여 주세요.
예를 들어서, 한강 작가의 소년의 온다 책의 관련 영화는 '택시운전사', '변호인', '1987'으로 나와야 합니다.

다음 형식으로 응답해주세요:
{
  "movies": [
    {
      "title": "영화 제목",
      "year": "개봉년도",
      "description": "영화 설명"
    }
  ]
}
`

        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
          model: "gpt-4o-mini",
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
        })

        const content = response.data.choices[0].message.content
        const parsedContent = JSON.parse(content)
        this.recommendedMovies = parsedContent.movies

        // 각 영화의 예고편 검색
        for (let movie of this.recommendedMovies) {
          await this.searchMovieTrailer(movie)
        }
      } catch (error) {
        console.error('영화 추천을 가져오는 데 실패했습니다:', error)
      }
    },
    async searchMovieTrailer(movie) {
      try {
        const searchQuery = `${movie.title} 공식 예고편`
        const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
          params: {
            part: 'snippet',
            maxResults: 1,
            q: searchQuery,
            type: 'video',
            key: 'AIzaSyAVq5PqVceFYHi_vNGDWTWJPc_JH-3aJ94'
          }
        })

        if (response.data.items && response.data.items.length > 0) {
          movie.trailerId = response.data.items[0].id.videoId
        }
      } catch (error) {
        console.error('영화 예고편을 가져오는 데 실패했습니다:', error)
      }
    },
    toggleMovieExpansion(movie) {
      if (this.expandedMovie === movie) {
        this.expandedMovie = null
      } else {
        this.expandedMovie = movie
      }
    }
  }
}
</script>

<style scoped>
.movie-recommendation-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.section-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #f5f5f5;
  border-radius: 10px;
  margin: 20px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.movie-section {
  margin-bottom: 40px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.movie-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.movie-card.expanded {
  grid-column: 1 / -1;
  transform: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.movie-info {
  padding: 15px;
}

.movie-title {
  font-size: 1.2rem;
  margin: 0 0 10px 0;
  color: #333;
}

.movie-year {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.movie-trailer {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  margin: 15px 0;
}

.movie-trailer iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.movie-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-top: 15px;
}

.expanded .movie-description {
  font-size: 1.1rem;
  line-height: 1.6;
}

.no-movies {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #f5f5f5;
  border-radius: 10px;
}

@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: 1fr;
  }
  
  .movie-card.expanded {
    margin: 0 -20px;
    border-radius: 0;
  }
}
</style> 