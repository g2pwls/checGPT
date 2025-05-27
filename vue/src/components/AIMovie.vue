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
             @click="openMovieModal(movie, $event)">
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

    <!-- 영화 상세 모달 -->
    <div v-if="selectedMovie" class="movie-modal" @click.self="closeMovieModal">
      <div class="modal-content" :style="modalStyle">
        <button class="close-button" @click="closeMovieModal">&times;</button>
        <div class="modal-body">
          <h2 class="modal-title">{{ selectedMovie.title }}</h2>
          <p class="modal-year">{{ selectedMovie.year }}</p>
          <div class="modal-trailer" v-if="selectedMovie.trailerId">
            <iframe
              :src="`https://www.youtube.com/embed/${selectedMovie.trailerId}?rel=0&autoplay=1`"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
          <div class="modal-description">
            <h3>줄거리</h3>
            <p>{{ selectedMovie.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AIMovie',
  props: {
    book: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      recommendedMovies: [],
      isLoading: true,
      selectedMovie: null,
      modalPosition: null
    }
  },
  computed: {
    modalStyle() {
      if (!this.modalPosition) return {}
      
      return {
        '--initial-top': `${this.modalPosition.top}px`,
        '--initial-left': `${this.modalPosition.left}px`,
        '--initial-width': `${this.modalPosition.width}px`,
        '--initial-height': `${this.modalPosition.height}px`
      }
    }
  },
  async created() {
    await this.getMovieRecommendations()
    this.isLoading = false
  },
  methods: {
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
      "description": "영화 설명",
      "poster": "포스터 이미지 URL"
    }
  ]
}`

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

        // 각 영화에 대해 유튜브 예고편 검색
        for (const movie of this.recommendedMovies) {
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
    openMovieModal(movie, event) {
      this.selectedMovie = movie
      document.body.style.overflow = 'hidden'
      
      // 클릭한 카드의 위치 정보 저장
      const card = event.currentTarget
      const rect = card.getBoundingClientRect()
      this.modalPosition = {
        top: rect.top,
        left: rect.left,
        width: rect.width,
        height: rect.height
      }
    },
    closeMovieModal() {
      this.selectedMovie = null
      document.body.style.overflow = 'auto'
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
  transition: transform 0.3s ease;
  cursor: pointer;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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

.no-movies {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #f5f5f5;
  border-radius: 10px;
}

/* 모달 스타일 */
.movie-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease;
  will-change: opacity;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 15px;
  width: 90%;
  max-width: 800px;
  position: relative;
  transform-origin: center;
  will-change: transform, opacity;
}

@keyframes popup {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-content {
  animation: popup 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.close-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 2rem;
  color: #666;
  cursor: pointer;
  z-index: 1;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.modal-body {
  padding: 30px;
}

.modal-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
  word-break: keep-all;
}

.modal-year {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.modal-trailer {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  margin-bottom: 30px;
}

.modal-trailer iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.modal-description {
  margin-top: 20px;
}

.modal-description h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 15px;
}

.modal-description p {
  color: #666;
  line-height: 1.6;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    margin: 10px;
  }

  .modal-body {
    padding: 20px;
  }

  .modal-title {
    font-size: 1.5rem;
  }

  .modal-description p {
    font-size: 1rem;
  }
}
</style> 