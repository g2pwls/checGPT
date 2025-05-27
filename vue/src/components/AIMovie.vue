<template>
  <div class="movie-recommendation-wrapper">
    <h1 class="title">{{ book.title }} 관련 영화 추천</h1>
    <div class="divider"></div>
    
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
  box-sizing: border-box;
  margin-top: 30px;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 25px;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  width: 100%;
}

.section-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background-color: #f8f8f8; /* 밝은 회색 배경 */
  border-radius: 8px; /* 둥근 모서리 */
  margin: 20px 0;
  border: 1px solid #eee;
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
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 10px;
  text-align: center;
  padding-bottom: 0;
  border-bottom: none;
}

.divider {
  width: 100%;
  height: 1px;
  background: #e0e0e0;
  margin: 20px 0;
  border-radius: 1px;
}

.movie-section {
  width: 100%;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  width: 100%;
}

.movie-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.movie-card:hover {
  transform: translateY(-3px); /* 호버 효과 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 호버 그림자 */
}

.movie-info {
  padding: 15px; /* 패딩 */
  flex-grow: 1; /* 남은 공간 채우기 */
  display: flex;
  flex-direction: column;
}

.movie-title {
  font-size: 1.1rem; /* 폰트 크기 조정 */
  font-weight: bold;
  color: #333;
  margin-bottom: 8px; /* 마진 */
}

.movie-year {
  font-size: 0.9rem; /* 폰트 크기 조정 */
  color: #777;
  margin-bottom: 10px;
}

.movie-trailer {
  width: 100%;
  height: 180px; /* 트레일러 높이 */
  margin-bottom: 10px;
}

.movie-trailer iframe {
  width: 100%;
  height: 100%;
  border-radius: 4px; /* 둥근 모서리 */
}

.movie-description {
  font-size: 0.95rem; /* 폰트 크기 조정 */
  color: #555;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 4; /* 최대 4줄 */
  -webkit-box-orient: vertical;
}

.no-movies {
  text-align: center;
  padding: 40px;
  background-color: #ffffff; /* 흰색 배경 */
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid #ddd;
  color: #777;
}

/* 영화 상세 모달 스타일 */
.movie-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7); /* 더 어두운 오버레이 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000; /* AIView의 모달보다 위에 표시 */
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background-color: #ffffff; /* 흰색 배경 */
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); /* 그림자 강화 */
  max-width: 800px;
  width: 90%;
  position: relative;
  animation: scaleIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.8rem; /* 폰트 크기 증가 */
  border: none;
  background: none;
  cursor: pointer;
  color: #777; /* 무채색 */
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #333; /* 호버 색상 */
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal-title {
  font-size: 1.8rem; /* 폰트 크기 */
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.modal-year {
  font-size: 1rem;
  color: #777;
  margin-bottom: 10px;
}

.modal-trailer {
  width: 100%;
  height: 400px; /* 모달 트레일러 높이 */
}

.modal-trailer iframe {
  width: 100%;
  height: 100%;
  border-radius: 4px;
}

.modal-description h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.modal-description p {
  font-size: 1rem;
  color: #555;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); /* 모바일 그리드 */
    gap: 15px;
  }

  .movie-card {
    flex-direction: column;
  }

  .movie-info {
    padding: 10px;
  }

  .movie-trailer {
    height: 150px; /* 모바일 트레일러 높이 */
  }

  .modal-content {
    padding: 20px;
  }

  .modal-trailer {
    height: 250px; /* 모바일 모달 트레일러 높이 */
  }

  .modal-title {
    font-size: 1.5rem;
  }
}
</style> 