<template>
  <div class="movie-recommendation">
    <h2>AI 영화 추천</h2>
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>영화를 찾고 있어요...</p>
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else class="movie-content">
      <div class="movie-info">
        <img :src="movie.poster" :alt="movie.title" class="movie-poster" />
        <div class="movie-details">
          <h3>{{ movie.title }}</h3>
          <p class="movie-description">{{ movie.description }}</p>
          <p class="movie-reason">{{ movie.recommendationReason }}</p>
        </div>
      </div>
      
      <div class="video-section">
        <h3>관련 영상</h3>
        <div class="video-container">
          <iframe
            v-if="videoId"
            :src="`https://www.youtube.com/embed/${videoId}`"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
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
      movie: null,
      videoId: null,
      isLoading: true,
      error: null
    }
  },
  async created() {
    await this.getMovieRecommendation()
  },
  methods: {
    async getMovieRecommendation() {
      try {
        // First, get movie recommendation from GPT
        const gptResponse = await axios.post('https://api.openai.com/v1/chat/completions', {
          model: "gpt-3.5-turbo",
          messages: [{
            role: "user",
            content: `다음 책의 내용을 바탕으로 가장 관련성이 높은 영화를 추천해주세요:
제목: ${this.book.title}
작가: ${this.book.author}
줄거리: ${this.book.description}

다음 형식으로 응답해주세요:
{
  "title": "영화 제목",
  "description": "영화 설명",
  "recommendationReason": "이 영화를 추천하는 이유"
}`
          }],
          temperature: 0.7,
          max_tokens: 500
        }, {
          headers: {
            'Authorization': `Bearer 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`,
            'Content-Type': 'application/json'
          }
        })

        const movieData = JSON.parse(gptResponse.data.choices[0].message.content)
        
        // Get movie poster from TMDB API
        const tmdbResponse = await axios.get(`https://api.themoviedb.org/3/search/movie`, {
          params: {
            api_key: 'YOUR_TMDB_API_KEY', // You'll need to get a TMDB API key
            query: movieData.title
          }
        })

        if (tmdbResponse.data.results.length > 0) {
          const posterPath = tmdbResponse.data.results[0].poster_path
          movieData.poster = `https://image.tmdb.org/t/p/w500${posterPath}`
        }

        this.movie = movieData

        // Search for related YouTube videos
        await this.searchYouTubeVideos(movieData.title)
      } catch (error) {
        console.error('Error getting movie recommendation:', error)
        this.error = '영화 추천을 가져오는 중 오류가 발생했습니다.'
      } finally {
        this.isLoading = false
      }
    },

    async searchYouTubeVideos(movieTitle) {
      try {
        const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
          params: {
            part: 'snippet',
            maxResults: 1,
            q: `${movieTitle} official trailer`,
            type: 'video',
            key: 'AIzaSyBYSS0TB0NZYLQSSA1yY_HNm8IK7-pSztE'
          }
        })

        if (response.data.items.length > 0) {
          this.videoId = response.data.items[0].id.videoId
        }
      } catch (error) {
        console.error('Error searching YouTube videos:', error)
      }
    }
  }
}
</script>

<style scoped>
.movie-recommendation {
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  color: #e74c3c;
  text-align: center;
  padding: 20px;
}

.movie-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.movie-info {
  display: flex;
  gap: 30px;
}

.movie-poster {
  width: 300px;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.movie-details {
  flex: 1;
}

.movie-details h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.movie-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.movie-reason {
  color: #e74c3c;
  font-style: italic;
  line-height: 1.6;
}

.video-section {
  margin-top: 20px;
}

.video-section h3 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 10px;
}

@media (max-width: 768px) {
  .movie-info {
    flex-direction: column;
  }

  .movie-poster {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }
}
</style>