<template>
  <div class="music-recommendation-wrapper">
    <div class="loading-overlay" v-if="isLoading">
      <div class="loading-spinner"></div>
      <p>음악 추천을 생성하는 중입니다...</p>
    </div>

    <div v-else class="content">
      <h1 class="title">{{ book.title }} 관련 음악 추천</h1>
      
      <!-- 음악 추천 섹션 -->
      <section class="music-section">
        <div v-if="recommendedTracks.length > 0" class="music-grid">
          <div v-for="track in recommendedTracks" :key="track.id" class="music-card">
            <div class="album-cover">
              <img :src="track.albumCover" :alt="track.albumName" />
            </div>
            <div class="music-info">
              <h3 class="track-title">{{ track.name }}</h3>
              <p class="artist-name">{{ track.artist }}</p>
              <p class="album-name">{{ track.albumName }}</p>
            </div>
          </div>
        </div>
        <div v-else class="no-music">
          <p>관련 음악을 찾을 수 없습니다.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AIMusic',
  data() {
    return {
      book: {},
      recommendedTracks: [],
      isLoading: true,
      accessToken: null
    }
  },
  async created() {
    await this.loadBookData()
    await this.getSpotifyToken()
    await this.getMusicRecommendations()
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
    async getSpotifyToken() {
      try {
        const clientId = '21b8d2d1a90940faab04e31992183f98'
        const clientSecret = 'b96cb47acda642a98e901521e65d451c'
        
        const response = await axios.post('https://accounts.spotify.com/api/token', 
          'grant_type=client_credentials', {
          headers: {
            'Authorization': 'Basic ' + btoa(clientId + ':' + clientSecret),
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        
        this.accessToken = response.data.access_token
      } catch (error) {
        console.error('Spotify 토큰을 가져오는 데 실패했습니다:', error)
      }
    },
    async getMusicRecommendations() {
      try {
        const prompt = `다음 책의 내용을 바탕으로 관련된 음악을 3곡 추천해주세요:
제목: ${this.book.title}
작가: ${this.book.author}
줄거리: ${this.book.description}

책의 분위기, 주제, 감정을 잘 담고 있는 음악을 추천해주세요.
다음 형식으로 응답해주세요:
{
  "tracks": [
    {
      "name": "노래 제목",
      "artist": "가수 이름"
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
        
        // Spotify에서 각 트랙 검색
        for (const track of parsedContent.tracks) {
          await this.searchSpotifyTrack(track)
        }
        
        this.recommendedTracks = parsedContent.tracks
      } catch (error) {
        console.error('음악 추천을 가져오는 데 실패했습니다:', error)
      }
    },
    async searchSpotifyTrack(track) {
      try {
        const query = `${track.name} ${track.artist}`
        const response = await axios.get('https://api.spotify.com/v1/search', {
          params: {
            q: query,
            type: 'track',
            limit: 1
          },
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        })

        if (response.data.tracks.items.length > 0) {
          const spotifyTrack = response.data.tracks.items[0]
          track.id = spotifyTrack.id
          track.albumName = spotifyTrack.album.name
          track.albumCover = spotifyTrack.album.images[0].url
        }
      } catch (error) {
        console.error('Spotify 트랙 검색에 실패했습니다:', error)
      }
    }
  }
}
</script>

<style scoped>
.music-recommendation-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 93.9vh;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #1DB954;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
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

.music-section {
  margin-bottom: 40px;
}

.music-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.music-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.music-card:hover {
  transform: translateY(-5px);
}

.album-cover {
  width: 100%;
  padding-top: 100%;
  position: relative;
}

.album-cover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.music-info {
  padding: 15px;
}

.track-title {
  font-size: 1.2rem;
  margin: 0 0 10px 0;
  color: #333;
}

.artist-name {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.album-name {
  color: #888;
  font-size: 0.8rem;
}

.no-music {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #f5f5f5;
  border-radius: 10px;
}

@media (max-width: 768px) {
  .music-grid {
    grid-template-columns: 1fr;
  }
}
</style>