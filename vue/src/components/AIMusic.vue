<template>
  <div class="music-recommendation-wrapper">
    <h1 class="title">{{ book.title }} 관련 음악 추천</h1>
    
    <!-- 음악 추천 섹션 -->
    <section class="music-section">
      <div v-if="isLoading" class="section-loading">
        <div class="loading-spinner"></div>
        <p>음악 추천을 생성하는 중입니다...</p>
      </div>
      
      <div v-else-if="recommendedTracks.length > 0" class="music-grid">
        <div v-for="track in recommendedTracks" :key="track.id" 
             class="music-card"
             @click="openMusicModal(track, $event)">
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

    <!-- 음악 상세 모달 -->
    <div v-if="selectedTrack" class="music-modal" @click.self="closeMusicModal">
      <div class="modal-content" :style="modalStyle">
        <button class="close-button" @click="closeMusicModal">&times;</button>
        <div class="modal-body">
          <div class="modal-album">
            <img :src="selectedTrack.albumCover" :alt="selectedTrack.albumName" class="modal-album-cover">
            <div class="modal-info">
              <h2 class="modal-title">{{ selectedTrack.name }}</h2>
              <p class="modal-artist">{{ selectedTrack.artist }}</p>
              <div class="album-details">
                <h3>앨범</h3>
                <p>{{ selectedTrack.albumName }}</p>
                
              </div>
            </div>
          </div>
        </div>
      </div>
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
      accessToken: null,
      selectedTrack: null,
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

무엇보다 중요한 부분입니다.
위의 줄거리는 단순히 참고만 하고,
직접 해당 도서의 줄거리를 찾아서 이 책의 내용과 분위기, 주제, 감정과 밀접하게 관련된 음악 3가지를 추천해 주세요.

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
        
        // Spotify에서 각 트랙 검색 및 정보 가져오기
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
          // Spotify에서 가져온 정보로 업데이트
          track.id = spotifyTrack.id
          track.name = spotifyTrack.name
          track.artist = spotifyTrack.artists[0].name
          track.albumName = spotifyTrack.album.name
          track.albumCover = spotifyTrack.album.images[0].url
          
          // 앨범 ID를 저장
          track.albumId = spotifyTrack.album.id
          
          // 앨범 상세 정보 가져오기
          await this.getAlbumDetails(track)
        }
      } catch (error) {
        console.error('Spotify 트랙 검색에 실패했습니다:', error)
      }
    },
    async getAlbumDetails(track) {
      try {
        const response = await axios.get(`https://api.spotify.com/v1/albums/${track.albumId}`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        })
        
        if (response.data) {
          track.albumDescription = response.data.description || '앨범 설명이 없습니다.'
        }
      } catch (error) {
        console.error('앨범 상세 정보를 가져오는 데 실패했습니다:', error)
        track.albumDescription = '앨범 설명을 가져올 수 없습니다.'
      }
    },
    openMusicModal(track, event) {
      this.selectedTrack = track
      document.body.style.overflow = 'hidden'
      
      const card = event.currentTarget
      const rect = card.getBoundingClientRect()
      this.modalPosition = {
        top: rect.top,
        left: rect.left,
        width: rect.width,
        height: rect.height
      }
    },
    closeMusicModal() {
      this.selectedTrack = null
      document.body.style.overflow = 'auto'
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
  border-top: 4px solid #1DB954;
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

.music-modal {
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

.modal-content {
  background: white;
  border-radius: 15px;
  width: 90%;
  max-width: 500px;
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

.modal-album {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.modal-album-cover {
  width: 250px;
  height: 250px;
  border-radius: 10px;
  object-fit: cover;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.modal-info {
  text-align: center;
  width: 100%;
}

.modal-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
  word-break: keep-all;
}

.modal-artist {
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.album-details {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.album-details h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 10px;
}

.album-details p {
  color: #666;
  font-size: 1.1rem;
}

.album-description {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.album-description h4 {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 10px;
}

.album-description p {
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
  white-space: pre-line;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 10px;
  }

  .modal-body {
    padding: 20px;
  }

  .modal-album-cover {
    width: 200px;
    height: 200px;
  }

  .modal-title {
    font-size: 1.5rem;
  }

  .modal-artist {
    font-size: 1.1rem;
  }

  .album-details h3 {
    font-size: 1.1rem;
  }

  .album-details p {
    font-size: 1rem;
  }

  .album-description h4 {
    font-size: 1rem;
  }
  
  .album-description p {
    font-size: 0.9rem;
  }
}
</style>